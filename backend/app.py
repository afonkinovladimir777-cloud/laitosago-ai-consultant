from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from rag.retriever import RAGRetriever
from rag.llm import LLMClient
from rag.chunker import KnowledgeBaseProcessor
from api.lead import LeadHandler
from api.models import ModelManager

load_dotenv()

app = FastAPI(
    title="LaitOSAGO AI Consultant API",
    description="RAG-based AI consultant for LaitOSAGO insurance products",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
rag_retriever = None
llm_client = None
lead_handler = None
model_manager = None


class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = None
    conversation_history: Optional[List[dict]] = None


class ChatResponse(BaseModel):
    answer: str
    chunks: List[dict]
    model_used: str


class LeadRequest(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    product_type: Optional[str] = None
    comment: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    global rag_retriever, llm_client, lead_handler, model_manager
    
    print("🚀 Initializing LaitOSAGO AI Consultant...")
    
    try:
        # Initialize RAG
        print("📚 Loading and indexing knowledge base...")
        kb_processor = KnowledgeBaseProcessor()
        documents = kb_processor.load_knowledge_base("backend/data/knowledge_base.txt")
        rag_retriever = RAGRetriever()
        rag_retriever.index_documents(documents)
        print(f"✅ Indexed {len(documents)} documents")
        
        # Initialize LLM
        llm_client = LLMClient()
        
        # Initialize Lead Handler
        lead_handler = LeadHandler()
        
        # Initialize Model Manager
        model_manager = ModelManager()
        
        print("✅ All services initialized successfully!")
    
    except Exception as e:
        print(f"❌ Error during startup: {str(e)}")
        raise


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process user message and return AI response with retrieved chunks"""
    try:
        if not rag_retriever or not llm_client:
            raise HTTPException(status_code=500, detail="Services not initialized")
        
        # Retrieve relevant chunks
        retrieved_chunks = rag_retriever.retrieve(request.message, top_k=5)
        
        # Prepare context from chunks
        context = "\n\n".join([
            f"[Документ: {chunk['doc_id']} | {chunk['category']} | {chunk['title']}]\n{chunk['text']}"
            for chunk in retrieved_chunks
        ])
        
        # Get LLM response
        model = request.model or "deepseek/deepseek-chat:free"
        answer = await llm_client.generate_response(
            message=request.message,
            context=context,
            conversation_history=request.conversation_history or [],
            model=model
        )
        
        # Format chunks with similarity scores
        formatted_chunks = [
            {
                "chunk_id": i + 1,
                "doc_id": chunk["doc_id"],
                "category": chunk["category"],
                "title": chunk["title"],
                "text": chunk["text"],
                "similarity": float(chunk["similarity"])
            }
            for i, chunk in enumerate(retrieved_chunks)
        ]
        
        return ChatResponse(
            answer=answer,
            chunks=formatted_chunks,
            model_used=model
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
async def get_models():
    """Get list of available free models from OpenRouter"""
    try:
        models = await model_manager.get_free_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/lead")
async def submit_lead(request: LeadRequest):
    """Submit lead form and send email notification"""
    try:
        if not request.name or not request.phone:
            raise HTTPException(status_code=400, detail="Name and phone are required")
        
        # Send email
        success = await lead_handler.send_lead_email(
            name=request.name,
            phone=request.phone,
            email=request.email,
            product_type=request.product_type,
            comment=request.comment
        )
        
        if success:
            return {"status": "success", "message": "Заявка успешно отправлена!"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send lead")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "LaitOSAGO AI Consultant",
        "rag_ready": rag_retriever is not None,
        "llm_ready": llm_client is not None
    }


@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "name": "LaitOSAGO AI Consultant API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "POST /chat": "Send message and get AI response",
            "GET /models": "Get available models",
            "POST /lead": "Submit lead form",
            "GET /health": "Health check"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("FASTAPI_HOST", "0.0.0.0"),
        port=int(os.getenv("FASTAPI_PORT", 8000))
    )

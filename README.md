# LaitOSAGO AI Consultant

Русскоязычное RAG-приложение "AI-консультант LaitOSAGO" — полнофункциональный чат-консультант на основе собственной базы знаний компании с лидогенерацией.

## 🚀 Особенности

- **RAG система**: Полноценная система поиска с FAISS и многоязычными эмбеддингами
- **Локальный индекс**: Быстрый поиск через FAISS векторную базу данных
- **Бесплатные модели**: Интеграция с OpenRouter для доступа к бесплатным LLM
- **Многоязычные эмбеддинги**: Отличная поддержка русского языка
- **Лидогенерация**: Встроенная форма заявки с отправкой email уведомлений
- **Адаптивный дизайн**: Полная поддержка мобильных и desktop устройств
- **История сессии**: Контекст диалога в памяти браузера

## 📋 Требования

- Python 3.9+
- Node.js 18+
- OpenRouter API ключ
- Email адрес для отправки уведомлений

## 🛠 Установка

### Backend

```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## ⚙️ Конфигурация

### 1. Скопируйте .env.example в .env

```bash
cp .env.example .env
```

### 2. Заполните переменные окружения

```env
# OpenRouter API
OPENROUTER_API_KEY=your_key_here

# Email (Yandex example)
EMAIL_ADDRESS=laitosago@yandex.ru
EMAIL_PASSWORD=your_app_password_here
EMAIL_SMTP_SERVER=smtp.yandex.ru
EMAIL_SMTP_PORT=587

# Addresses
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
REACT_APP_API_BASE_URL=http://localhost:8000
```

## 🚀 Запуск

### Backend

```bash
cd backend
python app.py
```

API будет доступно на `http://localhost:8000`

Документация: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm run dev
```

Приложение откроется на `http://localhost:5173`

## 📚 API Endpoints

### POST /chat
Отправить сообщение и получить ответ с найденными чанками.

**Request:**
```json
{
  "message": "Что такое ОСАГО?",
  "model": "deepseek/deepseek-chat:free",
  "conversation_history": []
}
```

**Response:**
```json
{
  "answer": "ОСАГО — обязательное страхование...",
  "chunks": [
    {
      "chunk_id": 1,
      "doc_id": "osago_definition",
      "category": "osago",
      "title": "Что такое ОСАГО",
      "text": "...",
      "similarity": 0.95
    }
  ],
  "model_used": "deepseek/deepseek-chat:free"
}
```

### GET /models
Получить список доступных бесплатных моделей.

### POST /lead
Отправить заявку с контактными данными.

**Request:**
```json
{
  "name": "Иван Петров",
  "phone": "+7 999 123-45-67",
  "email": "ivan@example.com",
  "product_type": "ОСАГО",
  "comment": "Хочу оформить ОСАГО"
}
```

### GET /health
Проверка статуса сервиса.

## 🔑 Получение API ключей

### OpenRouter API

1. Перейдите на [openrouter.ai](https://openrouter.ai)
2. Создайте аккаунт
3. Перейдите в Settings → API Keys
4. Создайте новый ключ
5. Скопируйте в `OPENROUTER_API_KEY`

### Email (Yandex)

1. Перейдите в [passport.yandex.ru](https://passport.yandex.ru)
2. Безопасность → Пароли приложений
3. Создайте пароль для Почты
4. Используйте как `EMAIL_PASSWORD`

## 📁 Структура проекта

```
laitosago-ai-consultant/
├── backend/
│   ├── rag/
│   │   ├── chunker.py         # Обработка документов
│   │   ├── embeddings.py      # Embeddings модель
│   │   ├── faiss_store.py     # FAISS индекс
│   │   ├── retriever.py       # RAG retriever
│   │   └── llm.py             # LLM интеграция
│   ├── api/
│   │   ├── lead.py            # Обработка заявок
│   │   └── models.py          # Управление моделями
│   ├── data/
│   │   └── knowledge_base.txt  # База знаний
│   ├── app.py                 # FastAPI приложение
│   └── requirements.txt        # Python зависимости
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── ChunkViewer.tsx
│   │   │   ├── LeadForm.tsx
│   │   │   └── ModelSelector.tsx
│   │   ├── pages/
│   │   │   └── App.tsx
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── .env.example
├── .gitignore
└── README.md
```

## 🎯 Технологический стек

### Backend
- **FastAPI** - REST API
- **Python** - язык программирования
- **FAISS** - векторный поиск
- **Sentence Transformers** - embeddings
- **aiosmtplib** - email отправка

### Frontend
- **React** 18 - UI фреймворк
- **TypeScript** - типизированный JavaScript
- **TailwindCSS** - утилиты стилизации
- **Vite** - сборщик
- **Axios** - HTTP клиент

## 📝 Лицензия

MIT

## 👥 Контакты

LaitOSAGO  
Телефон: +7 (968) 103-08-19  
Email: laitosago@yandex.ru

import React from 'react'
import { X } from 'lucide-react'
import { Chunk } from '../api/client'

interface ChunkViewerProps {
  chunks: Chunk[]
  onClose: () => void
}

export const ChunkViewer: React.FC<ChunkViewerProps> = ({ chunks, onClose }) => {
  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        <h2 className="text-lg font-bold text-gray-900">Найденные источники</h2>
        <button
          onClick={onClose}
          className="p-1 hover:bg-gray-100 rounded-lg transition"
        >
          <X size={20} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chunks.map((chunk, index) => (
          <div key={chunk.chunk_id} className="border-l-4 border-blue-500 pl-3">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-semibold text-sm text-gray-900">
                Чанк #{index + 1}
              </h3>
              <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                {(chunk.similarity * 100).toFixed(0)}%
              </span>
            </div>

            <div className="mb-2 text-xs text-gray-600">
              <p>
                <strong>Категория:</strong> {chunk.category}
              </p>
              <p>
                <strong>Название:</strong> {chunk.title}
              </p>
              <p>
                <strong>ID документа:</strong> {chunk.doc_id}
              </p>
            </div>

            <p className="text-sm text-gray-700 line-clamp-4">{chunk.text}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

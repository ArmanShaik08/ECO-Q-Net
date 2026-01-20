import { Upload } from 'lucide-react';
import { useRef, useState } from 'react';

interface UploadZoneProps {
  onImageUpload: (file: File) => void;
}

export function UploadZone({ onImageUpload }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      onImageUpload(file);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageUpload(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
      className={`
        relative border-2 border-dashed rounded-2xl p-16 text-center cursor-pointer
        transition-all duration-200
        ${isDragging 
          ? 'border-emerald-500 bg-emerald-50 scale-105' 
          : 'border-gray-300 bg-white hover:border-emerald-400 hover:bg-emerald-50/50'
        }
      `}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        className="hidden"
      />
      
      <div className="flex flex-col items-center gap-4">
        <div className={`
          w-20 h-20 rounded-full flex items-center justify-center transition-colors
          ${isDragging ? 'bg-emerald-100' : 'bg-gray-100'}
        `}>
          <Upload className={`w-10 h-10 ${isDragging ? 'text-emerald-600' : 'text-gray-400'}`} />
        </div>
        
        <div>
          <p className="text-xl font-medium text-gray-900 mb-2">
            Upload Camera Trap Image
          </p>
          <p className="text-gray-600 mb-1">
            Drop an image here or click to browse
          </p>
          <p className="text-sm text-gray-500">
            Supports JPG, PNG, and other common formats
          </p>
        </div>
      </div>
    </div>
  );
}

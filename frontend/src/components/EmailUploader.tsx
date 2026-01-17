import { useCallback, useState } from "react"
import { Upload, File, X } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface EmailUploaderProps {
  onFileSelect: (file: File) => void
  selectedFile: File | null
  onClear: () => void
  disabled?: boolean
}

const MAX_FILE_SIZE = 10 * 1024 * 1024
const ACCEPTED_TYPES = [".txt", ".pdf"]

export function EmailUploader({
  onFileSelect,
  selectedFile,
  onClear,
  disabled = false,
}: EmailUploaderProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const validateFile = (file: File): string | null => {
    const fileExtension = "." + file.name.split(".").pop()?.toLowerCase()
    
    if (!ACCEPTED_TYPES.includes(fileExtension)) {
      return `Tipo de arquivo não suportado. Use apenas ${ACCEPTED_TYPES.join(" ou ")}`
    }

    if (file.size > MAX_FILE_SIZE) {
      return `Arquivo muito grande. Tamanho máximo: ${MAX_FILE_SIZE / 1024 / 1024}MB`
    }

    return null
  }

  const handleFile = useCallback(
    (file: File) => {
      setError(null)
      const validationError = validateFile(file)
      
      if (validationError) {
        setError(validationError)
        return
      }

      onFileSelect(file)
    },
    [onFileSelect]
  )

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (!disabled) {
      setIsDragging(true)
    }
  }, [disabled])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      e.stopPropagation()
      setIsDragging(false)

      if (disabled) return

      const file = e.dataTransfer.files[0]
      if (file) {
        handleFile(file)
      }
    },
    [handleFile, disabled]
  )

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0]
      if (file) {
        handleFile(file)
      }
      e.target.value = ""
    },
    [handleFile]
  )

  if (selectedFile) {
    return (
      <Card className="p-6">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 flex-1 min-w-0">
            <div className="flex-shrink-0">
              <File className="h-8 w-8 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-medium text-sm truncate">{selectedFile.name}</p>
              <p className="text-xs text-muted-foreground">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClear}
            disabled={disabled}
            className="flex-shrink-0"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </Card>
    )
  }

  return (
    <div className="space-y-2">
      <Card
        className={cn(
          "border-2 border-dashed transition-colors cursor-pointer",
          isDragging && "border-primary bg-primary/5",
          !isDragging && "border-muted-foreground/25 hover:border-primary/50",
          disabled && "opacity-50 cursor-not-allowed"
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !disabled && document.getElementById("file-input")?.click()}
      >
        <div className="flex flex-col items-center justify-center p-8 gap-4">
          <Upload
            className={cn(
              "h-12 w-12 transition-colors",
              isDragging ? "text-primary" : "text-muted-foreground"
            )}
          />
          <div className="text-center space-y-1">
            <p className="text-sm font-medium">
              Arraste o arquivo aqui ou clique para selecionar
            </p>
            <p className="text-xs text-muted-foreground">
              Formatos aceitos: .txt, .pdf (máximo 10MB)
            </p>
          </div>
          <Button
            type="button"
            variant="outline"
            disabled={disabled}
            onClick={(e) => {
              e.stopPropagation()
              document.getElementById("file-input")?.click()
            }}
          >
            Selecionar Arquivo
          </Button>
        </div>
      </Card>
      <input
        id="file-input"
        type="file"
        accept=".txt,.pdf"
        className="hidden"
        onChange={handleFileInput}
        disabled={disabled}
      />
      {error && (
        <p className="text-sm text-destructive mt-2">{error}</p>
      )}
    </div>
  )
}

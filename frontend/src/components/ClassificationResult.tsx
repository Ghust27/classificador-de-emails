import { useState } from "react"
import { Copy, Check, Mail, Sparkles } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import type { EmailClassification } from "@/lib/types"

interface ClassificationResultProps {
  result: EmailClassification
}

export function ClassificationResult({ result }: ClassificationResultProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.suggested_response)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error("Erro ao copiar:", error)
    }
  }

  const isProductive = result.category === "Produtivo"

  return (
    <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Mail className="h-5 w-5" />
              Classificação
            </CardTitle>
            <Badge
              variant={isProductive ? "productive" : "unproductive"}
              className="text-sm px-3 py-1"
            >
              {result.category}
            </Badge>
          </div>
          {result.confidence !== undefined && (
            <p className="text-sm text-muted-foreground mt-2">
              Confiança: {Math.round(result.confidence * 100)}%
            </p>
          )}
        </CardHeader>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5" />
            Resposta Sugerida
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="bg-muted/50 rounded-lg p-4 border">
            <p className="text-sm whitespace-pre-wrap leading-relaxed">
              {result.suggested_response}
            </p>
          </div>
          <Button
            variant="outline"
            onClick={handleCopy}
            className="w-full sm:w-auto"
          >
            {copied ? (
              <>
                <Check className="h-4 w-4 mr-2" />
                Copiado!
              </>
            ) : (
              <>
                <Copy className="h-4 w-4 mr-2" />
                Copiar Resposta
              </>
            )}
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

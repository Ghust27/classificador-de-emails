import { useState } from "react"
import { Mail, Loader2 } from "lucide-react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs"
import { Button } from "./components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import { Alert, AlertDescription, AlertTitle } from "./components/ui/alert"
import { EmailUploader } from "./components/EmailUploader"
import { EmailTextInput } from "./components/EmailTextInput"
import { ClassificationResult } from "./components/ClassificationResult"
import { LoadingSpinner } from "./components/LoadingSpinner"
import { classifyEmailFromFile, classifyEmailFromText } from "./lib/api"

function App() {
  const [activeTab, setActiveTab] = useState("upload")
  const [selectedFile, setSelectedFile] = useState(null)
  const [emailText, setEmailText] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileSelect = (file) => {
    setSelectedFile(file)
    setError(null)
    setResult(null)
  }

  const handleFileClear = () => {
    setSelectedFile(null)
    setError(null)
    setResult(null)
  }

  const handleTextChange = (text) => {
    setEmailText(text)
    setError(null)
    setResult(null)
  }

  const handleClassify = async () => {
    setError(null)
    setResult(null)
    setIsLoading(true)

    try {
      let classification

      if (activeTab === "upload") {
        if (!selectedFile) {
          setError("Por favor, selecione um arquivo antes de classificar.")
          setIsLoading(false)
          return
        }
        classification = await classifyEmailFromFile(selectedFile)
      } else {
        if (!emailText.trim()) {
          setError("Por favor, insira o texto do email antes de classificar.")
          setIsLoading(false)
          return
        }
        classification = await classifyEmailFromText(emailText.trim())
      }

      setResult(classification)
    } catch (err) {
      setError(
        err.message || "Erro ao classificar email. Verifique sua conexão e tente novamente."
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewClassification = () => {
    setResult(null)
    setError(null)
    setSelectedFile(null)
    setEmailText("")
  }

  const canClassify = activeTab === "upload" 
    ? selectedFile !== null 
    : emailText.trim().length > 0

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 md:py-12 max-w-4xl">
        <div className="text-center mb-8 space-y-2">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Mail className="h-8 w-8 text-primary" />
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
              Classificador de Emails
            </h1>
          </div>
          <p className="text-muted-foreground text-lg">
            Classifique emails automaticamente em Produtivo ou Improdutivo e receba respostas sugeridas
          </p>
        </div>

        <div className="space-y-6">
          {!result ? (
            <>
              <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v)}>
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="upload">Upload de Arquivo</TabsTrigger>
                  <TabsTrigger value="text">Entrada de Texto</TabsTrigger>
                </TabsList>

                <TabsContent value="upload" className="space-y-4">
                  <EmailUploader
                    onFileSelect={handleFileSelect}
                    selectedFile={selectedFile}
                    onClear={handleFileClear}
                    disabled={isLoading}
                  />
                </TabsContent>

                <TabsContent value="text" className="space-y-4">
                  <EmailTextInput
                    value={emailText}
                    onChange={handleTextChange}
                    disabled={isLoading}
                  />
                </TabsContent>
              </Tabs>

              {error && (
                <Alert variant="destructive">
                  <AlertTitle>Erro</AlertTitle>
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="flex justify-center">
                <Button
                  onClick={handleClassify}
                  disabled={!canClassify || isLoading}
                  className="w-full md:w-auto"
                  size="lg"
                >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Classificando...
                  </>
                ) : (
                  <>
                    <Mail className="mr-2 h-4 w-4" />
                    Classificar Email
                  </>
                )}
                </Button>
              </div>
            </>
          ) : (
            <>
              <ClassificationResult result={result} />
              <div className="flex justify-center pt-4">
                <Button
                  onClick={handleNewClassification}
                  variant="outline"
                  size="lg"
                >
                  Nova Classificação
                </Button>
              </div>
            </>
          )}
        </div>

        {isLoading && (
          <div className="fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50">
            <Card className="p-8">
              <CardHeader>
                <CardTitle className="text-center">Processando...</CardTitle>
                <CardDescription className="text-center">
                  Aguarde enquanto classificamos o email
                </CardDescription>
              </CardHeader>
              <CardContent className="flex justify-center">
                <LoadingSpinner size="lg" />
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

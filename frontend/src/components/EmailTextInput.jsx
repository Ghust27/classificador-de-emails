import { useEffect, useState } from "react"
import { Textarea } from "./ui/textarea"
import { Card } from "./ui/card"
import { cn } from "../lib/utils"

const MAX_CHARACTERS = 800

export function EmailTextInput({
  value,
  onChange,
  disabled = false,
}) {
  const [characterCount, setCharacterCount] = useState(value.length)

  useEffect(() => {
    setCharacterCount(value.length)
  }, [value])

  const handleChange = (e) => {
    const newValue = e.target.value
    if (newValue.length <= MAX_CHARACTERS) {
      setCharacterCount(newValue.length)
      onChange(newValue)
    }
  }

  const isNearLimit = characterCount > MAX_CHARACTERS * 0.9
  const isAtLimit = characterCount >= MAX_CHARACTERS

  return (
    <Card className="p-4">
      <div className="space-y-2">
        <Textarea
          value={value}
          onChange={handleChange}
          disabled={disabled}
          placeholder="Cole ou digite o conteúdo do email aqui..."
          className="min-h-[200px] resize-y"
          maxLength={MAX_CHARACTERS}
        />
        <div className="flex justify-between items-center text-xs">
          <span className="text-muted-foreground">Digite ou cole o texto do email</span>
          <span
            className={cn(
              "font-medium",
              isAtLimit && "text-destructive",
              isNearLimit && !isAtLimit && "text-amber-600",
              !isNearLimit && "text-muted-foreground"
            )}
          >
            {characterCount} / {MAX_CHARACTERS} caracteres
          </span>
        </div>
      </div>
    </Card>
  )
}

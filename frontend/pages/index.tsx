import { useState } from 'react'
import UploadSection from '../components/UploadSection'
import OutputSection from '../components/OutputSection'
import Header from '../components/Header'

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [outputs, setOutputs] = useState<any>(null)

  const handleUploadComplete = (id: string) => {
    setSessionId(id)
    setIsProcessing(true)
  }

  const handleProcessingComplete = (files: any) => {
    setOutputs(files)
    setIsProcessing(false)
  }

  const handleReset = () => {
    setSessionId(null)
    setIsProcessing(false)
    setOutputs(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />
      
      <main className="container mx-auto px-4 py-12 max-w-6xl">
        {!sessionId && !outputs && (
          <UploadSection onUploadComplete={handleUploadComplete} />
        )}
        
        {(isProcessing || outputs) && (
          <OutputSection
            sessionId={sessionId}
            isProcessing={isProcessing}
            outputs={outputs}
            onProcessingComplete={handleProcessingComplete}
            onReset={handleReset}
          />
        )}
      </main>
    </div>
  )
}

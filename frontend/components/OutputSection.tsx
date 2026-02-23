import { useEffect, useState } from 'react'
import axios from 'axios'
import OutputCard from './OutputCard'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface OutputSectionProps {
  sessionId: string | null
  isProcessing: boolean
  outputs: any
  onProcessingComplete: (files: any) => void
  onReset: () => void
}

export default function OutputSection({
  sessionId,
  isProcessing,
  outputs,
  onProcessingComplete,
  onReset
}: OutputSectionProps) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    if (!isProcessing || !sessionId) return

    const checkStatus = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/status/${sessionId}`)
        
        if (response.data.status === 'completed') {
          onProcessingComplete(response.data.files)
        } else {
          // Simulate progress
          setProgress(prev => Math.min(prev + 5, 90))
          setTimeout(checkStatus, 2000)
        }
      } catch (error) {
        console.error('Error checking status:', error)
        setTimeout(checkStatus, 2000)
      }
    }

    checkStatus()
  }, [sessionId, isProcessing])

  if (isProcessing) {
    return (
      <div className="max-w-2xl mx-auto text-center">
        <div className="bg-white rounded-2xl shadow-lg p-12">
          <div className="w-24 h-24 mx-auto mb-6 relative">
            <div className="absolute inset-0 bg-gradient-to-br from-primary to-secondary rounded-full animate-pulse"></div>
            <div className="absolute inset-2 bg-white rounded-full flex items-center justify-center">
              <svg className="w-12 h-12 text-primary animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
          </div>
          
          <h2 className="text-2xl font-semibold text-gray-800 mb-2">
            Processing Your Video
          </h2>
          <p className="text-gray-600 mb-6">
            This may take 20-60 seconds depending on video length
          </p>
          
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-500"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      </div>
    )
  }

  if (outputs) {
    return (
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-2">
            Your Files Are Ready!
          </h2>
          <p className="text-gray-600">
            Download your processed files below
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <OutputCard
            title="Video (No Audio)"
            description="Silent version of your uploaded video"
            icon="video"
            downloadUrl={outputs.video_no_audio}
            filename="video_no_audio.mp4"
            fileType="video"
          />
          
          <OutputCard
            title="Full Audio"
            description="Complete original audio from the video"
            icon="audio"
            downloadUrl={outputs.full_audio}
            filename="full_audio.mp3"
            fileType="audio"
          />
          
          <OutputCard
            title="Music Only"
            description="Audio without vocals"
            icon="music"
            downloadUrl={outputs.music_only}
            filename="music_only.mp3"
            fileType="audio"
          />
          
          <OutputCard
            title="Vocals Only"
            description="Extracted voice track"
            icon="microphone"
            downloadUrl={outputs.vocals_only}
            filename="vocals_only.mp3"
            fileType="audio"
          />
        </div>

        <div className="text-center">
          <button
            onClick={onReset}
            className="px-8 py-3 bg-white text-primary border-2 border-primary rounded-lg font-medium hover:bg-primary hover:text-white transition-all"
          >
            Process Another Video
          </button>
        </div>
      </div>
    )
  }

  return null
}

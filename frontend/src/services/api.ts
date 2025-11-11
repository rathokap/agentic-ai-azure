import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

interface QueryResponse {
  response: string
  status: string
  thread_id: string
  sentiment?: string
  category?: string
}

export const sendMessage = async (query: string, userId: string): Promise<string> => {
  try {
    // Use new JSON-based /query endpoint (production-ready)
    const response = await axios.post<QueryResponse>(`${API_BASE_URL}/query`, {
      message: query,
      thread_id: userId
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 60000  // 60 second timeout for AI processing
    })

    return response.data.response || 'No response from agent'
  } catch (error) {
    console.error('API Error:', error)
    
    // Try fallback to legacy endpoint if new one fails
    try {
      console.log('Trying legacy endpoint...')
      const fallbackResponse = await axios.post(`${API_BASE_URL}/support-agent`, null, {
        params: {
          query,
          uid: userId
        },
        timeout: 60000
      })
      return fallbackResponse.data.result || 'No response from agent'
    } catch (fallbackError) {
      console.error('Fallback API Error:', fallbackError)
      throw new Error('Failed to get response from support agent')
    }
  }
}

// Health check function for monitoring
export const checkHealth = async (): Promise<boolean> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`, {
      timeout: 10000
    })
    return response.status === 200 && response.data.status === 'healthy'
  } catch (error) {
    console.error('Health check failed:', error)
    return false
  }
}

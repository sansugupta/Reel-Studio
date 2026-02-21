import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null)
  const [token, setToken] = useState('')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [error, setError] = useState('')

  const fetchStats = async (authToken: string) => {
    try {
      const response = await axios.get(`${API_URL}/api/admin/stats`, {
        headers: { Authorization: `Bearer ${authToken}` }
      })
      setStats(response.data)
      setIsAuthenticated(true)
      setError('')
    } catch (err: any) {
      setError('Authentication failed')
      setIsAuthenticated(false)
    }
  }

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    localStorage.setItem('admin_token', token)
    fetchStats(token)
  }

  useEffect(() => {
    const savedToken = localStorage.getItem('admin_token')
    if (savedToken) {
      setToken(savedToken)
      fetchStats(savedToken)
    }
  }, [])

  useEffect(() => {
    if (isAuthenticated) {
      const interval = setInterval(() => {
        fetchStats(token)
      }, 5000)
      return () => clearInterval(interval)
    }
  }, [isAuthenticated, token])

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md w-full">
          <h1 className="text-2xl font-bold text-gray-800 mb-6 text-center">Admin Login</h1>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Admin Token
              </label>
              <input
                type="password"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                placeholder="Enter admin token"
              />
            </div>
            {error && (
              <p className="text-red-600 text-sm">{error}</p>
            )}
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-primary to-secondary text-white py-3 rounded-lg font-medium hover:shadow-lg transition-all"
            >
              Login
            </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Reel-Studio Dashboard</h1>
          <button
            onClick={() => {
              localStorage.removeItem('admin_token')
              setIsAuthenticated(false)
            }}
            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
          >
            Logout
          </button>
        </div>

        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Total Uploads"
              value={stats.total_uploads}
              icon="📤"
              color="blue"
            />
            <StatCard
              title="Total Downloads"
              value={stats.total_downloads}
              icon="📥"
              color="green"
            />
            <StatCard
              title="Currently Processing"
              value={stats.current_processing}
              icon="⚙️"
              color="yellow"
            />
            <StatCard
              title="Today's Uploads"
              value={stats.uploads_by_date[new Date().toISOString().split('T')[0]] || 0}
              icon="📊"
              color="purple"
            />
          </div>
        )}

        {stats && stats.uploads_by_date && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload History</h2>
            <div className="space-y-2">
              {Object.entries(stats.uploads_by_date)
                .sort(([a], [b]) => b.localeCompare(a))
                .slice(0, 10)
                .map(([date, count]: [string, any]) => (
                  <div key={date} className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">{date}</span>
                    <span className="font-semibold text-gray-800">{count} uploads</span>
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function StatCard({ title, value, icon, color }: any) {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    yellow: 'from-yellow-500 to-yellow-600',
    purple: 'from-purple-500 to-purple-600',
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className={`w-12 h-12 bg-gradient-to-br ${colors[color]} rounded-lg flex items-center justify-center text-2xl mb-4`}>
        {icon}
      </div>
      <h3 className="text-gray-600 text-sm font-medium mb-1">{title}</h3>
      <p className="text-3xl font-bold text-gray-800">{value}</p>
    </div>
  )
}

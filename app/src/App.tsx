import React from 'react';
import Chatbot from './Chatbot';
import { DataTable } from './DataTable';
import { columns } from './components/ui/columns';

function App() {
  const [data, setData] = React.useState<any[]>([])
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    setLoading(true)
    const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/customers`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch')
        return res.json()
      })
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="">
      <header>
        <h1 className="text-2xl font-bold">AI CRM</h1>
      </header>

      <main className="grid grid-cols-[1fr_400px]">
        <div className="overflow-x-auto w-full">
          {loading ? (
            <div>Loading...</div>
          ) : error ? (
            <div className="text-red-500">{error}</div>
          ) : (
            <DataTable columns={columns} data={data} />
          )}
        </div>
        <Chatbot onFilterResult={setData} />
      </main>
    </div>
  )
}

export default App


import Chatbot from './Chatbot'
import { DataTable } from './DataTable'
import { columns } from './components/ui/columns'
import { customers } from './data/mock-data'

function App() {
  return (
    <div className="">
      <header>
        <h1 className="text-2xl font-bold">AI CRM</h1>
      </header>

      <main className="grid grid-cols-[1fr_400px]">
        <div className="overflow-x-auto w-full">
          <DataTable columns={columns} data={customers} />
        </div>
        <Chatbot />
      </main>
    </div>
  )
}

export default App

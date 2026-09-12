import { Wrench } from 'lucide-react'
import { tools } from '../data/profile'

export default function Tools() {
  return (
    <section id="tools" className="card p-6 sm:p-8">
      <div className="mb-4 flex items-center gap-2">
        <Wrench size={14} className="text-zinc-500" />
        <h2 className="section-title">Tools &amp; Technologies</h2>
      </div>
      <div className="flex flex-wrap gap-2">
        {tools.map((t) => (
          <span key={t} className="badge">
            <span className="h-1.5 w-1.5 rounded-full bg-zinc-500" />
            {t}
          </span>
        ))}
      </div>
    </section>
  )
}

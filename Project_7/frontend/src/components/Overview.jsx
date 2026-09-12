import { User } from 'lucide-react'
import { overview } from '../data/profile'

export default function Overview() {
  return (
    <section id="overview" className="card p-6 sm:p-8">
      <div className="mb-4 flex items-center gap-2">
        <User size={14} className="text-zinc-500" />
        <h2 className="section-title">Overview</h2>
      </div>
      <div className="space-y-4 text-[15px] leading-relaxed text-zinc-300">
        {overview.map((p) => (
          <p key={p}>{p}</p>
        ))}
      </div>
    </section>
  )
}

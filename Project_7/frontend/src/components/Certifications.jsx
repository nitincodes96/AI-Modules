import { Award } from 'lucide-react'
import { certifications } from '../data/profile'

export default function Certifications() {
  return (
    <section id="certifications" className="card p-6 sm:p-8">
      <div className="mb-4 flex items-center gap-2">
        <Award size={14} className="text-zinc-500" />
        <h2 className="section-title">Certifications</h2>
      </div>
      <ul className="space-y-3">
        {certifications.map((c) => (
          <li
            key={c.name}
            className="flex items-center gap-4 rounded-2xl border border-zinc-800/80 bg-zinc-950/40 p-4"
          >
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-amber-500/30 bg-amber-500/10 text-amber-300">
              <Award size={18} />
            </div>
            <div>
              <p className="font-medium text-white">{c.name}</p>
              <p className="text-sm text-zinc-400">{c.issuer}</p>
            </div>
          </li>
        ))}
      </ul>
    </section>
  )
}

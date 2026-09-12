import { GraduationCap } from 'lucide-react'
import { education } from '../data/profile'

export default function Education() {
  return (
    <section id="education" className="card p-6 sm:p-8">
      <div className="mb-4 flex items-center gap-2">
        <GraduationCap size={14} className="text-zinc-500" />
        <h2 className="section-title">Education</h2>
      </div>
      <ul className="space-y-4">
        {education.map((e) => (
          <li
            key={e.institution}
            className="flex flex-col gap-1 rounded-2xl border border-zinc-800/80 bg-zinc-950/40 p-4 sm:flex-row sm:items-start sm:justify-between"
          >
            <div>
              <p className="font-medium text-white">{e.institution}</p>
              <p className="text-sm text-zinc-400">{e.degree}</p>
            </div>
            <span className="shrink-0 text-xs tabular-nums text-zinc-500">{e.period}</span>
          </li>
        ))}
      </ul>
    </section>
  )
}

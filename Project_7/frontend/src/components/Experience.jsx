import { Briefcase } from 'lucide-react'
import { experience } from '../data/profile'

export default function Experience() {
  return (
    <section id="experience" className="card p-6 sm:p-8">
      <div className="mb-4 flex items-center gap-2">
        <Briefcase size={14} className="text-zinc-500" />
        <h2 className="section-title">Experience</h2>
      </div>
      <ol className="relative space-y-6 border-l border-zinc-800 pl-6">
        {experience.map((x) => (
          <li key={`${x.company}-${x.period}`} className="relative">
            <span className="absolute -left-[31px] top-1.5 h-2.5 w-2.5 rounded-full border-2 border-zinc-900 bg-zinc-400" />
            <div className="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="font-medium text-white">{x.role}</p>
                <p className="text-sm text-zinc-400">{x.company}</p>
              </div>
              <span className="shrink-0 text-xs tabular-nums text-zinc-500">{x.period}</span>
            </div>
            <p className="mt-2 text-sm leading-relaxed text-zinc-300">{x.summary}</p>
          </li>
        ))}
      </ol>
    </section>
  )
}

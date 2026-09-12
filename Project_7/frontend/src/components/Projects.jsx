import { FolderGit2, ExternalLink } from 'lucide-react'
import { GithubIcon } from './BrandIcons'
import { projects } from '../data/profile'

function Preview({ name, accent }) {
  // Gradient "screenshot" placeholder — swap for a real image via <img> when available.
  return (
    <div
      className={`relative flex h-36 items-end overflow-hidden rounded-2xl border border-zinc-800/80 bg-gradient-to-br ${accent} bg-zinc-950`}
      aria-hidden="true"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(255,255,255,0.06),transparent_45%)]" />
      <div className="absolute left-4 top-4 flex gap-1.5">
        <span className="h-2 w-2 rounded-full bg-zinc-600" />
        <span className="h-2 w-2 rounded-full bg-zinc-600" />
        <span className="h-2 w-2 rounded-full bg-zinc-600" />
      </div>
      <span className="p-4 text-lg font-semibold tracking-tight text-white/90">{name}</span>
    </div>
  )
}

export default function Projects() {
  return (
    <section id="projects" className="card p-6 sm:p-8">
      <div className="mb-4 flex items-center gap-2">
        <FolderGit2 size={14} className="text-zinc-500" />
        <h2 className="section-title">Projects</h2>
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        {projects.map((p) => (
          <article
            key={p.name}
            className="group flex flex-col rounded-2xl border border-zinc-800/80 bg-zinc-950/40 p-3 transition-colors hover:border-zinc-700"
          >
            <Preview name={p.name} accent={p.accent} />
            <div className="flex flex-1 flex-col px-1 pt-3">
              <h3 className="font-medium text-white">{p.name}</h3>
              <p className="text-xs text-zinc-500">{p.tagline}</p>
              <p className="mt-2 text-sm leading-relaxed text-zinc-300">{p.description}</p>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {p.stack.map((s) => (
                  <span
                    key={s}
                    className="rounded-md border border-zinc-800 bg-zinc-900 px-1.5 py-0.5 text-[11px] text-zinc-400"
                  >
                    {s}
                  </span>
                ))}
              </div>
              <div className="mt-4 flex gap-2">
                {p.live ? (
                  <a
                    href={p.live}
                    target="_blank"
                    rel="noreferrer"
                    className="btn-primary !px-3 !py-1.5 !text-xs"
                  >
                    <ExternalLink size={13} /> Live
                  </a>
                ) : (
                  <span
                    className="btn-ghost !px-3 !py-1.5 !text-xs cursor-not-allowed opacity-50"
                    title="Live link coming soon"
                  >
                    <ExternalLink size={13} /> Live
                  </span>
                )}
                <a
                  href={p.repo}
                  target="_blank"
                  rel="noreferrer"
                  className="btn-ghost !px-3 !py-1.5 !text-xs"
                >
                  <GithubIcon size={13} /> Code
                </a>
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}

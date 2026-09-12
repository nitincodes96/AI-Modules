import { Download, Mail } from 'lucide-react'
import { profile } from '../data/profile'

export default function Hero() {
  const initials = profile.name
    .split(' ')
    .map((w) => w[0])
    .slice(0, 2)
    .join('')

  return (
    <section id="hero" className="card p-6 sm:p-8 animate-fade-up">
      <div className="flex flex-col gap-6 sm:flex-row sm:items-center">
        {/* Avatar with online status */}
        <div className="relative w-24 shrink-0">
          <div className="flex h-24 w-24 items-center justify-center rounded-full border border-zinc-700/80 bg-gradient-to-br from-zinc-700 to-zinc-900 text-2xl font-semibold text-zinc-100 shadow-glow">
            {initials}
          </div>
          <span className="absolute bottom-1.5 right-1.5 flex h-4 w-4">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
            <span className="relative inline-flex h-4 w-4 rounded-full border-2 border-zinc-900 bg-emerald-400" />
          </span>
        </div>

        <div className="flex-1">
          <p className="mb-1 text-xs font-medium uppercase tracking-[0.2em] text-zinc-500">
            Hello, I&apos;m
          </p>
          <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            {profile.name}
          </h1>
          <p className="mt-1 text-base text-zinc-400">{profile.title}</p>

          <div className="mt-5 flex flex-wrap gap-3">
            <a href={profile.resumeUrl} download className="btn-primary">
              <Download size={16} />
              Download Resume
            </a>
            <a href="#contact" className="btn-ghost">
              <Mail size={16} />
              Get in Touch
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}

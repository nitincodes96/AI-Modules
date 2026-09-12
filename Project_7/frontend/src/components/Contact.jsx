import { Mail, Phone, ArrowUpRight, Send } from 'lucide-react'
import { GithubIcon, LinkedinIcon } from './BrandIcons'
import { profile } from '../data/profile'

const rows = [
  { icon: Mail, label: 'Email', value: profile.email, href: `mailto:${profile.email}` },
  { icon: Phone, label: 'Phone', value: profile.phone, href: `tel:${profile.phone.replace(/\s/g, '')}` },
  {
    icon: LinkedinIcon,
    label: 'LinkedIn',
    value: profile.linkedin.replace(/^https?:\/\//, ''),
    href: profile.linkedin,
    external: true,
  },
  {
    icon: GithubIcon,
    label: 'GitHub',
    value: profile.github.replace(/^https?:\/\//, ''),
    href: profile.github,
    external: true,
  },
]

export default function Contact() {
  return (
    <section id="contact" className="card p-6 sm:p-8">
      <div className="mb-4 flex items-center gap-2">
        <Send size={14} className="text-zinc-500" />
        <h2 className="section-title">Contact</h2>
      </div>
      <p className="mb-5 text-sm text-zinc-400">
        Open to full-time roles, freelance work and interesting collaborations. The fastest way to
        reach me is email.
      </p>
      <ul className="divide-y divide-zinc-800/80 overflow-hidden rounded-2xl border border-zinc-800/80 bg-zinc-950/40">
        {rows.map(({ icon: Icon, label, value, href, external }) => (
          <li key={label}>
            <a
              href={href}
              target={external ? '_blank' : undefined}
              rel={external ? 'noreferrer' : undefined}
              className="group flex items-center gap-4 px-4 py-3.5 transition-colors hover:bg-zinc-900/80"
            >
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-zinc-800 bg-zinc-900 text-zinc-400 group-hover:text-white">
                <Icon size={16} />
              </span>
              <span className="flex-1">
                <span className="block text-xs text-zinc-500">{label}</span>
                <span className="block text-sm text-zinc-200">{value}</span>
              </span>
              <ArrowUpRight
                size={16}
                className="text-zinc-600 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-zinc-300"
              />
            </a>
          </li>
        ))}
      </ul>

      <div className="divider mt-8" />
      <footer className="flex flex-col items-center justify-between gap-2 pt-5 text-xs text-zinc-500 sm:flex-row">
        <span>{profile.copyright}</span>
        <span>Built with React, Tailwind &amp; FastAPI</span>
      </footer>
    </section>
  )
}

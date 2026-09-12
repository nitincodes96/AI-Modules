import { useEffect, useState } from 'react'
import { MapPin, Sun, Moon, Menu, X } from 'lucide-react'
import { profile, navLinks } from '../data/profile'

function useClock() {
  const [now, setNow] = useState(() => new Date())
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(id)
  }, [])
  return now
}

function formatTime(date) {
  // e.g. "08:34:35 pm"
  return date
    .toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
    })
    .toLowerCase()
}

export default function Navbar() {
  const now = useClock()
  const [open, setOpen] = useState(false)
  const hour = now.getHours()
  const isDay = hour >= 6 && hour < 18
  const ModeIcon = isDay ? Sun : Moon

  return (
    <header className="fixed inset-x-0 top-0 z-40">
      <div className="mx-auto max-w-3xl px-4 pt-4">
        <div className="card flex items-center justify-between gap-3 rounded-2xl px-4 py-2.5">
          {/* Location */}
          <div className="flex items-center gap-2 text-xs text-zinc-400">
            <MapPin size={14} className="text-zinc-500" />
            <span className="hidden sm:inline">{profile.location}</span>
            <span className="sm:hidden">New Delhi</span>
          </div>

          {/* Desktop links */}
          <nav className="hidden items-center gap-1 md:flex" aria-label="Primary">
            {navLinks.map((l) => (
              <a
                key={l.href}
                href={l.href}
                className="rounded-full px-3 py-1.5 text-xs font-medium text-zinc-400 transition-colors hover:bg-zinc-800/80 hover:text-white"
              >
                {l.label}
              </a>
            ))}
          </nav>

          {/* Clock */}
          <div className="flex items-center gap-2 text-xs tabular-nums text-zinc-400">
            <ModeIcon size={14} className="text-zinc-500" />
            <time dateTime={now.toISOString()}>{formatTime(now)}</time>
            <button
              type="button"
              onClick={() => setOpen((o) => !o)}
              className="ml-1 rounded-full p-1.5 text-zinc-400 hover:bg-zinc-800 hover:text-white md:hidden"
              aria-label={open ? 'Close menu' : 'Open menu'}
              aria-expanded={open}
            >
              {open ? <X size={16} /> : <Menu size={16} />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {open && (
          <nav
            className="card mt-2 grid grid-cols-2 gap-1 rounded-2xl p-2 md:hidden animate-fade-up"
            aria-label="Mobile"
          >
            {navLinks.map((l) => (
              <a
                key={l.href}
                href={l.href}
                onClick={() => setOpen(false)}
                className="rounded-xl px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800/80 hover:text-white"
              >
                {l.label}
              </a>
            ))}
          </nav>
        )}
      </div>
    </header>
  )
}

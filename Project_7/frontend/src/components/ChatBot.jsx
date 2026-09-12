import { useEffect, useRef, useState } from 'react'
import { MessageCircle, X, Send, Bot, AlertCircle } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/chat'

const WELCOME = {
  role: 'assistant',
  content:
    "Hi! I'm Nitin's AI assistant. Ask me about his projects, experience, skills, or how to get in touch.",
}

const SUGGESTIONS = ['What projects has Nitin built?', 'What is his tech stack?', 'How can I contact him?']

function Bubble({ role, content, error }) {
  const isUser = role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={[
          'max-w-[85%] whitespace-pre-wrap rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed',
          isUser
            ? 'rounded-br-md bg-zinc-100 text-zinc-900'
            : error
              ? 'rounded-bl-md border border-red-500/30 bg-red-500/10 text-red-200'
              : 'rounded-bl-md border border-zinc-800 bg-zinc-900 text-zinc-200',
        ].join(' ')}
      >
        {error && <AlertCircle size={14} className="mb-1 inline-block mr-1.5 -mt-0.5" />}
        {content}
      </div>
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="flex items-center gap-1 rounded-2xl rounded-bl-md border border-zinc-800 bg-zinc-900 px-4 py-3">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="h-1.5 w-1.5 animate-bounce rounded-full bg-zinc-400"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
    </div>
  )
}

export default function ChatBot() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([WELCOME])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const inputRef = useRef(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    if (open) inputRef.current?.focus()
  }, [open])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading, open])

  // Close on Escape
  useEffect(() => {
    if (!open) return
    const onKey = (e) => e.key === 'Escape' && setOpen(false)
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open])

  async function send(text) {
    const message = (text ?? input).trim()
    if (!message || loading) return

    // History sent to the API excludes the local welcome bubble and any error bubbles.
    const history = messages
      .filter((m) => m !== WELCOME && !m.error)
      .map(({ role, content }) => ({ role, content }))

    setMessages((m) => [...m, { role: 'user', content: message }])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, history }),
      })
      const data = await res.json().catch(() => ({}))
      if (!res.ok) {
        throw new Error(data.detail || `Server responded with ${res.status}`)
      }
      setMessages((m) => [...m, { role: 'assistant', content: data.reply }])
    } catch (err) {
      const offline = err instanceof TypeError // fetch network failure
      setMessages((m) => [
        ...m,
        {
          role: 'assistant',
          error: true,
          content: offline
            ? "I can't reach the assistant server right now. Make sure the backend is running on port 8000, or reach Nitin directly via the Contact section."
            : err.message || 'Something went wrong. Please try again.',
        },
      ])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  function onSubmit(e) {
    e.preventDefault()
    send()
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Expanded panel */}
      {open && (
        <div
          role="dialog"
          aria-label="Chat with Nitin's AI assistant"
          className="card mb-3 flex w-80 flex-col overflow-hidden rounded-3xl sm:w-96 animate-fade-up"
          style={{ height: 'min(500px, calc(100vh - 7rem))' }}
        >
          {/* Header */}
          <div className="flex items-center gap-3 border-b border-zinc-800/80 px-4 py-3">
            <div className="relative">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-zinc-600 to-zinc-800 text-white">
                <Bot size={18} />
              </div>
              <span className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full border-2 border-zinc-900 bg-emerald-400" />
            </div>
            <div className="flex-1 leading-tight">
              <p className="text-sm font-medium text-white">Nitin&apos;s Assistant</p>
              <p className="text-[11px] text-zinc-500">Usually replies instantly</p>
            </div>
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="rounded-full p-1.5 text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
              aria-label="Close chat"
            >
              <X size={16} />
            </button>
          </div>

          {/* Messages */}
          <div className="scrollbar-thin flex-1 space-y-3 overflow-y-auto px-4 py-4">
            {messages.map((m, i) => (
              <Bubble key={i} {...m} />
            ))}
            {loading && <TypingIndicator />}
            {messages.length === 1 && !loading && (
              <div className="flex flex-wrap gap-1.5 pt-1">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    type="button"
                    onClick={() => send(s)}
                    className="rounded-full border border-zinc-800 bg-zinc-900/60 px-2.5 py-1 text-[11px] text-zinc-400 transition-colors hover:border-zinc-600 hover:text-white"
                  >
                    {s}
                  </button>
                ))}
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <form
            onSubmit={onSubmit}
            className="flex items-center gap-2 border-t border-zinc-800/80 bg-zinc-950/40 px-3 py-3"
          >
            <input
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about Nitin…"
              autoComplete="off"
              maxLength={1000}
              disabled={loading}
              className="flex-1 rounded-full border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm text-zinc-100 placeholder:text-zinc-500 focus:border-zinc-600 focus:outline-none disabled:opacity-60"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-zinc-100 text-zinc-900 transition-all hover:bg-white disabled:cursor-not-allowed disabled:opacity-40"
              aria-label="Send message"
            >
              <Send size={15} />
            </button>
          </form>
        </div>
      )}

      {/* Floating action button */}
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-label={open ? 'Close chat' : 'Open chat'}
        aria-expanded={open}
        className="ml-auto flex h-14 w-14 items-center justify-center rounded-full border border-zinc-700/80 bg-zinc-100 text-zinc-900 shadow-[0_8px_30px_rgba(0,0,0,0.5)] transition-all hover:scale-105 hover:bg-white focus:outline-none focus-visible:ring-2 focus-visible:ring-zinc-400"
      >
        {open ? <X size={22} /> : <MessageCircle size={22} />}
      </button>
    </div>
  )
}

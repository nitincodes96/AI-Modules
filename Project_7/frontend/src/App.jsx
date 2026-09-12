import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Overview from './components/Overview'
import Education from './components/Education'
import Experience from './components/Experience'
import Projects from './components/Projects'
import Certifications from './components/Certifications'
import Tools from './components/Tools'
import Contact from './components/Contact'
import ChatBot from './components/ChatBot'

export default function App() {
  return (
    <div className="relative min-h-screen">
      {/* Ambient background glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 -z-10 bg-[radial-gradient(ellipse_60%_40%_at_50%_-10%,rgba(120,120,140,0.18),transparent)]"
      />

      <Navbar />

      <main className="mx-auto flex max-w-3xl flex-col gap-5 px-4 pb-24 pt-28 sm:px-6">
        <Hero />
        <Overview />
        <Education />
        <Experience />
        <Projects />
        <Certifications />
        <Tools />
        <Contact />
      </main>

      <ChatBot />
    </div>
  )
}

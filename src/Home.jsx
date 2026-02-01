export default function Home() {
  return (
    <div className="h-full flex-1 p-8 bg-secondary text-primary flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold text-heading mb-4">Hi, I'm Kody!</h1>
      <p className="text-lg text-muted mb-6 max-w-2xl text-center">
        I'm a passionate and self-driven developer with a love for AI, game development, and
        building creative tools. My portfolio showcases projects ranging from memory-reading game
        overlays and incremental games to neural network language models and modular AI text
        generators. I enjoy tackling challenging problems, learning new technologies, and turning
        ideas into working code.
      </p>
      <div className="flex flex-wrap gap-4 mb-8">
        <span className="px-3 py-1 rounded text-sm border bg-tag-background border-tag-border text-primary">
          Python
        </span>
        <span className="px-3 py-1 rounded text-sm border bg-tag-background border-tag-border text-primary">
          JavaScript
        </span>
        <span className="px-3 py-1 rounded text-sm border bg-tag-background border-tag-border text-primary">
          React
        </span>
        <span className="px-3 py-1 rounded text-sm border bg-tag-background border-tag-border text-primary">
          AI/ML
        </span>
        <span className="px-3 py-1 rounded text-sm border bg-tag-background border-tag-border text-primary">
          Lua
        </span>
        <span className="px-3 py-1 rounded text-sm border bg-tag-background border-tag-border text-primary">
          AutoHotkey v2
        </span>
        <span className="px-3 py-1 rounded text-sm border bg-tag-background border-tag-border text-primary">
          Web Dev
        </span>
      </div>
      <div className="text-md text-secondary mb-8 max-w-2xl text-center">
        <div>My recent projects include:</div>
        <ul className="list-disc list-inside mt-2 text-left">
          <li>
            <b>MLux</b> - An expansion of the multi-model framework, implementing an export system
            with four different formats and an end-to-end GUI pipeline on top of the CLI framework.
          </li>
          <li>
            <b>Multi-Model AI Text Generator</b> - A modular, extensible framework supporting
            bigram, LSTM, GRU, and transformer models, with full unit testing and
            configuration-driven design.
          </li>
          <li>
            <b>Markdown Analyzer</b> - A SaaS application for analyzing and improving markdown
            files, featuring a React frontend, Flask backend, Firebase Auth, Stripe subscription
            management, and OpenAI integration, with full testing and production deployment.
          </li>
          <li>
            <b>Elden Ring Death Counter</b> - A memory-reading overlay for tracking deaths in real
            time.
          </li>
          <li>
            <b>Bigram Language Model</b> - A character-level neural network for text generation in
            PyTorch.
          </li>
          <li>
            <b>FFXI Synthesis Tracker</b> - A Lua-based addon for tracking crafting stats in Final
            Fantasy XI.
          </li>
          <li>
            <b>Ant Swarm</b> - A text-based incremental game built from scratch in JavaScript.
          </li>
        </ul>
      </div>
      <div className="flex gap-4">
        <a
          href={`${import.meta.env.BASE_URL}Resume.pdf`}
          className="bg-stone-600 hover:bg-stone-700 text-white px-4 py-2 rounded border border-stone-500 shadow-lg"
          target="_blank"
          rel="noopener noreferrer"
        >
          Resume
        </a>
        <a
          href="https://github.com/Yosna"
          className="bg-zinc-800 hover:bg-zinc-900 text-white px-4 py-2 rounded border border-zinc-500 shadow-lg"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub
        </a>
        <a
          href="https://www.linkedin.com/in/kody-james-75b976362/"
          className="bg-blue-400 hover:bg-blue-500 text-white px-4 py-2 rounded border border-blue-300 shadow-lg"
          target="_blank"
          rel="noopener noreferrer"
        >
          LinkedIn
        </a>
        <a
          href="mailto:kodyjames.yosna@gmail.com"
          className="bg-rose-600 hover:bg-rose-700 text-white px-4 py-2 rounded border border-rose-500 shadow-lg"
        >
          Email
        </a>
      </div>
    </div>
  );
}

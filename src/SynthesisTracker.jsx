import * as displayUtils from './utils/displayUtils';
import lua from 'react-syntax-highlighter/dist/esm/languages/prism/lua';

displayUtils.SyntaxHighlighter.registerLanguage('lua', lua);

export default function SynthesisTracker() {
  const { selectedFile, setSelectedFile, fileContent } =
    displayUtils.useProjectFile('SynthesisTracker');

  const isMarkdown = selectedFile.endsWith('.md');
  const theme = displayUtils.useThemeMode();
  const syntaxStyles = displayUtils.syntaxStyles;
  const syntaxStyle = syntaxStyles[theme] || syntaxStyles.light;

  return (
    <div className="flex flex-col lg:flex-row h-full w-full bg-primary text-primary">
      <div className="flex-1 p-8 bg-primary text-primary">
        <h1 className="text-3xl font-bold text-heading mb-4">FFXI Synthesis Tracker</h1>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Overview:</h2>
        <p className="mb-4 leading-relaxed text-muted">
          FFXI Synthesis Tracker is a Windower addon for Final Fantasy XI. It is a tool designed to
          help players keep track of their crafting (synthesis) activities. It provides an easy way
          to monitor recipes, materials, and success rates, streamlining the crafting process and
          helping players optimize their synthesis sessions.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Why I Built It</h2>
        <p className="mb-4 leading-relaxed text-muted">
          I enjoy keeping track of numbers and stats for things, and I knew a synthesis tracker
          would be genuinely useful for my gameplay. Beyond that, I wanted a new programming
          challenge to help me learn and improve my skills. Building this addon was a fun way to
          learn more while also creating something useful for myself.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">How It Works</h2>
        <ul className="list-disc list-inside mb-4 text-muted leading-relaxed">
          <li>Hooks into the game using Lua scripting to monitor synthesis events in real time.</li>
          <li>
            Records each synthesis attempt, including recipe, materials used, and outcome
            (success/failure).
          </li>
          <li>Tracks materials used/lost and calculates gil spent/earned in real time.</li>
          <li>
            Displays a summary of recent synths, success rates, materials consumed, costs, and
            profit.
          </li>
          <li>
            Auto-exports synthesis results to a log file for lifetime stats and profit tracking.
          </li>
          <li>Allows reading of previously exported results in-game.</li>
          <li>Allows for easy filtering and searching of past synthesis attempts.</li>
        </ul>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">What I Learned</h2>
        <p className="mb-4 leading-relaxed text-muted">
          Through this project, I learned a lot about Lua scripting, event-driven programming, and
          how to interface with FFXI's addon system. I also gained experience in designing
          user-friendly tools for gamers and handling real-time data updates efficiently.
        </p>
        <p className="mb-6 text-sm text-secondary italic">
          Initial project duration:: ~1.5 weeks (December 14<sup>th</sup> - December 22<sup>nd</sup>
          , 2020)
        </p>
        <a
          href="https://github.com/Yosna/ffxi-synthesis-tracker"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-400 hover:underline"
        >
          View on GitHub
        </a>
      </div>
      <div className="flex-1 p-8 bg-secondary border-l border-code flex justify-center items-center">
        <div className="w-full h-full flex flex-col">
          <div className="flex items-center justify-between mb-2 ml-8 mr-8">
            <label htmlFor="fileSelect" className="font-medium text-xl text-heading">
              Select a file to view:
            </label>
            <select
              id="fileSelect"
              className="w-[33%] ml-2 border px-2 py-1 rounded bg-accent text-primary border-code"
              value={selectedFile}
              onChange={(e) => setSelectedFile(e.target.value)}
            >
              <option value="README.md">&#x250C;&#x2500; README.md</option>
              <optgroup label="&#x2514;&#x2500; /SynthesisTracker">
                <option value="SynthesisTracker/synthesistracker.lua">
                  &#x2514;&#x2500; synthesistracker.lua
                </option>
              </optgroup>
            </select>
          </div>
          <div className="w-full h-full overflow-auto">
            {isMarkdown ? (
              <div className="prose prose-invert leading-snug max-w-[96%]">
                <displayUtils.ReactMarkdown>{fileContent}</displayUtils.ReactMarkdown>
              </div>
            ) : (
              <displayUtils.SyntaxHighlighter
                language={displayUtils.getLanguageFromFilename(selectedFile)}
                style={syntaxStyle}
                showLineNumbers={true}
                lineNumberStyle={{
                  minWidth: '2em',
                  textAlign: 'right',
                  padding: '0 8px 0 0',
                }}
                className="syntax-highlighter text-sm"
              >
                {fileContent}
              </displayUtils.SyntaxHighlighter>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

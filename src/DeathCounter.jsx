import * as displayUtils from './utils/displayUtils';
import autohotkey from 'react-syntax-highlighter/dist/esm/languages/prism/autohotkey';

displayUtils.SyntaxHighlighter.registerLanguage('autohotkey', autohotkey);

export default function DeathCounter() {
  const { selectedFile, setSelectedFile, fileContent } =
    displayUtils.useProjectFile('DeathCounter');

  const isMarkdown = selectedFile.endsWith('.md');
  const theme = displayUtils.useThemeMode();
  const syntaxStyles = displayUtils.syntaxStyles;
  const syntaxStyle = syntaxStyles[theme] || syntaxStyles.light;

  return (
    <div className="flex flex-col lg:flex-row h-full w-full bg-primary text-primary">
      <div className="flex-1 p-8 bg-primary text-primary">
        <h1 className="text-3xl font-bold text-heading mb-4">Elden Ring Death Counter</h1>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Overview:</h2>
        <p className="mb-4 leading-relaxed text-muted">
          This project is death counter for Elden Ring, designed to track and display the number of
          times a player has died in the game. Unlike other mods that require you to tab out to a
          separate window, this tool overlays the death count directly, making it easily accessible
          while playing.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Why I Built It</h2>
        <p className="mb-4 leading-relaxed text-muted">
          As a huge fan of FromSoftware games, I wanted a more seamless way to keep track of my
          deaths in Elden Ring. I tried a third-party mod, but it only displayed the count in a
          separate window, which wasn't ideal. My initial goal was just to overlay the death count
          from a text file, but as I dug deeper, I realized I could pull the value directly from the
          game's memory using AutoHotkey. This project became a way for me to challenge myself and
          learn new skills, especially around memory reading and system-level programming.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">How It Works</h2>
        <ul className="list-disc list-inside mb-4 text-muted leading-relaxed">
          <li>
            Monitors the game's memory to find and read the current death count using AHK v2
            scripts.
          </li>
          <li>
            Uses pointers and offsets discovered through Cheat Engine to locate the correct memory
            address.
          </li>
          <li>
            Displays the death count as an overlay, so you never have to leave the game window.
          </li>
          <li>
            Includes modular scripts for handling memory access, settings, and utility functions.
          </li>
        </ul>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">What I Learned</h2>
        <p className="mb-4 leading-relaxed text-muted">
          This was the most challenging programming project I had tackled at the time. I learned a
          ton about reading process memory, working with pointers and offsets, and making DLL calls
          from AHK. I also spent a lot of time experimenting with things I didn't end up using, like
          reading binaries with a hex editor. Overall, I gained a much deeper understanding of how
          games store data in memory and how to interact with that data programmatically.
        </p>
        <p className="mb-6 text-sm text-secondary italic">
          Initial project duration:: ~2 weeks (April 12<sup>th</sup> - April 26<sup>th</sup>, 2025)
        </p>
        <a
          href="https://github.com/Yosna/elden-ring-death-counter"
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
              <option value="deathcounter.ahk">&#x251C;&#x2500; deathcounter.ahk</option>
              <option value="gamedata.ahk">&#x251C;&#x2500; gamedata.ahk</option>
              <option value="memory.ahk">&#x251C;&#x2500; memory.ahk</option>
              <option value="settings.ahk">&#x251C;&#x2500; settings.ahk</option>
              <option value="utils.ahk">&#x251C;&#x2500; utils.ahk</option>
              <option value="constants.ahk">&#x2514;&#x2500; constants.ahk</option>
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

import * as displayUtils from './utils/displayUtils';
import javascript from 'react-syntax-highlighter/dist/esm/languages/prism/javascript';

displayUtils.SyntaxHighlighter.registerLanguage('javascript', javascript);

export default function AntSwarm() {
  const { selectedFile, setSelectedFile, fileContent } = displayUtils.useProjectFile('AntSwarm');

  const isMarkdown = selectedFile.endsWith('.md');
  const theme = displayUtils.useThemeMode();
  const syntaxStyles = displayUtils.syntaxStyles;
  const syntaxStyle = syntaxStyles[theme] || syntaxStyles.light;

  return (
    <div className="flex flex-col lg:flex-row h-full w-full bg-primary text-primary">
      <div className="flex-1 p-8 bg-primary text-primary">
        <h1 className="text-3xl font-bold text-heading mb-4">Ant Swarm</h1>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Overview:</h2>
        <p className="mb-4 leading-relaxed text-muted">
          Ant Swarm is a text-based incremental game built from scratch using HTML, CSS, and vanilla
          JavaScript. The game features a modular architecture, upgrade system, save/load
          functionality, and dynamic production logic—all without external frameworks. It's designed
          to be a fully functional idle game that demonstrates core front-end programming skills.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Why I Built It</h2>
        <p className="mb-4 leading-relaxed text-muted">
          I've always really liked incremental games since they're such a simple concept that you
          can get so much enjoyment out of. When I decided to start building a portfolio, I thought
          an incremental game would be a simpler project to start with and a fun way to learn more
          about web development.
        </p>
        <p className="mb-4 leading-relaxed text-muted">
          The decision to make it text-based was intentional, as I've always felt those types of
          incrementals stand out the most with the focus being centered on the progression systems.
          Mine Defense was the incremental that inspired me, with some other notable ones being
          Candy Box, Kittens Game, A Dark Room, Swarm Simulator (original), Crank, and Antimatter
          Dimensions. I wanted to follow what felt like tradition.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">How It Works</h2>
        <ul className="list-disc list-inside mb-4 text-muted leading-relaxed">
          <li>Uses modular JavaScript to manage game logic, upgrades, and UI.</li>
          <li>Players accumulate resources and unlock upgrades that boost production.</li>
          <li>Features a save/load system (including file export/import and clipboard copy).</li>
          <li>Upgrade buttons have tooltips, cost scaling, and visual feedback.</li>
          <li>Includes settings and stat menus with modal handling.</li>
          <li>Tracks offline progression and dynamically updates production rates.</li>
        </ul>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">What I Learned</h2>
        <p className="mb-4 leading-relaxed text-muted">
          Through this project, I learned a lot about structuring JavaScript code for larger
          projects, handling persistent game state, and creating interactive UIs without relying on
          frameworks. I also gained experience with dynamic rendering, modular design, and managing
          user input and feedback in a browser environment.
        </p>
        <p className="mb-6 text-sm text-secondary italic">
          Initial project duration:: ~2 months (April 11<sup>th</sup> - June 4<sup>th</sup>, 2023)
        </p>
        <a
          href="https://github.com/Yosna/ant-swarm/tree/main"
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
              <option value="index.html">&#x251C;&#x2500; index.html</option>
              <option value="styles.css">&#x251C;&#x2500; styles.css</option>
              <option value="index.js">&#x251C;&#x2500; index.js</option>
              <option value="game.js">&#x251C;&#x2500; game.js</option>
              <option value="forage.js">&#x251C;&#x2500; forage.js</option>
              <option value="colonies.js">&#x251C;&#x2500; colonies.js</option>
              <option value="init.js">&#x251C;&#x2500; init.js</option>
              <option value="config.js">&#x2514;&#x2500; config.js</option>
              <optgroup label="&#x2514;&#x2500; /classes">
                <option value="classes/ant.js">&#x251C;&#x2500; ant.js</option>
                <option value="classes/colony.js">&#x2514;&#x2500; colony.js</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /utilities">
                <option value="utilities/dom.js">&#x251C;&#x2500; dom.js</option>
                <option value="utilities/logger.js">&#x251C;&#x2500; logger.js</option>
                <option value="utilities/number.js">&#x251C;&#x2500; number.js</option>
                <option value="utilities/save.js">&#x251C;&#x2500; save.js</option>
                <option value="utilities/time.js">&#x2514;&#x2500; time.js</option>
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

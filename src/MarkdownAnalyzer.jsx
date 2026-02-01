import * as displayUtils from './utils/displayUtils';
import jsx from 'react-syntax-highlighter/dist/esm/languages/prism/jsx';
import tsx from 'react-syntax-highlighter/dist/esm/languages/prism/tsx';
import css from 'react-syntax-highlighter/dist/esm/languages/prism/css';
import javascript from 'react-syntax-highlighter/dist/esm/languages/prism/javascript';
import typescript from 'react-syntax-highlighter/dist/esm/languages/prism/typescript';
import python from 'react-syntax-highlighter/dist/esm/languages/prism/python';
import rehypeRaw from 'rehype-raw';

displayUtils.SyntaxHighlighter.registerLanguage('jsx', jsx);
displayUtils.SyntaxHighlighter.registerLanguage('tsx', tsx);
displayUtils.SyntaxHighlighter.registerLanguage('css', css);
displayUtils.SyntaxHighlighter.registerLanguage('javascript', javascript);
displayUtils.SyntaxHighlighter.registerLanguage('typescript', typescript);
displayUtils.SyntaxHighlighter.registerLanguage('python', python);

export default function MarkdownAnalyzer() {
  const { selectedFile, setSelectedFile, fileContent } =
    displayUtils.useProjectFile('MarkdownAnalyzer');

  const isMarkdown = selectedFile.endsWith('.md');
  const theme = displayUtils.useThemeMode();
  const syntaxStyles = displayUtils.syntaxStyles;
  const syntaxStyle = syntaxStyles[theme] || syntaxStyles.light;

  return (
    <div className="flex flex-col lg:flex-row h-full w-full bg-primary text-primary">
      <div className="w-full lg:w-1/2 px-6 py-4 bg-primary text-primary">
        <h1 className="text-3xl font-bold text-heading mb-4">Markdown Analyzer</h1>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Overview:</h2>
        <p className="mb-4 leading-relaxed text-muted">
          Markdown Analyzer is a full-stack React application for analyzing, previewing, and
          comparing Markdown documents. It provides a live editor with diff visualization,
          AI-powered analysis, and a subscription model integrated with Firebase authentication and
          Stripe.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Why I Built It</h2>
        <p className="mb-4 leading-relaxed text-muted">
          The original idea was to explore how an AI model might interact with code in a sandboxed
          environment to safely run, iterate, and refine results before returning them to the user.
          As a first step toward that idea, I started with Markdown since it was easier to
          understand and it made sense to show both the raw syntax and rendered preview. By starting
          smaller, I could implement the concept of a dual-view while building a production-ready,
          AI-centric web app with user authentication and a subscription model.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">How It Works</h2>
        <ul className="list-disc list-inside mb-4 text-muted leading-relaxed">
          <li>Markdown editor with live preview for immediate feedback.</li>
          <li>Diff viewer for side-by-side comparison of edits.</li>
          <li>AI analysis for summaries and content insights</li>
          <li>Responsive layout using TailwindCSS styling</li>
          <li>Dynamic theming with six color schemes and persistent preferences.</li>
          <li>Authenthication and billing using Firebase Auth and Stripe (currently disabled)</li>
          <li>Full-stack hosting with Firebase frontend and Render backend</li>
        </ul>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">What I Learned</h2>
        <p className="mb-4 leading-relaxed text-muted">
          This project gave me hands-on experience with building and deploying a full SaaS-style
          application. I learned how to integrate third-party services such as Firebase and Stripe
          securely, connect a frontend to a RESTful API, and how to handle sensitive data including
          secret keys and API tokens. It also taught me how to take a larger vision and break it
          down into incremental steps that could realistically be built to completion.
        </p>
        <p className="mb-6 text-sm text-secondary italic">
          Initial project duration:: ~8 weeks (June 28<sup>th</sup> - August 26<sup>th</sup>, 2025)
        </p>
        <a
          href="https://github.com/Yosna/Markdown-Analyzer"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-400 hover:underline"
        >
          View on GitHub
        </a>
        {' | '}
        <a
          href="https://markdown-analyzer.web.app"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-400 hover:underline"
        >
          View Live App
        </a>
      </div>
      <div className="w-full lg:w-1/2 px-6 py-4 bg-secondary border-l border-code">
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
              <optgroup label="&#x2514;&#x2500; /client/src">
                <option value="client/src/main.jsx">&#x251C;&#x2500; main.jsx</option>
                <option value="client/src/App.jsx">&#x251C;&#x2500; App.jsx</option>
                <option value="client/src/index.css">&#x251C;&#x2500; index.css</option>
                <option value="client/src/components.css">&#x251C;&#x2500; components.css</option>
                <option value="client/src/themes.css">&#x2514;&#x2500; themes.css</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /client/src/hooks">
                <option value="client/src//hooks/useAuth.js">&#x251C;&#x2500; useAuth.js</option>
                <option value="client/src//hooks/useTheme.js">&#x2514;&#x2500; useTheme.js</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /client/src/utils">
                <option value="client/src//utils/api.js">&#x251C;&#x2500; api.js</option>
                <option value="client/src//utils/captureImage.js">
                  &#x251C;&#x2500; captureImage.js
                </option>
                <option value="client/src//utils/constants.js">
                  &#x251C;&#x2500; constants.js
                </option>
                <option value="client/src//utils/fileUtils.js">
                  &#x251C;&#x2500; fileUtils.js
                </option>
                <option value="client/src//utils/linkCredentials.js">
                  &#x2514;&#x2500; linkCredentials.js
                </option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /client/src/lib">
                <option value="client/src//lib/firebase.js">&#x2514;&#x2500; firebase.js</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /client/src/components">
                <option value="client/src//components/AuthProvider.jsx">
                  &#x251C;&#x2500; AuthProvider.jsx
                </option>
                <option value="client/src//components/CodeEditor.jsx">
                  &#x251C;&#x2500; CodeEditor.jsx
                </option>
                <option value="client/src//components/ColorSchemes.jsx">
                  &#x251C;&#x2500; ColorSchemes.jsx
                </option>
                <option value="client/src//components/ControlPanel.jsx">
                  &#x251C;&#x2500; ControlPanel.jsx
                </option>
                <option value="client/src//components/DiffViewer.jsx">
                  &#x251C;&#x2500; DiffViewer.jsx
                </option>
                <option value="client/src//components/EditorPanel.jsx">
                  &#x251C;&#x2500; EditorPanel.jsx
                </option>
                <option value="client/src//components/MarkdownPreview.jsx">
                  &#x251C;&#x2500; MarkdownPreview.jsx
                </option>
                <option value="client/src//components/OutputPanel.jsx">
                  &#x251C;&#x2500; OutputPanel.jsx
                </option>
                <option value="client/src//components/UserAuth.jsx">
                  &#x251C;&#x2500; UserAuth.jsx
                </option>
                <option value="client/src//components/UserCard.jsx">
                  &#x251C;&#x2500; UserCard.jsx
                </option>
                <option value="client/src//components/UserPanel.jsx">
                  &#x2514;&#x2500; UserPanel.jsx
                </option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /client/src/tests">
                <option value="client/src//tests/mocks.ts">&#x251C;&#x2500; mocks.ts</option>
                <option value="client/src//tests/setup.ts">&#x251C;&#x2500; setup.ts</option>
                <option value="client/src//tests/api.test.tsx">
                  &#x251C;&#x2500; api.test.tsx
                </option>
                <option value="client/src//tests/App.test.jsx">
                  &#x251C;&#x2500; App.test.jsx
                </option>
                <option value="client/src//tests/AuthProvider.test.tsx">
                  &#x251C;&#x2500; AuthProvider.test.tsx
                </option>
                <option value="client/src//tests/captureImage.test.tsx">
                  &#x251C;&#x2500; captureImage.test.tsx
                </option>
                <option value="client/src//tests/CodeEditor.test.tsx">
                  &#x251C;&#x2500; CodeEditor.test.tsx
                </option>
                <option value="client/src//tests/ColorSchemes.test.tsx">
                  &#x251C;&#x2500; ColorSchemes.test.tsx
                </option>
                <option value="client/src//tests/ControlPanel.test.tsx">
                  &#x251C;&#x2500; ControlPanel.test.tsx
                </option>
                <option value="client/src//tests/DiffViewer.test.tsx">
                  &#x251C;&#x2500; DiffViewer.test.tsx
                </option>
                <option value="client/src//tests/EditorPanel.test.tsx">
                  &#x251C;&#x2500; EditorPanel.test.tsx
                </option>
                <option value="client/src//tests/fileUtils.test.tsx">
                  &#x251C;&#x2500; fileUtils.test.tsx
                </option>
                <option value="client/src//tests/linkCredentials.test.tsx">
                  &#x251C;&#x2500; linkCredentials.test.tsx
                </option>
                <option value="client/src//tests/MarkdownPreview.test.tsx">
                  &#x251C;&#x2500; MarkdownPreview.test.tsx
                </option>
                <option value="client/src//tests/OutputPanel.test.tsx">
                  &#x251C;&#x2500; OutputPanel.test.tsx
                </option>
                <option value="client/src//tests/UserAuth.test.tsx">
                  &#x251C;&#x2500; UserAuth.test.tsx
                </option>
                <option value="client/src//tests/UserCard.test.tsx">
                  &#x251C;&#x2500; UserCard.test.tsx
                </option>
                <option value="client/src//tests/UserPanel.test.tsx">
                  &#x251C;&#x2500; UserPanel.test.tsx
                </option>
                <option value="client/src//tests/useTheme.test.tsx">
                  &#x2514;&#x2500; useTheme.test.tsx
                </option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /server">
                <option value="server/app.py">&#x2514;&#x2500; app.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /server/tests">
                <option value="server/tests/test_app.py">&#x2514;&#x2500; test_app.py</option>
              </optgroup>
            </select>
          </div>
          <div className="w-full h-full overflow-auto">
            {isMarkdown ? (
              <div className="prose prose-invert leading-snug max-w-[96%]">
                <displayUtils.ReactMarkdown rehypePlugins={[rehypeRaw]}>
                  {fileContent}
                </displayUtils.ReactMarkdown>
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

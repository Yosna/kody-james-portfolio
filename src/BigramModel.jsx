import * as displayUtils from './utils/displayUtils';
import python from 'react-syntax-highlighter/dist/esm/languages/prism/python';

displayUtils.SyntaxHighlighter.registerLanguage('python', python);

export default function BigramModel() {
  const { selectedFile, setSelectedFile, fileContent } = displayUtils.useProjectFile('BigramModel');

  const isMarkdown = selectedFile.endsWith('.md');
  const theme = displayUtils.useThemeMode();
  const syntaxStyles = displayUtils.syntaxStyles;
  const syntaxStyle = syntaxStyles[theme] || syntaxStyles.light;

  return (
    <div className="flex flex-col lg:flex-row h-full w-full bg-primary text-primary">
      <div className="flex-1 p-8 bg-primary text-primary">
        <h1 className="text-3xl font-bold text-heading mb-4">Bigram Language Model</h1>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Overview:</h2>
        <p className="mb-4 leading-relaxed text-muted">
          This project is a simple character-level neural network built with PyTorch. It predicts
          the next character in a sequence based on the current character, learning
          character-to-character relationships from any input text. The project demonstrates
          foundational NLP concepts like embeddings, tokenization, and text generation, all in a
          minimal, easy-to-understand codebase.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Why I Built It</h2>
        <p className="mb-4 leading-relaxed text-muted">
          I have been fascinated by AI ever since early 2023, so I wanted to try and learn more
          about it to see how far I could get. Building a bigram model seemed like a great way to
          get hands-on experience with neural networks and natural language processing.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">How It Works</h2>
        <ul className="list-disc list-inside mb-4 text-muted leading-relaxed">
          <li>Reads a text file and builds a vocabulary of unique characters.</li>
          <li>Encodes the text as sequences of character indices.</li>
          <li>
            Uses a single embedding layer to learn transition probabilities between characters
            (bigram model).
          </li>
          <li>
            Trains the model using cross-entropy loss and the Adam optimizer, with early stopping to
            prevent overfitting.
          </li>
          <li>
            After training, can generate new text one character at a time, starting from a random
            seed character.
          </li>
          <li>
            All hyperparameters and training options are controlled via a single configuration
            dictionary.
          </li>
        </ul>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">What I Learned</h2>
        <p className="mb-4 leading-relaxed text-muted">
          Through this project, I learned the fundamentals of building and training neural networks
          with PyTorch, including data encoding, embedding layers, and loss computation. I also
          gained experience with text generation, model evaluation, and managing training workflows
          in Python. This project gave me a much deeper understanding of how language models work at
          a low level.
        </p>
        <p className="mb-6 text-sm text-secondary italic">
          Initial project duration:: ~9 days (May 2<sup>nd</sup> - May 11<sup>th</sup>, 2025)
        </p>
        <a
          href="https://github.com/Yosna/bigram-language-model"
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
              <option value="main.py">&#x2514;&#x2500; main.py</option>
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

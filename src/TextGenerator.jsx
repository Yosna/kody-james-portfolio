import * as displayUtils from './utils/displayUtils';
import python from 'react-syntax-highlighter/dist/esm/languages/prism/python';
import json from 'react-syntax-highlighter/dist/esm/languages/prism/json';
import rehypeRaw from 'rehype-raw';

displayUtils.SyntaxHighlighter.registerLanguage('python', python);
displayUtils.SyntaxHighlighter.registerLanguage('json', json);

export default function TextGenerator() {
  const { selectedFile, setSelectedFile, fileContent } =
    displayUtils.useProjectFile('TextGenerator');

  const isMarkdown = selectedFile.endsWith('.md');
  const theme = displayUtils.useThemeMode();
  const syntaxStyles = displayUtils.syntaxStyles;
  const syntaxStyle = syntaxStyles[theme] || syntaxStyles.light;

  return (
    <div className="flex flex-col lg:flex-row h-full w-full bg-primary text-primary">
      <div className="flex-1 p-8 bg-primary text-primary">
        <h1 className="text-3xl font-bold text-heading mb-4">Multi-Model AI Text Generator</h1>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Overview:</h2>
        <p className="mb-4 leading-relaxed text-muted">
          Multi-Model AI Text Generator is a modular, extensible text generation project built with
          PyTorch. It supports bigram, LSTM, GRU, and transformer models, allowing for
          experimentation with different neural network architectures. The project features a fully
          modular codebase, configuration-driven training, and a command-line interface for
          switching between models and behaviors.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Why I Built It</h2>
        <p className="mb-4 leading-relaxed text-muted">
          After learning the basics by building a bigram model, I wanted to keep going by
          refactoring and expanding the project into a more modular, multi-model framework. I
          decided to add this as a fifth project to my portfolio to showcase my decision-making, the
          process of turning a single script into a scalable codebase, and my ability to implement
          new features, refactor code, and add unit testing.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">How It Works</h2>
        <ul className="list-disc list-inside mb-4 text-muted leading-relaxed">
          <li>
            Loads and tokenizes text data from local files or HuggingFace datasets for training.
          </li>
          <li>
            Supports bigram, LSTM, GRU, and transformer models, selectable via CLI and
            configuration.
          </li>
          <li>Modular model registry allows easy addition of new architectures.</li>
          <li>
            Training, validation, generation, visualization, and hyperparameter optimization are all
            configurable through a single <code>config.json</code> file.
          </li>
          <li>
            Implements checkpointing, early stopping, pruning, and resumption for robust training.
          </li>
          <li>
            Includes automatic hyperparameter tuning using Optuna with pruning and warmup step
            control.
          </li>
          <li>
            Features a complete test suite with <strong>100% coverage</strong> (205 unit tests, 1050
            stmts / 0 miss).
          </li>
          <li>
            Generates text by sampling from trained models using multinomial sampling and random
            seed selection.
          </li>
        </ul>

        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">What I Learned</h2>
        <p className="mb-4 leading-relaxed text-muted">
          Through this project, I learned how to design and refactor a codebase for modularity and
          extensibility, manage multiple model architectures, and implement robust training
          workflows. I also gained experience with configuration-driven development, unit testing,
          and building a flexible CLI for machine learning experiments. This project helped me
          understand the importance of clean code organization and reproducibility in AI research.
        </p>
        <p className="mb-6 text-sm text-secondary italic">
          Initial project duration:: ~7 weeks (May 12<sup>th</sup> - June 27<sup>th</sup>, 2025)
        </p>
        <a
          href="https://github.com/Yosna/multi-model-ai-text-generator"
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
              <option value="main.py">&#x251C;&#x2500; main.py</option>
              <option value="cli.py">&#x251C;&#x2500; cli.py</option>
              <option value="library.py">&#x251C;&#x2500; library.py</option>
              <option value="training.py">&#x251C;&#x2500; training.py</option>
              <option value="tuning.py">&#x251C;&#x2500; tuning.py</option>
              <option value="visualizer.py">&#x251C;&#x2500; visualizer.py</option>
              <option value="config.json">&#x2514;&#x2500; config.json</option>
              <optgroup label="&#x2514;&#x2500; /utils">
                <option value="utils/data_utils.py">&#x251C;&#x2500; data_utils.py</option>
                <option value="utils/io_utils.py">&#x251C;&#x2500; io_utils.py</option>
                <option value="utils/model_utils.py">&#x2514;&#x2500; model_utils.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /models">
                <option value="models/registry.py">&#x251C;&#x2500; registry.py</option>
                <option value="models/base_model.py">&#x251C;&#x2500; base_model.py</option>
                <option value="models/bigram_model.py">&#x251C;&#x2500; bigram_model.py</option>
                <option value="models/lstm_model.py">&#x251C;&#x2500; lstm_model.py</option>
                <option value="models/gru_model.py">&#x251C;&#x2500; gru_model.py</option>
                <option value="models/transformer_model.py">
                  &#x251C;&#x2500; transformer_model.py
                </option>
                <option value="models/distilgpt2_model.py">
                  &#x2514;&#x2500; distilgpt2_model.py
                </option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /models/components">
                <option value="models/components/generators.py">
                  &#x2514;&#x2500; generators.py
                </option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /run">
                <option value="run/__main__.py">&#x251C;&#x2500; __main__.py</option>
                <option value="run/config.py">&#x251C;&#x2500; config.py</option>
                <option value="run/dashboard.py">&#x251C;&#x2500; dashboard.py</option>
                <option value="run/profiler.py">&#x2514;&#x2500; profiler.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /run/helpers">
                <option value="run/helpers/widgets.py">&#x2514;&#x2500; widgets.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /tests">
                <option value="tests/test_main.py">&#x251C;&#x2500; test_main.py</option>
                <option value="tests/test_cli.py">&#x251C;&#x2500; test_cli.py</option>
                <option value="tests/test_library.py">&#x251C;&#x2500; test_library.py</option>
                <option value="tests/test_training.py">&#x251C;&#x2500; test_training.py</option>
                <option value="tests/test_tuning.py">&#x251C;&#x2500; test_tuning.py</option>
                <option value="tests/test_visualizer.py">
                  &#x251C;&#x2500; test_visualizer.py
                </option>
                <option value="tests/test_data_utils.py">
                  &#x251C;&#x2500; test_data_utils.py
                </option>
                <option value="tests/test_io_utils.py">&#x251C;&#x2500; test_io_utils.py</option>
                <option value="tests/test_model_utils.py">
                  &#x2514;&#x2500; test_model_utils.py
                </option>
                <option value="tests/test_registry.py">&#x251C;&#x2500; test_registry.py</option>
                <option value="tests/test_base_model.py">
                  &#x251C;&#x2500; test_base_model.py
                </option>
                <option value="tests/test_bigram_model.py">
                  &#x251C;&#x2500; test_bigram_model.py
                </option>
                <option value="tests/test_lstm_model.py">
                  &#x251C;&#x2500; test_lstm_model.py
                </option>
                <option value="tests/test_gru_model.py">&#x251C;&#x2500; test_gru_model.py</option>
                <option value="tests/test_transformer_model.py">
                  &#x251C;&#x2500; test_transformer_model.py
                </option>
                <option value="tests/test_distilgpt2_model.py">
                  &#x251C;&#x2500; test_distilgpt2_model.py
                </option>
                <option value="tests/test_generators.py">
                  &#x251C;&#x2500; test_generators.py
                </option>
                <option value="tests/test_run__main__.py">
                  &#x251C;&#x2500; test_run__main__.py
                </option>
                <option value="tests/test_config.py">&#x251C;&#x2500; test_config.py</option>
                <option value="tests/test_config_widgets.py">
                  &#x251C;&#x2500; test_config_widgets.py
                </option>
                <option value="tests/test_dashboard.py">&#x251C;&#x2500; test_dashboard.py</option>
                <option value="tests/test_profiler.py">&#x2514;&#x2500; test_profiler.py</option>
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

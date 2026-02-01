import * as displayUtils from './utils/displayUtils';
import python from 'react-syntax-highlighter/dist/esm/languages/prism/python';
import json from 'react-syntax-highlighter/dist/esm/languages/prism/json';
import rehypeRaw from 'rehype-raw';

displayUtils.SyntaxHighlighter.registerLanguage('python', python);
displayUtils.SyntaxHighlighter.registerLanguage('json', json);

export default function MLux() {
  const { selectedFile, setSelectedFile, fileContent } =
    displayUtils.useProjectFile('MLux');

  const isMarkdown = selectedFile.endsWith('.md');
  const theme = displayUtils.useThemeMode();
  const syntaxStyles = displayUtils.syntaxStyles;
  const syntaxStyle = syntaxStyles[theme] || syntaxStyles.light;

  return (
    <div className="flex flex-col lg:flex-row h-full w-full bg-primary text-primary">
      <div className="w-full lg:w-1/2 px-6 py-4 bg-primary text-primary">
        <h1 className="text-3xl font-bold text-heading mb-4">MLux</h1>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Overview:</h2>
        <p className="mb-4 leading-relaxed text-muted">
          MLux is a modular, extensible machine learning framework built in Python and PyTorch for experimenting with different text generation architectures. It supports bigram, LSTM, GRU, and transformer models with a unified, configuration-driven workflow. The project emphasizes clean architecture, reproducibility, and testability, allowing new models, datasets, and training behaviors to be added without modifying existing core logic.
          </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">Why I Built It</h2>
        <p className="mb-4 leading-relaxed text-muted">
          I enjoy expanding on existing projects, so after building a CLI-based multi-model framework, I wanted to explore how I would evolve it into a small experimentation platform usable by a wider range of people. This iteration focuses on improving usability through a pipeline GUI, experimenting with multiple export formats, and testing how far the original architecture could be expanded without sacrificing clarity or maintainability.
        </p>
        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">How It Works</h2>
        <ul className="list-disc list-inside mb-4 text-muted leading-relaxed">
          <li>
            Builds directly on the original CLI-based multi-model framework, reusing the same core training and generation logic.
          </li>
          <li>
            Introduces a pipeline GUI for configuring datasets, models, training, and exporting directly from the GUI.
          </li>
          <li>
            Ensures consistent training and generation behavior across the CLI, GUI, and applicable model export formats.
          </li>
          <li>
            Explores multiple export formats, including reusable architectures, packaged trained models, framework distributions, and standalone application builds.
          </li>
          <li>
            Prioritizes clean, maintainable code to extend existing functionality without breaking the original framework.
          </li>
        </ul>

        <h2 className="text-xl font-semibold mt-6 mb-2 text-accent">What I Learned</h2>
        <p className="mb-4 leading-relaxed text-muted">
          Through MLux, I gained deeper experience designing systems for extensibility and long-term maintainability rather than short-term experimentation. I learned how architectural choices affect testing strategy and reproducibility as a project grows in scope. This project also reinforced the importance of configuration-driven design, disciplined refactoring, and reusability for experimentation workflows.
        </p>
        <p className="mb-6 text-sm text-secondary italic">
          Initial project duration:: ~8 weeks (Oct 7<sup>th</sup> - Dec 2<sup>nd</sup>, 2025)
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
      <div className="w-full lg:w-1/2 p-8 bg-secondary border-l border-code">
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
                <option value="run/pipeline.py">&#x251C;&#x2500; pipeline.py</option>
                <option value="run/profiler.py">&#x2514;&#x2500; profiler.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /run/core">
                <option value="run/core/dpg_utils.py">&#x2514;&#x2500; dpg_utils.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /run/services">
                <option value="run/services/callbacks.py">&#x251C;&#x2500; callbacks.py</option>
                <option value="run/services/terminal.py">&#x2514;&#x2500; terminal.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /run/ui">
                <option value="run/ui/builders.py">&#x251C;&#x2500; builders.py</option>
                <option value="run/ui/handlers.py">&#x251C;&#x2500; handlers.py</option>
                <option value="run/ui/layout.py">&#x251C;&#x2500; layout.py</option>
                <option value="run/ui/ui.py">&#x251C;&#x2500; ui.py</option>
                <option value="run/ui/widgets.py">&#x2514;&#x2500; widgets.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /services">
                <option value="run/services/application.py">&#x251C;&#x2500; application.py</option>
                <option value="run/services/architecture.py">&#x251C;&#x2500; architecture.py</option>
                <option value="run/services/exporter.py">&#x251C;&#x2500; exporter.py</option>
                <option value="run/services/wrappers.py">&#x2514;&#x2500; wrappers.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /utils">
                <option value="utils/data_utils.py">&#x251C;&#x2500; data_utils.py</option>
                <option value="utils/io_utils.py">&#x251C;&#x2500; io_utils.py</option>
                <option value="utils/model_utils.py">&#x2514;&#x2500; model_utils.py</option>
              </optgroup>
              <optgroup label="&#x2514;&#x2500; /tests">
                <option value="tests/test_application.py">&#x251C;&#x2500; test_application.py</option>
                <option value="tests/test_architecture.py">&#x251C;&#x2500; test_architecture.py</option>
                <option value="tests/test_base_model.py">&#x251C;&#x2500; test_base_model.py</option>
                <option value="tests/test_bigram_model.py">&#x251C;&#x2500; test_bigram_model.py</option>
                <option value="tests/test_builders.py">&#x251C;&#x2500; test_builders.py</option>
                <option value="tests/test_callbacks.py">&#x251C;&#x2500; test_callbacks.py</option>
                <option value="tests/test_cli.py">&#x251C;&#x2500; test_cli.py</option>
                <option value="tests/test_config.py">&#x251C;&#x2500; test_config.py</option>
                <option value="tests/test_config_widgets.py">&#x251C;&#x2500; test_config_widgets.py</option>
                <option value="tests/test_dashboard.py">&#x251C;&#x2500; test_dashboard.py</option>
                <option value="tests/test_data_utils.py">&#x251C;&#x2500; test_data_utils.py</option>
                <option value="tests/test_distilgpt2_model.py">&#x251C;&#x2500; test_distilgpt2_model.py</option>
                <option value="tests/test_dpg_utils.py">&#x251C;&#x2500; test_dpg_utils.py</option>
                <option value="tests/test_exporter.py">&#x251C;&#x2500; test_exporter.py</option>
                <option value="tests/test_generators.py">&#x251C;&#x2500; test_generators.py</option>
                <option value="tests/test_gru_model.py">&#x251C;&#x2500; test_gru_model.py</option>
                <option value="tests/test_handlers.py">&#x251C;&#x2500; test_handlers.py</option>
                <option value="tests/test_io_utils.py">&#x251C;&#x2500; test_io_utils.py</option>
                <option value="tests/test_layout.py">&#x251C;&#x2500; test_layout.py</option>
                <option value="tests/test_library.py">&#x251C;&#x2500; test_library.py</option>
                <option value="tests/test_lstm_model.py">&#x251C;&#x2500; test_lstm_model.py</option>
                <option value="tests/test_main.py">&#x251C;&#x2500; test_main.py</option>
                <option value="tests/test_model_utils.py">&#x251C;&#x2500; test_model_utils.py</option>
                <option value="tests/test_pipeline.py">&#x251C;&#x2500; test_pipeline.py</option>
                <option value="tests/test_profiler.py">&#x251C;&#x2500; test_profiler.py</option>
                <option value="tests/test_registry.py">&#x251C;&#x2500; test_registry.py</option>
                <option value="tests/test_run__main__.py">&#x251C;&#x2500; test_run__main__.py</option>
                <option value="tests/test_terminal.py">&#x251C;&#x2500; test_terminal.py</option>
                <option value="tests/test_training.py">&#x251C;&#x2500; test_training.py</option>
                <option value="tests/test_transformer_model.py">&#x251C;&#x2500; test_transformer_model.py</option>
                <option value="tests/test_tuning.py">&#x251C;&#x2500; test_tuning.py</option>
                <option value="tests/test_ui.py">&#x251C;&#x2500; test_ui.py</option>
                <option value="tests/test_visualizer.py">&#x251C;&#x2500; test_visualizer.py</option>
                <option value="tests/test_wrappers.py">&#x2514;&#x2500; test_wrappers.py</option>
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

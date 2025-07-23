import { useState, useRef } from 'react';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import './App.css';

function App() {
  const [files, setFiles] = useState([]);
  const [rules, setRules] = useState(`- Convert PHP files to equivalent JavaScript modules or classes.
- For index.html, replace PHP code with JavaScript that imports/uses the converted JS files.
- Output only the code for each file, no explanations.
- For example, if index.html used PHP to render a user, use a <script> tag to call the JS code and render the result in the DOM.`);
  const [progress, setProgress] = useState(0);
  const [isMigrating, setIsMigrating] = useState(false);
  const [error, setError] = useState('');
  const [apiKey] = useState(import.meta.env.VITE_OPENAI_API_KEY || '');
  const fileInputRef = useRef();

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
    setError('');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setFiles(Array.from(e.dataTransfer.files));
    setError('');
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleStartMigration = async () => {
    if (!files.length) {
      setError('Please upload at least one PHP file.');
      return;
    }
    if (!apiKey) {
      setError('OpenAI API key is not set. Please set it in your .env file.');
      return;
    }
    setIsMigrating(true);
    setProgress(0);
    setError('');
    const zip = new JSZip();
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const phpCode = await file.text();
      try {
        const jsCode = await migratePHPtoJS(phpCode, rules, apiKey);
        const jsFileName = file.name.replace(/\.php$/, '.js');
        zip.file(jsFileName, jsCode);
      } catch (err) {
        zip.file(file.name.replace(/\.php$/, '.js'), `// Migration failed: ${err.message}`);
      }
      setProgress(Math.round(((i + 1) / files.length) * 100));
    }
    // Generate ZIP and trigger download
    zip.generateAsync({ type: 'blob' }).then((content) => {
      saveAs(content, `migrated_js_${Date.now()}.zip`);
      setIsMigrating(false);
      setProgress(0);
    });
  };

  async function migratePHPtoJS(phpCode, rules, apiKey) {
    const prompt = `Convert the following PHP code to modern JavaScript. Apply these migration rules: ${rules}\n\nPHP code:\n${phpCode}\n\nJavaScript code:`;
    const response = await fetch('https://api.openai.com/v1/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo-instruct',
        prompt,
        max_tokens: 2048,
        temperature: 0,
      }),
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error?.message || 'OpenAI API error');
    }
    const data = await response.json();
    return data.choices[0].text.trim();
  }

  return (
    <div className="container">
      <h1>PHP to JavaScript Migration (Frontend Only)</h1>
      <div
        className="upload-area"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current.click()}
      >
        <input
          type="file"
          accept=".php"
          multiple
          style={{ display: 'none' }}
          ref={fileInputRef}
          onChange={handleFileChange}
          webkitdirectory="true"
          directory="true"
        />
        <p>Drag & drop PHP files or select a <b>folder</b> to upload your project.</p>
        {files.length > 0 && (
          <ul className="file-list">
            {files.map((f, i) => (
              <li key={i}>{f.name}</li>
            ))}
          </ul>
        )}
      </div>
      <div className="rules-section">
        <label htmlFor="rules">Migration Checklist / Rules:</label>
        <textarea
          id="rules"
          value={rules}
          onChange={e => setRules(e.target.value)}
          placeholder="e.g. convert $this to this, use try/catch for error handling"
        />
      </div>
      <button className="migrate-btn" onClick={handleStartMigration} disabled={isMigrating}>
        {isMigrating ? 'Migrating...' : 'Start Migration'}
      </button>
      {progress > 0 && (
        <div className="progress-bar">
          <div className="progress" style={{ width: `${progress}%` }}></div>
        </div>
      )}
      {error && <div className="error">{error}</div>}
      <div style={{marginTop: '1.5rem', fontSize: '0.95rem', color: '#888'}}>
        <b>Note:</b> Your OpenAI API key is read from your .env file and never shown in the UI.<br/>
        For privacy, do not commit your .env file to version control.
      </div>
    </div>
  );
}

export default App;

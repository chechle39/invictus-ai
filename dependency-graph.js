#!/usr/bin/env node
// dependency-graph.js
// Script: Quét dependency cho nhiều ngôn ngữ (PHP, JS, TS, Python, Java, C#, Ruby)

const fs = require("fs");
const path = require("path");

// --- Config ---
const EXT_LANG_MAP = {
  ".php": "php",
  ".js": "js",
  ".ts": "ts",
  ".py": "python",
  ".java": "java",
  ".cs": "csharp",
  ".rb": "ruby",
};

// --- Helper: Recursively get all files ---
function getAllFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  files.forEach((file) => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      getAllFiles(filePath, fileList);
    } else {
      fileList.push(filePath);
    }
  });
  return fileList;
}

// --- Dependency analyzers for each language ---
function analyzePhpDependencies(content) {
  // Tìm require/include/use/class/function call
  const regexes = [
    /require(?:_once)?\s*\(?['"](.+?)['"]\)?/g,
    /include(?:_once)?\s*\(?['"](.+?)['"]\)?/g,
    /use\s+([\w\\]+)/g,
    /new\s+([A-Za-z_][\w\\]*)/g,
    /([A-Za-z_][\w]*)::/g,
  ];
  return extractMatches(content, regexes);
}

function analyzeJsDependencies(content) {
  // import, require, ES6 export
  const regexes = [
    /require\(['"](.+?)['"]\)/g,
    /import\s+.*?from\s+['"](.+?)['"]/g,
    /import\s+['"](.+?)['"]/g,
    /export\s+.*?from\s+['"](.+?)['"]/g,
  ];
  return extractMatches(content, regexes);
}

function analyzePythonDependencies(content) {
  // import, from ... import ...
  const regexes = [/import\s+([\w\.]+)/g, /from\s+([\w\.]+)\s+import/g];
  return extractMatches(content, regexes);
}

function analyzeJavaDependencies(content) {
  // import, extends, implements
  const regexes = [
    /import\s+([\w\.]+);/g,
    /extends\s+([A-Za-z_][\w]*)/g,
    /implements\s+([A-Za-z_][\w, ]*)/g,
  ];
  return extractMatches(content, regexes);
}

function analyzeCsharpDependencies(content) {
  // using, namespace, class inheritance
  const regexes = [
    /using\s+([\w\.]+);/g,
    /namespace\s+([\w\.]+)/g,
    /:([A-Za-z_][\w]*)/g, // class inheritance
  ];
  return extractMatches(content, regexes);
}

function analyzeRubyDependencies(content) {
  // require, require_relative, include, class inheritance
  const regexes = [
    /require(_relative)?\s+['"](.+?)['"]/g,
    /include\s+([A-Za-z_][\w]*)/g,
    /<\s*([A-Za-z_][\w]*)/g, // class inheritance
  ];
  return extractMatches(content, regexes);
}

function extractMatches(content, regexes) {
  const deps = new Set();
  for (const regex of regexes) {
    let match;
    while ((match = regex.exec(content))) {
      // Lấy group cuối cùng không phải undefined
      for (let i = match.length - 1; i > 0; i--) {
        if (match[i]) {
          deps.add(match[i]);
          break;
        }
      }
    }
  }
  return Array.from(deps);
}

// --- Main ---
function analyzeDependencies(filePath, lang) {
  const content = fs.readFileSync(filePath, "utf-8");
  switch (lang) {
    case "php":
      return analyzePhpDependencies(content);
    case "js":
    case "ts":
      return analyzeJsDependencies(content);
    case "python":
      return analyzePythonDependencies(content);
    case "java":
      return analyzeJavaDependencies(content);
    case "csharp":
      return analyzeCsharpDependencies(content);
    case "ruby":
      return analyzeRubyDependencies(content);
    default:
      return [];
  }
}

// --- CLI ---
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log("Usage: node dependency-graph.js <sourceDir> <output.json>");
    process.exit(1);
  }
  const [sourceDir, outputFile] = args;
  const files = getAllFiles(sourceDir);
  const results = [];
  for (const file of files) {
    const ext = path.extname(file).toLowerCase();
    const lang = EXT_LANG_MAP[ext] || "unknown";
    if (lang === "unknown") continue;
    const deps = analyzeDependencies(file, lang);
    results.push({ file, type: lang, dependencies: deps });
  }
  fs.writeFileSync(outputFile, JSON.stringify(results, null, 2), "utf-8");
  console.log(`Dependency graph saved to ${outputFile}`);
}

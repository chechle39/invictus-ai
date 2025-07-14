#!/usr/bin/env node
// migration-map.js
// CLI tool: Generate migration map using OpenAI

const fs = require("fs");
const path = require("path");
const OpenAI = require("openai");
const { Command } = require("commander");
const PdfPrinter = require("pdfmake");

// --- Config ---
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
if (!OPENAI_API_KEY) {
  console.error("Please set your OPENAI_API_KEY environment variable.");
  process.exit(1);
}

const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

// --- CLI setup ---
const program = new Command();
program
  .argument("<sourceDir>", "Source code directory to analyze")
  .option("-o, --output <file>", "Output file", "migration-map.json")
  .option("--pdf <file>", "Export migration map to PDF")
  .option(
    "--from <sourceLang>",
    "Source programming language (e.g., php, java, nodejs)",
    "php"
  )
  .option(
    "--to <targetLang>",
    "Target programming language (e.g., nodejs, java, python)",
    "nodejs"
  )
  .parse();

const [sourceDir] = program.args;
const { output, pdf, from, to } = program.opts();

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

// --- Helper: Summarize file for prompt ---
function summarizeFile(filePath) {
  const ext = path.extname(filePath);
  return `File: ${filePath} (type: ${ext})`;
}

// --- Main: Analyze files with OpenAI ---
async function analyzeFile(filePath) {
  const prompt = `You are a system migration expert. The source system is written in ${from}. The target system must be in ${to}.
Analyze the following file:
${summarizeFile(filePath)}
1. Classify: (a) Direct migration, (b) Rewrite, (c) Special review required.
2. Suggest equivalent technology, library, or framework in the target language if needed (e.g., SQL → NoSQL, REST → GraphQL, PHP array config → Node.js JSON config).
3. If possible, provide migration notes specific to converting from ${from} to ${to}.
Reply in JSON format, in English:
{
  "file": "...",
  "migrationType": "...", // One of: direct migration, rewrite, special review
  "suggestedTech": "...", // Suggest equivalent technology (if any)
  "note": "..." // Short note in English, specific to migration from ${from} to ${to}
}`;

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.2,
    });
    const text = completion.choices[0].message.content;
    console.log(
      "\n--- AI response for",
      filePath,
      "---\n",
      text,
      "\n-----------------------------\n"
    );
    // Sửa lỗi escape ký tự trong JSON trả về từ OpenAI
    const safeText = text.replace(/\\/g, "\\\\");
    return JSON.parse(safeText);
  } catch (err) {
    return {
      file: filePath,
      migrationType: "error",
      suggestedTech: "",
      note: err.message,
    };
  }
}

// --- Export to PDF using pdfmake ---
function exportToPDF(data, pdfFile) {
  const fonts = {
    Roboto: {
      normal: "./fonts/Roboto-Regular.ttf",
      bold: "./fonts/Roboto-Bold.ttf",
      italics: "./fonts/Roboto-Regular.ttf",
      bolditalics: "./fonts/Roboto-Bold.ttf",
    },
  };
  const printer = new PdfPrinter(fonts);

  // Table header + body
  const tableBody = [
    [
      { text: "File", bold: true },
      { text: "Migration Type", bold: true },
      { text: "Suggested Tech", bold: true },
      { text: "Note", bold: true },
    ],
    ...data.map((item) => {
      const noteCell = {
        text: item.note || "",
        noWrap: false,
        alignment: "left",
        fontSize: 9,
      };
      if (item.migrationType === "error") {
        return [
          { text: item.file || "", color: "red", noWrap: false },
          { text: "ERROR", color: "red", bold: true, noWrap: false },
          { text: item.suggestedTech || "", color: "red", noWrap: false },
          { ...noteCell, color: "red" },
        ];
      }
      return [
        { text: item.file || "", noWrap: false },
        { text: item.migrationType || "", noWrap: false },
        { text: item.suggestedTech || "", noWrap: false },
        noteCell,
      ];
    }),
  ];

  const docDefinition = {
    pageOrientation: "landscape", // Xoay ngang trang nếu cần
    content: [
      { text: "Migration Map", style: "header" },
      {
        text: `Generated at: ${new Date().toLocaleString()}`,
        margin: [0, 0, 0, 10],
      },
      {
        table: {
          headerRows: 1,
          widths: [100, 80, 100, "*"], // Cột Note tự động rộng nhất
          body: tableBody,
        },
        layout: "lightHorizontalLines",
      },
    ],
    styles: {
      header: { fontSize: 18, bold: true, margin: [0, 0, 0, 10] },
    },
  };

  const pdfDoc = printer.createPdfKitDocument(docDefinition);
  pdfDoc.pipe(fs.createWriteStream(pdfFile));
  pdfDoc.end();
}

// --- Main flow ---
(async () => {
  console.log(`Scanning directory: ${sourceDir}`);
  const files = getAllFiles(sourceDir);
  console.log(`Found ${files.length} files. Analyzing...`);

  const results = [];
  for (const file of files) {
    console.log(`Analyzing: ${file}`);
    const res = await analyzeFile(file);
    results.push(res);
  }

  fs.writeFileSync(output, JSON.stringify(results, null, 2), "utf-8");
  console.log(`Migration map saved to ${output}`);

  if (pdf) {
    exportToPDF(results, pdf);
    console.log(`Migration map PDF exported to ${pdf}`);
  }
})();

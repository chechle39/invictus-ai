const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
const fs = require("fs");
const { generateChecklistAI } = require("./lib/checklist-generator");
const PdfPrinter = require("pdfmake");

const app = express();
app.use(bodyParser.json());
app.use(express.static("public"));
app.use(
  "/example/result",
  express.static(path.join(__dirname, "example", "result"))
);

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.post("/generate_checklist", async (req, res) => {
  try {
    const apiKey = req.headers["x-openai-api-key"];
    if (!apiKey) return res.status(400).json({ error: "Missing API key" });
    const {
      srcDir,
      outputFile = "manual-checklist.xlsx",
      language = "vi",
      generatePdf,
    } = req.body;
    if (!srcDir) return res.status(400).json({ error: "Missing srcDir" });
    const resultDir = path.join(__dirname, "example", "result");
    const outPath = await generateChecklistAI({
      srcDir: path.isAbsolute(srcDir) ? srcDir : path.join(__dirname, srcDir),
      resultDir,
      outputFile,
      openaiApiKey: apiKey,
      language,
    });
    let pdfUrl = null;
    if (generatePdf) {
      // Đọc lại file xlsx, chuyển sang PDF
      const XLSX = require("xlsx");
      const wb = XLSX.readFile(outPath);
      const ws = wb.Sheets[wb.SheetNames[0]];
      const data = XLSX.utils.sheet_to_json(ws, { header: 1 });
      // Tạo PDF
      const fonts = {
        Roboto: {
          normal: path.join(__dirname, "fonts", "Roboto-Regular.ttf"),
          bold: path.join(__dirname, "fonts", "Roboto-Bold.ttf"),
          italics: path.join(__dirname, "fonts", "Roboto-Regular.ttf"),
          bolditalics: path.join(__dirname, "fonts", "Roboto-Bold.ttf"),
        },
      };
      const printer = new PdfPrinter(fonts);
      const docDefinition = {
        pageOrientation: "landscape",
        content: [
          { text: "Checklist Manual Test", style: "header" },
          {
            table: {
              headerRows: 1,
              body: data,
            },
            layout: "lightHorizontalLines",
          },
        ],
        styles: {
          header: { fontSize: 18, bold: true, margin: [0, 0, 0, 10] },
        },
      };
      const pdfFile = path.join(
        resultDir,
        outputFile.replace(/\.xlsx$/, ".pdf")
      );
      const pdfDoc = printer.createPdfKitDocument(docDefinition);
      pdfDoc.pipe(fs.createWriteStream(pdfFile));
      pdfDoc.end();
      pdfUrl = `/example/result/${path.basename(pdfFile)}`;
    }
    const fileUrl = `/example/result/${outputFile}`;
    res.json({ fileUrl, pdfUrl });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Checklist AI web server running at http://localhost:${PORT}`);
});

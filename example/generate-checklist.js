const { generateChecklistAI } = require("../lib/checklist-generator");
const path = require("path");

(async () => {
  const openaiApiKey = process.env.OPENAI_API_KEY;
  if (!openaiApiKey) {
    console.error("Vui lòng set biến môi trường OPENAI_API_KEY");
    process.exit(1);
  }
  const srcDir = path.join(__dirname, "src");
  const resultDir = path.join(__dirname, "result");
  const outputFile = "manual-checklist.xlsx";
  const outPath = await generateChecklistAI({
    srcDir,
    resultDir,
    outputFile,
    openaiApiKey,
    language: "vi", // hoặc 'en'
  });
  console.log("Đã sinh checklist:", outPath);
})();

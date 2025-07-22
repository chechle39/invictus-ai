const fs = require("fs");
const path = require("path");
const XLSX = require("xlsx");

const SRC_DIR = path.join(__dirname, "example", "src");
const RESULT_DIR = path.join(__dirname, "example", "result");
const OUTPUT_FILE = path.join(RESULT_DIR, "manual-checklist.xlsx");

// Helper: Recursively get all files in a directory
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

// Helper: Extract class/function names from PHP/JS files (simple regex)
function extractEntities(content, ext) {
  const entities = [];
  if (ext === ".php") {
    // Class
    const classRegex = /class\s+(\w+)/g;
    let match;
    while ((match = classRegex.exec(content))) {
      entities.push({ type: "Class", name: match[1] });
    }
    // Function
    const funcRegex = /function\s+(\w+)/g;
    while ((match = funcRegex.exec(content))) {
      entities.push({ type: "Function", name: match[1] });
    }
  } else if (ext === ".js" || ext === ".ts") {
    // Function
    const funcRegex = /function\s+(\w+)/g;
    let match;
    while ((match = funcRegex.exec(content))) {
      entities.push({ type: "Function", name: match[1] });
    }
    // Class
    const classRegex = /class\s+(\w+)/g;
    while ((match = classRegex.exec(content))) {
      entities.push({ type: "Class", name: match[1] });
    }
  }
  return entities;
}

// Main logic
function main() {
  if (!fs.existsSync(RESULT_DIR)) {
    fs.mkdirSync(RESULT_DIR, { recursive: true });
  }
  const files = getAllFiles(SRC_DIR);
  let testCases = [];
  let tcId = 1;
  for (const file of files) {
    const ext = path.extname(file).toLowerCase();
    if (![".php", ".js", ".ts"].includes(ext)) continue;
    const content = fs.readFileSync(file, "utf-8");
    const entities = extractEntities(content, ext);
    // Nếu không có entity, vẫn tạo test case cho file
    if (entities.length === 0) {
      testCases.push({
        id: `TC-${tcId.toString().padStart(3, "0")}`,
        file: path.relative(SRC_DIR, file),
        entity: "",
        description: `Kiểm thử chức năng chính của file ${path.basename(file)}`,
        steps:
          "Kiểm tra các chức năng chính, luồng xử lý, và các điểm tích hợp.",
        expected: "Chức năng hoạt động đúng, không lỗi.",
        note: "",
      });
      tcId++;
    } else {
      for (const ent of entities) {
        testCases.push({
          id: `TC-${tcId.toString().padStart(3, "0")}`,
          file: path.relative(SRC_DIR, file),
          entity: `${ent.type}: ${ent.name}`,
          description: `Kiểm thử ${ent.type.toLowerCase()} ${
            ent.name
          } trong file ${path.basename(file)}`,
          steps: `Kiểm tra các chức năng, luồng xử lý, và các trường hợp biên của ${ent.type.toLowerCase()} ${
            ent.name
          }.`,
          expected: `${ent.type} ${ent.name} hoạt động đúng, không lỗi.`,
          note: "",
        });
        tcId++;
      }
    }
  }
  // Tạo worksheet và ghi file xlsx
  const wsData = [
    [
      "Test Case ID",
      "File",
      "Entity",
      "Mô tả",
      "Bước thực hiện",
      "Kết quả mong đợi",
      "Ghi chú",
    ],
    ...testCases.map((tc) => [
      tc.id,
      tc.file,
      tc.entity,
      tc.description,
      tc.steps,
      tc.expected,
      tc.note,
    ]),
  ];
  const ws = XLSX.utils.aoa_to_sheet(wsData);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Checklist");
  XLSX.writeFile(wb, OUTPUT_FILE);
  console.log(`Đã sinh file checklist: ${OUTPUT_FILE}`);
}

main();

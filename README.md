# Migration Map CLI

Tool CLI Node.js giúp tạo bản đồ chuyển đổi (migration map) cho quá trình migrate hệ thống, sử dụng OpenAI để phân tích và gợi ý công nghệ tương đương.

## Tính năng chính

- **Phân tích code tự động:** Quét thư mục mã nguồn và phân tích từng file
- **AI-powered migration mapping:** Sử dụng OpenAI để phân loại loại chuyển đổi và gợi ý công nghệ tương đương
- **Hỗ trợ đa ngôn ngữ:** PHP, Python, Java, Node.js, C#, Go, v.v.
- **Export đa định dạng:** JSON và PDF với bảng chi tiết
- **Error handling:** Tự động xử lý lỗi và hiển thị rõ ràng trong PDF

## Cài đặt

1. **Cài Node.js >= 16**
2. **Cài dependencies:**
   ```bash
   npm install
   ```
3. **Đặt biến môi trường OpenAI API key:**

   ```bash
   # Windows PowerShell:
   $env:OPENAI_API_KEY="your_openai_api_key"

   # Windows CMD:
   set OPENAI_API_KEY=your_openai_api_key

   # Mac/Linux:
   export OPENAI_API_KEY=your_openai_api_key
   ```

## Sử dụng

### Cú pháp cơ bản

```bash
node migration-map.js <sourceDir> --from <sourceLang> --to <targetLang> [options]
```

### Tham số

- `<sourceDir>`: Thư mục mã nguồn cần phân tích
- `--from <sourceLang>`: Ngôn ngữ nguồn (php, python, java, nodejs, csharp, go, v.v.)
- `--to <targetLang>`: Ngôn ngữ đích (nodejs, python, java, csharp, go, v.v.)

### Options

- `-o, --output <file>`: Tên file JSON xuất kết quả (mặc định: migration-map.json)
- `--pdf <file>`: Xuất migration map ra file PDF có bảng

### Ví dụ sử dụng

**Phân tích PHP sang Node.js:**

```bash
node migration-map.js ./example/src --from php --to nodejs --pdf ./example/result/migration-map.pdf -o ./example/result/migration-map.json
```

**Phân tích Python sang Java:**

```bash
node migration-map.js ./example/src --from python --to java --pdf ./example/result/migration-map.pdf
```

**Phân tích Java sang C#:**

```bash
node migration-map.js ./example/src --from java --to csharp --pdf ./example/result/migration-map.pdf
```

## Kết quả

### File JSON

Chứa migration map với các trường:

- `file`: Tên file/module
- `migrationType`: Loại chuyển đổi (direct migration, rewrite, special review)
- `suggestedTech`: Gợi ý công nghệ tương đương
- `note`: Ghi chú chi tiết về migration

### File PDF

- Bảng migration map dễ theo dõi
- Tự động xuống dòng cho nội dung dài
- Highlight các trường hợp error
- Trang ngang (landscape) để hiển thị nhiều nội dung

## Ví dụ kết quả

### PHP → Node.js

| File               | Migration Type | Suggested Tech   | Note                                            |
| ------------------ | -------------- | ---------------- | ----------------------------------------------- |
| UserController.php | Rewrite        | Express.js       | Convert PHP class to Node.js Express controller |
| config.php         | Rewrite        | JSON config      | Convert PHP array to Node.js JSON configuration |
| schema.sql         | Special review | MongoDB/Mongoose | SQL to NoSQL migration requires careful review  |

### Python → Java

| File               | Migration Type | Suggested Tech         | Note                                           |
| ------------------ | -------------- | ---------------------- | ---------------------------------------------- |
| user_controller.py | Rewrite        | Spring Boot            | Convert Python class to Java Spring controller |
| config.py          | Rewrite        | application.properties | Convert Python dict to Java properties file    |

## Cấu trúc thư mục example

```
example/
  src/           # Chứa code mẫu để test
    UserController.php
    User.php
    config.php
    PaymentService.php
    schema.sql
    # Có thể thêm file Python, Java, v.v.
  result/        # Chứa kết quả phân tích
    migration-map.json
    migration-map.pdf
  README.md      # Hướng dẫn test
```

## Lưu ý

- **Chi phí OpenAI:** Mỗi file tốn khoảng $0.0005–$0.003 (với gpt-3.5-turbo)
- **API Key:** Đảm bảo có đủ quota và API key hợp lệ
- **Font PDF:** Cần tải font Roboto về thư mục `fonts/` nếu gặp lỗi font
- **File size:** Tool tự động xử lý file lớn và nội dung dài

## Mở rộng

- Thêm support cho ngôn ngữ mới
- Tích hợp với CI/CD pipeline
- Thêm tính năng phân tích dependency
- Export ra định dạng khác (CSV, Excel, Markdown)

## License

MIT

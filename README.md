# Migration Map Tool (All-in-One)

## Mục đích

Tool này giúp bạn phân tích, lập kế hoạch migrate (chuyển đổi) dự án code từ ngôn ngữ này sang ngôn ngữ khác một cách thông minh:

- Tự động nhận diện các file/module có liên kết với nhau (dependency graph).
- Phát hiện và gợi ý migrate database (schema, truy vấn SQL, ORM, GraphQL...)
- Đề xuất công nghệ tương ứng ở ngôn ngữ đích.
- Xuất kết quả ra file JSON và PDF, dễ đọc, dễ kiểm tra.

## Tính năng nổi bật

- **Nhóm file/module liên kết**: Các file có liên kết sẽ được nhóm thành từng nhóm/module rõ ràng.
- **Gợi ý database hiện đại**: Tự động phát hiện schema, truy vấn SQL, gợi ý ORM, GraphQL, NoSQL nếu phù hợp.
- **Hỗ trợ đa ngôn ngữ**: PHP, JS, TS, Python, Java, C#, Ruby...

## Cách sử dụng

### 1. Cài đặt dependencies

```bash
npm install
```

### 2. Thiết lập biến môi trường OpenAI API Key

- **PowerShell:**
  ```powershell
  $env:OPENAI_API_KEY="your_openai_api_key"
  ```
- **CMD:**
  ```cmd
  set OPENAI_API_KEY=your_openai_api_key
  ```

### 3. Chạy tool migrate

```bash
node migration-map.js <sourceDir> --from <sourceLang> --to <targetLang> -o <output.json> --pdf <output.pdf>
```

- `<sourceDir>`: Thư mục chứa source code dự án.
- `--from`: Ngôn ngữ nguồn (vd: php, java, python...)
- `--to`: Ngôn ngữ đích (vd: nodejs, java, python...)
- `-o`: File kết quả JSON.
- `--pdf`: File kết quả PDF.

**Ví dụ:**

```bash
node migration-map.js example/src --from php --to nodejs -o example/result/migration-map.json --pdf example/result/migration-map.pdf
```

## Ý nghĩa các khái niệm

### Dependency (liên kết giữa các file)

- Tool sẽ tự động phát hiện các file nào gọi nhau, import nhau, hoặc có quan hệ logic.
- Các file liên kết sẽ được nhóm thành 1 module/nhóm, giúp bạn migrate logic tổng thể, không bị rời rạc.

### Database & ORM

- Tool sẽ tự động phát hiện file schema (.sql), truy vấn SQL trong code, và gợi ý công nghệ database hiện đại ở ngôn ngữ đích.
- **ORM (Object-Relational Mapping):**
  - Là kỹ thuật giúp bạn thao tác database bằng object/class thay vì viết SQL thuần.
  - Ví dụ: Sequelize, TypeORM (Node.js), Eloquent (PHP), SQLAlchemy (Python)...
  - Giúp code dễ bảo trì, bảo mật, chuyển đổi DB dễ dàng.

### Gợi ý công nghệ hiện đại

- Tool sẽ gợi ý các công nghệ phù hợp ở ngôn ngữ đích: ORM, GraphQL, NoSQL, REST, v.v.
- Giúp bạn refactor project theo hướng hiện đại, dễ mở rộng.

## Kết quả xuất ra

- **JSON**: Dễ dùng cho automation, kiểm tra chi tiết.
- **PDF**: Dễ đọc, trình bày rõ ràng từng nhóm file/module, gợi ý migration, database, công nghệ.

## Ví dụ kết quả (PDF/JSON)

| Files                                            | Migration Plan                                                             | Suggested Tech        | Database Suggestion    | Note                                |
| ------------------------------------------------ | -------------------------------------------------------------------------- | --------------------- | ---------------------- | ----------------------------------- |
| UserController.php, PaymentService.php, User.php | Refactor thành các module Node.js, dùng ORM Sequelize, chuyển SQL sang ORM | Sequelize, ES6 module | PostgreSQL/MySQL + ORM | Lưu ý async/await, khác biệt syntax |
| config.php                                       | Chuyển sang JSON config, dùng package 'config'                             | config (Node.js)      | ORM cho DB             | Lưu ý khác biệt cấu hình            |
| schema.sql                                       | Chuyển schema sang model ORM                                               | Sequelize/Knex.js     | PostgreSQL/MySQL       | Lưu ý mapping type                  |

## Liên hệ & đóng góp

- Nếu có vấn đề, góp ý, hoặc muốn mở rộng tool cho ngôn ngữ khác, hãy liên hệ hoặc tạo issue trên repo!

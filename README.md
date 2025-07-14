# Migration Map CLI

Tool CLI Node.js giúp tạo bản đồ chuyển đổi (migration map) cho quá trình migrate hệ thống, sử dụng OpenAI để phân tích và gợi ý công nghệ tương đương.

## Cài đặt

1. Cài Node.js >= 16
2. Cài dependencies:
   ```bash
   npm install
   ```
3. Đặt biến môi trường OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   # Hoặc trên Windows:
   set OPENAI_API_KEY=your_openai_api_key
   ```

## Sử dụng

```bash
node migration-map.js <sourceDir> [-o output.json] [--pdf output.pdf]
```

- `<sourceDir>`: Thư mục mã nguồn cần phân tích
- `-o, --output`: Tên file xuất kết quả JSON (mặc định: migration-map.json)
- `--pdf`: Xuất migration map ra file PDF có bảng (ví dụ: `--pdf migration-map.pdf`)

Ví dụ:

```bash
node migration-map.js ./src -o migration-map.json --pdf migration-map.pdf
```

## Kết quả

- Tool sẽ xuất file JSON chứa migration map với các trường:
  - `file`: Tên file/module
  - `migrationType`: Loại chuyển đổi (chuyển trực tiếp, viết lại, kiểm tra đặc biệt)
  - `suggestedTech`: Gợi ý công nghệ tương đương
  - `note`: Ghi chú
- Nếu dùng `--pdf`, sẽ có thêm file PDF trình bày migration map dạng bảng, dễ theo dõi và chia sẻ.

## Lưu ý

- Tool sử dụng OpenAI API, có thể tốn phí theo số lượng file và request.
- Bạn có thể tùy chỉnh prompt trong file `migration-map.js` để phù hợp hơn với dự án của mình.

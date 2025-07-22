# Checklist AI Generator

Sinh checklist/manual test case tự động bằng AI (OpenAI GPT-3.5-turbo) cho tester kiểm thử thủ công UI/integration.

## Tính năng

- Phân tích mã nguồn nhiều ngôn ngữ (PHP, JS, TS, Python, Java, C#, Ruby...)
- Sinh checklist/manual test case tổng hợp cho UI/integration
- Xuất file checklist: Excel (.xlsx) và PDF (.pdf)
- Giao diện web đẹp, dễ dùng (Bootstrap)
- Nhập API key qua modal, bảo mật
- Retry 3 lần khi gọi OpenAI API

## Hướng dẫn sử dụng

### 1. Cài đặt

```bash
npm install
```

### 2. Chạy server web

```bash
node web-server.js
```

### 3. Truy cập giao diện

Mở trình duyệt: [http://localhost:3000/](http://localhost:3000/)

### 4. Sử dụng

- Nhập đường dẫn mã nguồn (trên server, ví dụ: `example/src`)
- Chọn ngôn ngữ checklist (Tiếng Việt/English)
- Đặt tên file output (mặc định: `manual-checklist.xlsx`)
- Tick “Tạo file PDF checklist” nếu muốn
- Nhấn **Set API Key** để nhập OpenAI API key
- Nhấn **Generate Checklist**
- Tải file checklist `.xlsx` và `.pdf` khi hoàn thành

## Lưu ý

- Đường dẫn mã nguồn là trên server
- API key chỉ lưu trên trình duyệt
- Nếu thiếu package, cài thêm bằng `npm install <tên-package>`
- Nếu mã nguồn quá lớn, nên chia nhỏ để AI xử lý tốt hơn

---

Nếu cần mở rộng thêm tính năng, preview checklist trên web, hoặc tích hợp CI/CD, hãy liên hệ tác giả!

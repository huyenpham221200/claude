# Report Template — Export File Onpage

Format bắt buộc cho output của SKILL `/export-file-onpage`.

---

## 📤 Export kết quả check onpage — <tên spreadsheet>

**Sheet**: [<tên tab>](<link sheet>)
**Cột đích**: `<chữ cột>` — header `"<tên header>"`
**Ngày export**: <YYYY-MM-DD>

---

## Kết quả ghi

| Checklist | Dòng trong sheet | Trạng thái ghi | Ghi chú đã đẩy lên |
|---|---|---|---|
| <tên checklist> | <số dòng> | ✅ Đã ghi / ⚠️ Đã ghi đè / ❌ Không tìm thấy | <nội dung đã ghi, rút gọn nếu quá dài> |

(Dòng ❌ Không tìm thấy: liệt kê rõ để user tự kiểm tra thủ công — không bỏ
qua âm thầm.)

---

## Ví dụ filled-in report (đã chạy thật, 2026-07-05)

## 📤 Export kết quả check onpage — Checklist Onpage Đá Mỹ Nghệ Cát Tiến

**Sheet**: [Checklist dùng cho khách](https://docs.google.com/spreadsheets/d/1E2_GMLOdEzBgNpPRLf7cpGN5fbpGmyF4DgyObVOLCv4/edit?gid=56626959)
**Cột đích**: `L` — header `"Check lần 2"`
**Ngày export**: 2026-07-05

### Kết quả ghi

| Checklist | Dòng trong sheet | Trạng thái ghi | Ghi chú đã đẩy lên |
|---|---|---|---|
| www & non-www | 11 | ✅ Đã ghi | Cả 4 phiên bản đều tồn tại độc lập, không redirect qua nhau → cần set 301 |
| http & https | 12 | ✅ Đã ghi | (giống dòng 11 — cùng 1 finding Domain) |
| Robots.txt | 14 | ✅ Đã ghi | OK - Có robots.txt, có khai báo Sitemap: |
| OG tags | 44 | ✅ Đã ghi | Thiếu og:image, đã có 5/6 tag còn lại |
| Viewport | 45 | ✅ Đã ghi | OK - content="width=device-width, initial-scale=1" |
| Charset | 46 | ✅ Đã ghi | OK - UTF-8 |
| Hreflang | 47 | ✅ Đã ghi | Không có thẻ hreflang — cần xác nhận site có đa ngôn ngữ không |

### Lưu ý phát hiện thêm khi export

Cột J (Tình trạng hiện tại) của sheet cho thấy `robots.txt` thực tế có xung
đột nhiều block `User-agent: *` (bị Yoast ghi đè thành mở toàn site) — chi
tiết hơn kết quả PASS của `check-onpage-co-ban`. Đã **giữ nguyên dữ liệu có
sẵn trong sheet**, không tự ý sửa đè — chỉ thêm ghi chú lần check mới vào
cột L như yêu cầu.

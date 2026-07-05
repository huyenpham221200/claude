---
name: export-file-onpage
description: Đẩy kết quả check onpage (cột "Ghi chú chi tiết" từ skill check-onpage-co-ban) lên 1 Google Sheet có sẵn, ghi đúng dòng tương ứng với từng checklist. Dùng khi user đưa link Google Sheet + tên cột đích và muốn "export file onpage", "đẩy kết quả lên sheet", "cập nhật sheet check onpage", hoặc gõ "/export-file-onpage".
user-invokable: true
argument-hint: <link Google Sheet> <cột đích> (vd: /export-file-onpage https://docs.google.com/spreadsheets/d/xxx/edit#gid=123 L)
license: MIT
metadata:
  author: SEONGON
  version: 1.0
  category: seo
---

# Export File Onpage

## Role

Bạn là trợ lý đẩy kết quả check onpage lên Google Sheet cho nhân sự SEONGON.
Đầu vào là 1 báo cáo đã có sẵn (thường vừa tạo ra bởi skill
`check-onpage-co-ban`, cột "Ghi chú chi tiết") và 1 Google Sheet có sẵn cấu
trúc dạng bảng checklist (cột "Hạng mục" / "Tên checklist" / ...). Nhiệm vụ:
đọc đúng sheet, tự nhận diện dòng nào ứng với checklist nào, rồi ghi ghi chú
vào đúng ô của cột đích user chỉ định — **không đoán vị trí**, luôn đọc dữ
kiện thật từ Sheets API trước khi ghi.

## Khi nào được gọi

- User gõ `/export-file-onpage <link sheet> <cột đích>`.
- User đưa link Google Sheet + tên cột và nói "đẩy kết quả check lên sheet
  giúp tôi", "export file onpage", "cập nhật cột ... trong sheet này".

## Setup 1 lần (đã hoàn tất, không cần lặp lại mỗi lần dùng skill)

Skill dùng OAuth2 riêng (không dùng chung với skill khác) — client lưu ở
`credentials/oauth_client.json`, token ở `credentials/token.json` (cả 2 đều
gitignore, không lên GitHub). Nếu máy mới/chưa có token, chạy:

```
python scripts/auth.py
```

Lệnh này mở browser 1 lần để đăng nhập Google + cấp quyền
(`https://www.googleapis.com/auth/spreadsheets`). Sau đó token tự refresh,
không cần đăng nhập lại.

## Quy trình 5 bước

### Bước 1 — Parse input

Từ yêu cầu user, xác định:
- **Link Google Sheet** (giữ nguyên URL, có thể chứa `#gid=...` hoặc
  `?gid=...` để biết đúng tab).
- **Cột đích** (vd "L", hoặc "cột L - Check lần 2" → cột là `L`, tên header
  mong muốn là `Check lần 2`).

Nếu user không nói rõ tên header cho cột đích, hỏi lại trước khi ghi.

### Bước 2 — Đọc cấu trúc sheet thật

Dùng `scripts/sheet_io.py`:

```
python scripts/sheet_io.py resolve-tab "<link sheet>"
python scripts/sheet_io.py read "<link sheet>" --range "A1:Z50"
```

Từ dữ liệu đọc được, **tự xác định** (không đoán, đọc thật):
- Dòng nào là **dòng header** (dòng có các nhãn cột như "Chi tiết", "Trạng
  thái", tương tự — thường là dòng đầu tiên có nhiều ô liền kề không rỗng và
  ngay phía trên các dòng dữ liệu có cột STT dạng số).
- Cột nào chứa **Tên checklist** (thường đi kèm cột "Hạng mục" — xem ví dụ
  thật ở [`checklist-export.md`](checklist-export.md)).

### Bước 3 — Đối chiếu từng checklist

Với mỗi dòng trong báo cáo check-onpage-co-ban (Hạng mục | Checklist |
Trạng thái | Ghi chú chi tiết), tìm dòng trong sheet có cột Tên checklist
khớp (so sánh không phân biệt hoa/thường, bỏ khoảng trắng thừa). Lưu ý đặc
biệt:
- **Checklist "Domain" của skill 1 là 1 dòng gộp** (`www & non-www / http &
  https`) nhưng sheet thực tế có thể **tách thành 2 dòng riêng** (`www &
  non-www` và `http & https`) — nếu vậy, ghi **cùng 1 nội dung ghi chú** vào
  cả 2 dòng đó.
- Nếu **không tìm thấy** dòng khớp cho 1 checklist nào đó trong sheet — báo
  rõ cho user, **không bỏ qua âm thầm** và không đoán đại 1 dòng gần đúng.

### Bước 4 — Ghi vào cột đích

- Nếu ô header của cột đích (cùng dòng header đã xác định ở Bước 2) đang
  **trống** → ghi tên header trước (vd `Check lần 2`).
- Nếu ô header đã có **nội dung khác** → báo cho user, hỏi xác nhận trước
  khi ghi đè (có thể user đã đặt tên cột khác ý muốn).
- Với mỗi dòng đã khớp ở Bước 3: **đọc trước** giá trị hiện tại của ô đích.
  - Nếu ô đang **trống** → ghi thẳng.
  - Nếu ô đã **có nội dung khác** với nội dung sắp ghi → báo cho user
    (liệt kê rõ nội dung cũ vs nội dung mới), hỏi xác nhận trước khi ghi đè.

Dùng:
```
python scripts/sheet_io.py write "<link sheet>" --range "<A1 range>" --values '[["<nội dung>"]]'
```

### Bước 5 — Xác nhận lại

Đọc lại toàn bộ các ô vừa ghi (không tin tưởng mù quáng vào response của
lệnh write), so khớp với nội dung dự kiến, rồi báo cáo theo format ở
[`report-template.md`](report-template.md): dòng nào ghi thành công, dòng
nào không tìm thấy khớp trong sheet.

Trả report này cho user trong chat như bình thường **và đồng thời** lưu 1 bản
y hệt ra file, để giữ lịch sử các lần export trước:

```
mkdir -p ~/.claude/output/export-file-onpage
python -c "import datetime; print(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))"
```

Ghi report vừa tạo vào:
```
~/.claude/output/export-file-onpage/<timestamp>.md
```
(vd `~/.claude/output/export-file-onpage/2026-07-05_14-30.md`). Mỗi lần chạy
skill là 1 file mới theo timestamp lúc chạy — **không ghi đè** file của lần
chạy trước.

## Tiêu chí chất lượng

Trước khi báo hoàn thành cho user, tự check:
- [ ] Đã đọc header + cột Tên checklist thật từ sheet, không đoán vị trí.
- [ ] Mỗi dòng ghi đều đã đọc lại để xác nhận, không chỉ tin response của
      lệnh write.
- [ ] Không ghi đè ô đã có nội dung khác mà chưa hỏi user.
- [ ] Checklist nào không tìm thấy dòng khớp đều được liệt kê rõ, không bỏ
      qua âm thầm.
- [ ] Báo cáo cuối có link trực tiếp tới sheet + tab đã ghi.
- [ ] Đã lưu 1 bản report ra `~/.claude/output/export-file-onpage/<timestamp>.md`,
      không ghi đè file lần chạy trước.

## Vết xe đổ — lỗi thường gặp

- **Google Sheets API cần TÊN tab, không dùng được `gid` trực tiếp trong A1
  notation.** Luôn gọi `spreadsheets().get()` để map `gid` → tên tab trước
  khi đọc/ghi (đã xử lý sẵn trong `resolve-tab` của `sheet_io.py`).
- **Merged cells khiến cột "Hạng mục" chỉ có giá trị ở dòng đầu nhóm, các
  dòng sau trống** (vd "Domain" chỉ xuất hiện ở dòng `www & non-www`, dòng
  `http & https` ngay dưới có cột Hạng mục rỗng). Đừng hiểu nhầm dòng rỗng
  đó là thiếu dữ liệu — vẫn match theo cột Tên checklist bình thường.
- **In tiếng Việt ra console Windows dễ lỗi encoding** (`UnicodeEncodeError`
  với `cp1252`) dù dữ liệu Sheets API trả về vẫn đúng UTF-8 — đã set
  `sys.stdout.reconfigure(encoding="utf-8")` trong `sheet_io.py`, không phải
  lỗi dữ liệu nếu gặp lại lỗi này ở script khác.
- **Lỗi `403: access_denied` khi chạy `auth.py` lần đầu**: do OAuth consent
  screen ở chế độ "Testing" (User Type External) mà tài khoản đăng nhập chưa
  được thêm vào "Test users". Vào Cloud Console → APIs & Services → OAuth
  consent screen → thêm email vào Test users → chạy lại `auth.py`.
- **Robots.txt có thể "tồn tại + có Sitemap" (PASS theo skill 1) nhưng vẫn
  hỏng thật** nếu có ≥2 block `User-agent: *` chồng nhau (vd 1 block chặn
  thư mục, 1 block sau đó ghi đè bằng `Disallow:` rỗng của Yoast, vô hiệu
  hoá toàn bộ chặn trước đó). Đây là giới hạn đã biết của
  `check-onpage-co-ban/scripts/check_onpage.py` (chỉ check tồn tại +
  Sitemap, chưa parse xung đột nhiều block) — nếu thấy sheet ghi "Cần sửa"
  chi tiết hơn PASS của skill 1, **tin dữ liệu có sẵn trong sheet hơn**,
  không tự ý sửa đè bằng kết quả PASS của skill 1.

## Cấm

- **Cấm ghi vào ô ngoài cột đích** user đã chỉ định.
- **Cấm ghi đè ô đích đã có nội dung khác** mà chưa hỏi xác nhận.
- **Cấm đoán dòng khớp** khi tên checklist không trùng khớp rõ ràng — phải
  báo "không tìm thấy" thay vì chọn đại dòng gần giống.
- **Cấm hard-code** spreadsheet ID/gid cụ thể trong script dùng chung — luôn
  nhận từ input của user ở mỗi lần chạy.

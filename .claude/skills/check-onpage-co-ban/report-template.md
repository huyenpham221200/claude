# Report Template — Check Onpage Cơ Bản

Format bắt buộc cho output của SKILL `/check-onpage-co-ban`.

---

## 🔍 Báo cáo Check Onpage Cơ Bản — <domain>

**URL kiểm tra**: <URL cuối cùng sau redirect>
**Ngày check**: <YYYY-MM-DD>

---

## Kết quả

Cột "Ghi chú chi tiết" **không được rút gọn thành 1 câu chung chung** — phải
nêu đủ dữ kiện thật (URL cụ thể, giá trị meta tag cụ thể) và ý nghĩa thực tế,
theo đúng nguyên tắc ở `checklist-onpage.md`.

| Hạng mục | Checklist | Trạng thái | Ghi chú chi tiết |
|---|---|---|---|
| Domain | www & non-www / http & https | ✅/⚠️/❌ | <liệt kê URL cuối cùng của cả 4 biến thể, có/không hợp nhất, khuyến nghị bản chính> |
| Khả năng index | Robots.txt | ✅/⚠️/❌ | <có/không có Sitemap:, có dòng Disallow: / không> |
| Website metadata | OG tags | ✅/⚠️/❌ | <liệt kê tag nào có, tag nào thiếu> |
| Website metadata | Viewport | ✅/⚠️/❌ | <nguyên văn content thực tế> |
| Website metadata | Charset | ✅/⚠️/❌ | <charset thực tế> |
| Website metadata | Hreflang | ✅/⚠️/❌ | <có/không — nhắc rõ đây không mặc định là lỗi nếu site 1 ngôn ngữ> |

---

## Vấn đề cần xử lý

(Chỉ liệt kê các dòng ❌ hoặc ⚠️ thực sự cần hành động — Hreflang WARN do site
1 ngôn ngữ thì **không liệt kê** ở đây, chỉ note ở bảng trên.)

### 🔴 Cần sửa ngay

- **<tên checklist>**: <mô tả vấn đề> → **Tác động**: <vì sao quan trọng> →
  **Cách sửa**: <hướng dẫn cụ thể>.

### 🟡 Nên rà soát thêm

- **<tên checklist>**: <mô tả> → **Cách sửa**: <hướng dẫn>.

---

## Phần cần kiểm tra thủ công (ngoài phạm vi script)

- Redirect có phải 301 (vĩnh viễn) không, SSL còn hạn không — xem bằng
  `httpstatus.io`.
- Nội dung `sitemap.xml` (không trùng URL, cập nhật real-time) — dùng
  Screaming Frog hoặc Google Search Console.
- OG tags hiển thị thực tế khi share link — Facebook Sharing Debugger
  (`developers.facebook.com/tools/debug`).
- Viewport hiển thị thực tế trên nhiều thiết bị — test tay trên điện thoại
  hoặc Chrome DevTools.

---

## Ví dụ filled-in report

### 🔍 Báo cáo Check Onpage Cơ Bản — seongon.com

**URL kiểm tra**: https://seongon.com
**Ngày check**: 2026-07-05

### Kết quả

| Hạng mục | Checklist | Trạng thái | Ghi chú chi tiết |
|---|---|---|---|
| Domain | www & non-www / http & https | ⚠️ | Chỉ 2/4 phiên bản thống nhất về `https://seongon.com` — `http://seongon.com` và `https://www.seongon.com` chưa redirect về đúng bản chính |
| Khả năng index | Robots.txt | ✅ | Có robots.txt, có khai báo `Sitemap:` |
| Website metadata | OG tags | ⚠️ | Thiếu `og:image`, đã có 5/6 tag còn lại |
| Website metadata | Viewport | ✅ | `width=device-width, initial-scale=1.0` |
| Website metadata | Charset | ✅ | UTF-8 |
| Website metadata | Hreflang | ⚠️ | Không có — site chỉ chạy 1 ngôn ngữ nên **không cần fix** |

### Vấn đề cần xử lý

#### 🔴 Cần sửa ngay

- **Domain redirect**: `http://seongon.com` và `https://www.seongon.com`
  chưa redirect thẳng về `https://seongon.com`. → **Tác động**: Google có
  thể index trùng nhiều URL cho cùng nội dung, loãng thứ hạng. → **Cách
  sửa**: thêm rule redirect 301 ở server/CDN để cả 4 biến thể đều dẫn về
  đúng 1 URL chuẩn.

#### 🟡 Nên rà soát thêm

- **OG tags**: thiếu `og:image` → khi chia sẻ link lên Facebook/Zalo có thể
  không hiển thị ảnh preview. → **Cách sửa**: thêm thẻ
  `<meta property="og:image" content="...">` trỏ tới ảnh đại diện phù hợp.

### Phần cần kiểm tra thủ công

- Xác nhận redirect trên là 301 (không phải 302) bằng `httpstatus.io`.
- Verify hiển thị OG tags thực tế bằng Facebook Sharing Debugger sau khi bổ
  sung `og:image`.

---

### Ví dụ 2 — trường hợp FAIL (0/4 phiên bản hợp nhất)

### 🔍 Báo cáo Check Onpage Cơ Bản — damynghecattien.com

**URL kiểm tra**: https://damynghecattien.com/
**Ngày check**: 2026-07-05

### Kết quả

| Hạng mục | Checklist | Trạng thái | Ghi chú chi tiết |
|---|---|---|---|
| Domain | www & non-www / http & https | ❌ | Cả 4 phiên bản `http://damynghecattien.com/`, `https://damynghecattien.com/`, `http://www.damynghecattien.com/`, `https://www.damynghecattien.com/` đều đang tồn tại độc lập — không phiên bản nào redirect sang phiên bản khác |
| Khả năng index | Robots.txt | ✅ | Có robots.txt, có khai báo `Sitemap:` |
| Website metadata | OG tags | ⚠️ | Thiếu `og:image`, đã có 5/6 tag còn lại |
| Website metadata | Viewport | ✅ | `width=device-width, initial-scale=1` |
| Website metadata | Charset | ✅ | UTF-8 |
| Website metadata | Hreflang | ⚠️ | Không có — cần xác nhận site có đa ngôn ngữ không, nếu không thì bỏ qua |

### Vấn đề cần xử lý

#### 🔴 Cần sửa ngay

- **Domain chưa chuẩn hoá**: cả 4 bản sống song song, không cái nào redirect
  về cái nào. → **Tác động**: Google có thể coi đây là nhiều trang trùng nội
  dung, loãng thứ hạng/trust. → **Cách sửa**: chọn 1 bản chính thức (khuyến
  nghị `https://damynghecattien.com/` — đã đúng https, non-www), thêm rule
  redirect 301 từ 3 bản còn lại về bản này ở server/hosting.

#### 🟡 Nên rà soát thêm

- **OG tags**: thiếu `og:image` → có thể không hiện ảnh preview khi share
  link. → **Cách sửa**: thêm `<meta property="og:image" content="...">`.

### Phần cần kiểm tra thủ công

- Xác nhận site có đa ngôn ngữ không (nếu không thì Hreflang WARN bỏ qua
  được).
- Nếu cần biết chính xác Google đang index bản nào trong 4 bản trên — tự mở
  `google.com`, gõ `site:damynghecattien.com` (và các biến thể còn lại) bằng
  trình duyệt thật để đọc kết quả trực tiếp (skill không tự động hoá bước
  này — xem lý do ở `checklist-onpage.md`).

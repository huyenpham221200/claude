# Checklist: Onpage cơ bản

Đi tuần tự theo bảng dưới: **Hạng mục → Tên checklist → các bước check**
(mỗi bước nối bằng `>`). Chạy đúng thứ tự bước, không nhảy cóc — mỗi bước
cho ra 1 dữ kiện thật (từ script), bước cuối mới là kết luận trạng thái.

| Hạng mục | Tên checklist | Mô tả chi tiết cách check |
|---|---|---|
| 01. Domain | www & non-www / http & https | Chạy `scripts/check_onpage.py <url>` để lấy URL cuối cùng (sau redirect nếu có) của cả 4 biến thể `http://domain`, `https://domain`, `http://www.domain`, `https://www.domain` > So sánh 4 URL cuối cùng với nhau > Nếu ≥3/4 cùng dẫn về 1 URL duy nhất → **OK**, ghi rõ URL chuẩn đó là gì > Nếu chỉ 2/4 thống nhất → **WARN**, ghi rõ URL nào đang lệch, chưa redirect > Nếu mỗi URL trả về chính nó (0-1/4 thống nhất, không cái nào redirect) → **FAIL**, liệt kê đủ cả 4 URL đang tồn tại độc lập, giải thích rủi ro: nhiều URL cùng trỏ tới cùng 1 nội dung dễ bị Google coi là trùng lặp, loãng thứ hạng. |
| 02. Khả năng index | Robots.txt | Script fetch `<domain>/robots.txt` > Nếu status khác 200 (không tồn tại file) → **FAIL**, ghi "không có robots.txt" > Nếu có file, đọc nội dung tìm dòng `Disallow:` áp dụng cho `User-agent: *` > Nếu gặp `Disallow: /` (chặn toàn bộ site) → **FAIL nghiêm trọng**, ghi rõ đây là lỗi chặn Google index toàn site, cần sửa ngay > Nếu không bị chặn, tìm tiếp dòng `Sitemap:` > Có khai báo → **OK** > Không có khai báo → **WARN**, ghi "thiếu khai báo Sitemap: trong robots.txt". |
| 03. Website metadata | OG tags (Open Graph) | Script fetch HTML trang, tìm 6 meta property trong `<head>`: `og:locale`, `og:type`, `og:title`, `og:description`, `og:url`, `og:image` > Đếm số tag tìm thấy trong 6 tag trên > Đủ 6/6 → **OK** > Thiếu 1-2 tag → **WARN**, ghi rõ tên tag còn thiếu (thường gặp nhất là thiếu `og:image`) > Không có tag OG nào → **FAIL**. |
| 03. Website metadata | Viewport | Script tìm `<meta name="viewport">` trong `<head>` > Đọc giá trị `content` > Content có chứa `width=device-width` → **OK**, ghi lại nguyên văn content > Có thẻ viewport nhưng thiếu `width=device-width` → **WARN** > Không có thẻ viewport → **FAIL**. |
| 03. Website metadata | Charset | Script tìm `<meta charset="...">` hoặc `<meta http-equiv="Content-Type" content="...charset=...">` > Đọc giá trị charset tìm được > Là `UTF-8` (không phân biệt hoa/thường) → **OK** > Có khai báo nhưng khác UTF-8 → **WARN**, ghi rõ charset thực tế và rủi ro lỗi font tiếng Việt > Không khai báo charset nào → **FAIL**. |
| 03. Website metadata | Hreflang | Script tìm `<link rel="alternate" hreflang="..." href="...">` > Nếu tìm thấy → **OK**, liệt kê từng cặp `hreflang -> URL` > Nếu không tìm thấy thẻ nào → xác nhận với user/khách hàng site có đang chạy đa ngôn ngữ/đa khu vực không > Nếu site chỉ 1 ngôn ngữ → ghi "không áp dụng, bỏ qua, không tính là lỗi" > Nếu site có đa ngôn ngữ mà vẫn thiếu → **WARN thật**, cần bổ sung. |

## Nguyên tắc ghi chú tình trạng

Không dừng ở nhãn OK/WARN/FAIL đơn thuần — mỗi hạng mục phải ghi chú **tình
trạng thực tế bằng dữ kiện cụ thể** (URL nào, giá trị nào, tag nào), theo
đúng mẫu ở [`report-template.md`](report-template.md). Ví dụ với hạng mục
Domain khi FAIL:

> Cả 4 phiên bản `http://damynghecattien.com/`, `https://damynghecattien.com/`,
> `http://www.damynghecattien.com/`, `https://www.damynghecattien.com/` đều
> đang tồn tại độc lập, không phiên bản nào redirect sang phiên bản khác.
> → Cần chọn 1 bản chính thức (khuyến nghị bản `https + non-www`) và set
> redirect 301 từ 3 bản còn lại về bản đó.

## Giới hạn đã biết (không đưa vào tự động hoá)

- **Không dùng cú pháp `site:domain` để kiểm tra Google đã index bản nào**:
  tool tìm kiếm web hiện có (`WebSearch`) không mô phỏng đúng hành vi
  `site:` của Google thật — test thực tế cho thấy `site:damynghecattien.com`
  và `site:www.damynghecattien.com` trả về **kết quả giống hệt nhau**, và
  với domain không tồn tại thì tool tự fallback sang tìm kiếm từ khóa chung
  thay vì báo "không tìm thấy kết quả" như Google. Nếu cần biết chính xác
  bản nào đang được Google index, phải tự mở `google.com`, gõ `site:<url>`
  bằng trình duyệt thật và đọc kết quả trực tiếp — đây là việc làm thủ công,
  không có trong phạm vi tự động của skill này.
- Redirect có phải mã 301 (vĩnh viễn) hay 302 (tạm thời), SSL certificate
  còn hạn hay không — xem thêm bằng `httpstatus.io` nếu cần chắc chắn.

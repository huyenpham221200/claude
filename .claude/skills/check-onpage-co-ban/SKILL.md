---
name: check-onpage-co-ban
description: Kiểm tra onpage SEO cơ bản cho 1 URL — 3 hạng mục cốt lõi Domain (www/non-www, http/https), Khả năng index (robots.txt), Website metadata (OG tags, Viewport, Charset, Hreflang). Dùng khi user đưa 1 URL và muốn "check onpage cơ bản", "check onpage", "audit onpage", "rà soát onpage", hoặc gõ "/check-onpage-co-ban".
user-invokable: true
argument-hint: "<url> (vd: /check-onpage-co-ban https://example.com)"
license: MIT
metadata:
  author: SEONGON
  version: 2.0
  category: seo
---

# Check Onpage Cơ Bản

## Role

Bạn là trợ lý kiểm tra onpage SEO cho nhân sự SEONGON. Nhiệm vụ:
- Chạy script tự động lấy dữ kiện thật từ website (không đoán mò).
- Đối chiếu với `checklist-onpage.md` để biết PASS/WARN/FAIL nghĩa là gì.
- Xuất báo cáo theo đúng format `report-template.md`.

Phạm vi skill này **chỉ gồm 3 hạng mục cốt lõi** — Domain, Khả năng index
(robots.txt), Website metadata (OG tags/Viewport/Charset/Hreflang). Các hạng
mục onpage khác (Title, Meta description, Heading, Alt ảnh, Schema, URL
structure, Internal/External link, Sitemap.xml, Tốc độ...) **không thuộc
phạm vi skill này** — không tự ý mở rộng thêm.

## Khi nào được gọi

- User gõ `/check-onpage-co-ban <url>`.
- User đưa 1 URL và nói "check onpage giúp tôi", "audit onpage cơ bản", "rà
  soát domain/metadata cho site này".

## Quy trình 3 bước

### Bước 1 — Truy cập website

Chạy script để lấy toàn bộ dữ kiện thật cùng lúc (1 lần chạy, không cần gọi
lại cho từng hạng mục):

```
python "<đường dẫn skill>/scripts/check_onpage.py" <url>
```

Đường dẫn skill là thư mục chứa file `SKILL.md` này. Script chỉ dùng thư viện
chuẩn Python (không cần pip install), tự fetch URL (thử cả 4 biến thể
www/non-www × http/https), fetch `robots.txt`, và parse các meta tag cần
thiết.

Nếu script báo lỗi không tải được trang chính (`ERROR` khi fetch URL gốc):
báo lại cho user, hỏi lại URL hoặc kiểm tra kết nối — **không tự suy diễn**
kết quả.

### Bước 2 — Check lần lượt từng checklist

Mở [`checklist-onpage.md`](checklist-onpage.md) và đi **tuần tự đúng thứ tự
bảng trong đó**: mỗi dòng là 1 cặp Hạng mục → Tên checklist, cột thứ 3 là các
bước check nối bằng `>` — làm đúng từng bước, không nhảy cóc, không tự suy
diễn kết quả khi chưa đọc dữ kiện thật từ script.

Thứ tự bắt buộc:
1. **01. Domain** → `www & non-www / http & https`
2. **02. Khả năng index** → `Robots.txt`
3. **03. Website metadata** → `OG tags` → `Viewport` → `Charset` → `Hreflang`

Với mỗi checklist, sau khi đi hết các bước con, **ghi chú tình trạng chi
tiết** — không dừng ở nhãn OK/WARN/FAIL đơn thuần mà phải nêu rõ dữ kiện thật
(URL nào, giá trị meta tag nào, dòng robots.txt nào) và ý nghĩa thực tế của
nó. Ví dụ đúng chuẩn (hạng mục Domain, trường hợp FAIL):

> Cả 4 phiên bản `http://damynghecattien.com/`, `https://damynghecattien.com/`,
> `http://www.damynghecattien.com/`, `https://www.damynghecattien.com/` đều
> đang tồn tại độc lập, không phiên bản nào redirect sang phiên bản khác. →
> Cần chọn 1 bản chính thức (khuyến nghị `https + non-www`) và set redirect
> 301 từ 3 bản còn lại về bản đó.

Lưu ý đặc biệt khi đối chiếu:
- **Hreflang WARN không mặc định là lỗi** — chỉ là vấn đề thật nếu site có
  nhiều phiên bản ngôn ngữ/khu vực. Nếu không chắc, hỏi lại user thay vì tự
  kết luận là "thiếu".
- **Robots.txt FAIL do `Disallow: /`** là lỗi nghiêm trọng (chặn toàn site
  khỏi Google) — luôn xếp vào "Cần sửa ngay" nếu gặp.
- **Không tự ý dùng WebSearch để kiểm tra Google đã index URL nào** — xem lý
  do ở mục "Giới hạn đã biết" trong `checklist-onpage.md`. Đây là việc thủ
  công, để user tự làm bằng trình duyệt thật nếu cần.

### Bước 3 — Xuất báo cáo

Tổng hợp lại theo format trong [`report-template.md`](report-template.md):
bảng 4 cột (Hạng mục | Checklist | Trạng thái | Ghi chú chi tiết), phần "Vấn
đề cần xử lý" chỉ liệt kê dòng thực sự cần hành động, và phần "Cần kiểm tra
thủ công" nhắc các việc script không tự động hoá được (redirect có phải 301
không, OG tags hiển thị thực tế, Google đã index bản nào, v.v.).

Trả report này cho user trong chat như bình thường **và đồng thời** lưu 1 bản
y hệt ra file, để không mất kết quả các lần chạy trước:

```
mkdir -p ~/.claude/output/check-onpage-co-ban
python -c "import datetime; print(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))"
```

Ghi report vừa tạo vào:
```
~/.claude/output/check-onpage-co-ban/<timestamp>.md
```
(vd `~/.claude/output/check-onpage-co-ban/2026-07-05_14-30.md`). Mỗi lần chạy
skill là 1 file mới theo timestamp lúc chạy — **không ghi đè** file của lần
chạy trước.

## Tiêu chí chất lượng

Trước khi đưa report cho user, tự check:
- [ ] Đã chạy script thật, không bịa số liệu.
- [ ] Đủ cả 3 hạng mục / 6 checklist trong bảng.
- [ ] Hreflang WARN (nếu có) không bị gắn nhãn "lỗi" khi chưa xác nhận site
      có đa ngôn ngữ.
- [ ] Mỗi vấn đề ❌/⚠️ có tác động + cách sửa cụ thể, không nói chung chung.
- [ ] Có nhắc phần cần kiểm tra thủ công.
- [ ] Report không quá dài dòng — ưu tiên bảng, gạch đầu dòng.
- [ ] Đã lưu 1 bản report ra `~/.claude/output/check-onpage-co-ban/<timestamp>.md`,
      không ghi đè file lần chạy trước.

## Quy tắc đặc biệt

### Khi user đưa domain trần (không có http/https)

Tự thêm `https://` trước khi chạy script.

### Khi user hỏi thêm về hạng mục ngoài phạm vi

Nếu user hỏi thêm về Title, Meta description, Heading, Alt ảnh, Schema,
Sitemap.xml, Tốc độ... — trả lời rằng các hạng mục này nằm ngoài phạm vi
skill `check-onpage-co-ban` (skill khác sẽ phụ trách), không tự mở rộng
script để check thêm.

### Khi site đã đạt hết 3 hạng mục

Khen ngợi ngắn gọn, không cần bịa thêm vấn đề để báo cáo trông "đầy đủ" hơn.

## Vết xe đổ — lỗi thường gặp

Ghi lại các trường hợp dễ hiểu sai khi đọc output script, để không lặp lại.
Bổ sung thêm mỗi khi gặp case mới trong thực tế.

- **Site không redirect biến thể nào cả (như `damynghecattien.com`,
  2026-07-05)**: cả 4 URL `http/https × www/non-www` đều trả về chính nó,
  không cái nào redirect sang cái nào. Đây **không phải lỗi của script** —
  script đang báo đúng: site thực sự chưa chuẩn hoá domain, Google có thể
  đang index trùng nhiều URL. Đừng nghi ngờ script khi thấy kết quả này, xử
  lý như 1 FAIL thật.
- **`ERROR` không đồng nghĩa với "site lỗi"**: một số site có WAF/CDN
  (Cloudflare, Sucuri...) chặn request có User-Agent lạ (script dùng UA
  `SEONGON-OnpageChecker/1.0`) và trả về 403/Access Denied dù site vẫn chạy
  bình thường với trình duyệt thật. Nếu gặp `ERROR` hoặc status lạ (403,
  503...), thử mở lại URL đó bằng trình duyệt thường trước khi kết luận site
  down.
- **Timeout giả trên site chậm**: script chờ tối đa 12 giây/request. Site
  hosting yếu hoặc đang cao điểm có thể timeout dù bình thường vẫn tải được
  (chỉ chậm). Nếu 1 trong 4 biến thể domain bị timeout còn lại thì OK, thử
  chạy lại script 1 lần nữa trước khi báo FAIL toàn bộ.
- **OG tags/meta tag "thiếu" trên site SPA/React render bằng JS**: script chỉ
  đọc HTML tĩnh trả về ban đầu (chưa chạy JavaScript). Nếu site dùng
  client-side rendering, các meta tag do JS chèn vào sau sẽ **không được
  script nhìn thấy** dù thực tế có tồn tại. Nếu nghi ngờ (site là SPA), xác
  nhận thêm bằng "View Page Source" (Ctrl+U) trong trình duyệt trước khi báo
  FAIL.
- **`robots.txt` tồn tại không có nghĩa là an toàn**: dễ chỉ nhìn "có
  robots.txt → PASS" mà bỏ qua nội dung. Luôn đọc kỹ dòng `Disallow: /` —
  nếu có, đây là FAIL nghiêm trọng dù file vẫn "tồn tại" bình thường.
- **Script chưa phát hiện được xung đột nhiều block `User-agent: *`** (phát
  hiện thực tế trên `damynghecattien.com`, 2026-07-05, qua đối chiếu với
  Google Sheet tracking của khách): robots.txt có 2 block `User-agent: *`,
  block đầu chặn vài thư mục nhưng block sau (do Yoast SEO tự sinh) ghi
  `Disallow:` rỗng → ghi đè, vô hiệu hoá toàn bộ chặn trước đó, site gần như
  mở toàn bộ cho crawl. Script hiện tại chỉ check "có file + có khai báo
  Sitemap:" nên báo PASS, **không phát hiện được** kiểu lỗi này. Nếu có dữ
  liệu tay (Screaming Frog, hoặc sheet tracking khác) cho thấy chi tiết hơn
  PASS của script — ưu tiên tin dữ liệu đó hơn.

## Cấm

- **Cấm bịa kết quả** khi chưa chạy được script — phải báo lỗi rõ ràng.
- **Cấm tự ý thêm hạng mục** ngoài Domain / Robots.txt / Metadata (OG,
  Viewport, Charset, Hreflang).
- **Cấm gắn nhãn "lỗi"** cho Hreflang WARN khi chưa xác nhận site có đa ngôn
  ngữ.
- **Cấm sửa code/website của user** trong lúc audit — chỉ đọc và báo cáo.

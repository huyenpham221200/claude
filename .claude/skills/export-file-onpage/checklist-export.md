# Hướng dẫn: tìm đúng dòng để ghi

## Bước dò cấu trúc sheet (làm mẫu từ ví dụ thật đã test)

Sheet test: `https://docs.google.com/spreadsheets/d/1E2_GMLOdEzBgNpPRLf7cpGN5fbpGmyF4DgyObVOLCv4/edit?gid=56626959`

Đọc `A1:L15` trả về (rút gọn):

```
Dòng 1-5: dashboard tổng hợp (Hạng mục / Số lượng / Hoàn thành...) — bỏ qua.
Dòng 6: trống.
Dòng 7: STT | Các vấn đề cần kiểm tra | (trống) | Chi tiết | Trạng thái | ... ← ĐÂY LÀ DÒNG HEADER
Dòng 8-10: các mục không thuộc phạm vi skill (hiển thị ảnh, bộ lọc sản phẩm...) — STT là số (0, 0, 0).
Dòng 11: STT=1 | Domain | www & non-www | ...          ← khớp checklist "www & non-www"
Dòng 12: STT=2 | (trống) | http & https | ...           ← khớp checklist "http & https"
Dòng 14: STT=4 | Khả năng index | robots.txt | ...       ← khớp checklist "Robots.txt"
```

**Cách nhận diện dòng header đúng**: dòng mà cột đầu tiên (STT) là chữ (`STT`)
thay vì số, và các cột liền kề đều có nhãn ngắn gọn kiểu tiêu đề (`Chi tiết`,
`Trạng thái`...).

**Cách nhận diện cột "Tên checklist"**: đi cùng cột "Hạng mục" bên trái (ở
ví dụ này là cột B "Các vấn đề cần kiểm tra" = Hạng mục, cột C = Tên
checklist) — kiểm tra bằng cách xem giá trị trong cột có khớp với tên các
checklist đã biết từ `check-onpage-co-ban` không (`www & non-www`, `http &
https`, `robots.txt`, `OG tags`, `viewport`, `Charset`, `hreflang` — so
sánh không phân biệt hoa/thường).

## Bảng map: checklist skill 1 ↔ tên trong sheet (ví dụ thật)

| Checklist (check-onpage-co-ban) | Tên trong sheet (cột C) | Dòng (ví dụ thật) |
|---|---|---|
| Domain — www & non-www / http & https | `www & non-www` **và** `http & https` (2 dòng riêng) | 11 và 12 |
| Khả năng index — Robots.txt | `robots.txt` | 14 |
| Website metadata — OG tags | `OG tags` | 44 |
| Website metadata — Viewport | `viewport` | 45 |
| Website metadata — Charset | `Charset` (có thể có khoảng trắng thừa cuối, nhớ `.strip()`) | 46 |
| Website metadata — Hreflang | `hreflang` | 47 |

**Lưu ý**: số dòng trên chỉ đúng với sheet test cụ thể này. Với sheet khác,
KHÔNG dùng lại số dòng này — luôn đọc lại từ đầu theo Bước 2 của SKILL.md.

## Ghi header cột đích

Cột đích ghi ở CÙNG dòng header đã xác định (dòng 7 trong ví dụ trên), ví
dụ ô `L7` = `Check lần 2`. Không ghi header ở dòng 1 hay dòng 2 một cách máy
móc — phải là đúng dòng header thật của sheet đó.

## Ví dụ lệnh thực tế đã chạy thành công

```
python scripts/sheet_io.py write "<link sheet>" --range "L7" --values '[["Check lần 2"]]'
python scripts/sheet_io.py write "<link sheet>" --range "L11" --values '[["<ghi chú Domain>"]]'
python scripts/sheet_io.py write "<link sheet>" --range "L12" --values '[["<ghi chú Domain>"]]'
python scripts/sheet_io.py write "<link sheet>" --range "L14" --values '[["<ghi chú Robots.txt>"]]'
python scripts/sheet_io.py write "<link sheet>" --range "L44" --values '[["<ghi chú OG tags>"]]'
python scripts/sheet_io.py write "<link sheet>" --range "L45" --values '[["<ghi chú Viewport>"]]'
python scripts/sheet_io.py write "<link sheet>" --range "L46" --values '[["<ghi chú Charset>"]]'
python scripts/sheet_io.py write "<link sheet>" --range "L47" --values '[["<ghi chú Hreflang>"]]'
```

## Xác nhận lại sau khi ghi

Đọc lại theo cặp cột Tên-checklist + cột-đích để confirm đúng dòng:

```
python scripts/sheet_io.py read "<link sheet>" --range "C11:L12"
python scripts/sheet_io.py read "<link sheet>" --range "C14:L14"
python scripts/sheet_io.py read "<link sheet>" --range "C44:L47"
```

So khớp giá trị cột C (tên checklist) với nội dung vừa ghi ở cột đích —
nếu khớp đúng dòng thì mới báo thành công cho user.

# Belt Tension Dashboard 2026

Dashboard สรุปผลตรวจวัดแรงตึงสายพาน (Check List of Belt Tension) รายเดือน ม.ค.–ต.ค. 2026

- `index.html` — dashboard (HTML/SVG ล้วน ไม่ต้องติดตั้งอะไร)
- `data/tension.db` — ฐานข้อมูล SQLite ที่ดึงจากไฟล์ Excel (dashboard อ่านไฟล์นี้ทุกครั้งที่เปิดหรือกด Refresh)
- `scripts/parse_excel.py` — แปลง Excel → SQLite
- `scripts/sync.py` / `sync.bat` — สร้าง SQLite ใหม่แล้ว push ขึ้น GitHub (เฉพาะเมื่อข้อมูลเปลี่ยน)

## อัปเดตข้อมูลเดือนใหม่

วางไฟล์ Excel ในโฟลเดอร์ `<ปี>/<เลขเดือน> ...` ของโฟลเดอร์หลัก (เช่น `2026/11 Nov 2026/`) แล้วดับเบิลคลิก `sync.bat` หรือรัน

```bash
python scripts/sync.py
```

จากนั้นกดปุ่ม **⟳ Refresh ข้อมูล** บน dashboard จะเห็นข้อมูลใหม่ทันที (ต้องติดตั้ง `openpyxl` และ login `gh auth login` ไว้ก่อน)

## ตาราง SQLite

- `reports` — 1 แถวต่อเดือน (year, month_idx, month, date, file)
- `lines` — ค่าแรงตึงรายไลน์ (std, before, after, noload_run, load, helix_ton, remark, standby …)
- `machines` — ค่าแรงดันเครื่องจักร bar (machine, location, std, left, right, remark)
- `meta` — updated_at, content_hash
## เกณฑ์สถานะ

เทียบแรงตึงจริงกับค่ามาตรฐาน 100%: ปกติ ±5% · เฝ้าระวัง ±5–10% · ผิดเกณฑ์ เกิน ±10%

# Belt Tension Dashboard 2026

Dashboard สรุปผลตรวจวัดแรงตึงสายพาน (Check List of Belt Tension) รายเดือน ม.ค.–ต.ค. 2026

- `index.html` — dashboard (HTML/SVG ล้วน ไม่ต้องติดตั้งอะไร)
- `data/tension.json`, `data/tension.js` — ข้อมูลที่ดึงจากไฟล์ Excel
- `scripts/parse_excel.py` — สคริปต์แปลง Excel → JSON

## อัปเดตข้อมูลเดือนใหม่

วางไฟล์ Excel ในโฟลเดอร์ `2026/<เลขเดือน> ...` ของโฟลเดอร์หลัก แล้วรัน

```bash
pip install openpyxl
python scripts/parse_excel.py .. data/tension.json
```

## เกณฑ์สถานะ

เทียบแรงตึงจริงกับค่ามาตรฐาน 100%: ปกติ ±5% · เฝ้าระวัง ±5–10% · ผิดเกณฑ์ เกิน ±10%

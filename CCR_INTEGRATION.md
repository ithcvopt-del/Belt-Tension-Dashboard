# เพิ่มเมนู Belt Tension ใน ccr.ith.co.th

เมนูด้านซ้ายของ ccr.ith.co.th ถูกเขียนไว้ในโค้ด (Next.js) ต้องแก้ใน source แล้ว deploy ใหม่
ส่งไฟล์นี้ให้ผู้ดูแลเว็บ CCR ได้เลย

Dashboard: https://ithcvopt-del.github.io/Belt-Tension-Dashboard/
(GitHub Pages ไม่ได้ส่ง `X-Frame-Options` / `frame-ancestors` จึงฝังด้วย iframe ได้)

## 1. เพิ่มรายการในเมนู

ในไฟล์ sidebar ที่มีอาร์เรย์เมนู ให้เพิ่มต่อจาก `22 kV Load (MDS)`:

```tsx
{ href: "/load22kv", label: "22 kV Load (MDS)", icon: Activity, tone: "load" },
{ href: "/tension",  label: "Belt Tension",     icon: Gauge,    tone: "load" }, // ← เพิ่ม
```

(`Gauge` มาจาก `lucide-react` หรือเลือกไอคอน/สี `tone` ตามที่เว็บมีอยู่)

## 2. สร้างหน้า `/tension`

`app/tension/page.tsx`

```tsx
export const metadata = { title: "Belt Tension - CCR Dashboard" };

const SRC = "https://ithcvopt-del.github.io/Belt-Tension-Dashboard/";

export default function TensionPage() {
  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      <div className="flex items-center justify-between px-4 py-3">
        <h1 className="text-lg font-semibold">Belt Tension Dashboard</h1>
        <a href={SRC} target="_blank" rel="noopener" className="text-sm underline">เปิดหน้าเต็ม ↗</a>
      </div>
      <iframe src={SRC} title="Belt Tension Dashboard" className="flex-1 w-full border-0" />
    </div>
  );
}
```

ถ้าเว็บกำหนด Content-Security-Policy ไว้ ให้เพิ่ม `frame-src https://ithcvopt-del.github.io` ด้วย
และถ้าหน้าอื่นอยู่หลัง login (Keycloak) ให้ใส่ `/tension` ใน matcher ของ middleware แบบเดียวกับ `/load22kv`

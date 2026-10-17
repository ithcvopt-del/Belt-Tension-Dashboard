"""Parse monthly Belt Tension Report workbooks into data/tension.json."""
import glob, json, os, re, sys
import openpyxl

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
LEVELS = [1.10, 1.05, 1.03, 1.00, 0.90, 0.80, 0.70]

def num(v):
    return float(v) if isinstance(v, (int, float)) else None

def text(v):
    return v.strip() if isinstance(v, str) and v.strip() not in ("", "-") else None

def parse(path, month_idx):
    ws = openpyxl.load_workbook(path, data_only=True, read_only=True).worksheets[0]
    rows = [list(r) + [None] * 25 for r in ws.iter_rows(values_only=True)]
    date = None
    for r in rows[:4]:
        m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", str(r[0] or ""))
        if m:
            date = f"{m[3]}-{int(m[2]):02d}-{int(m[1]):02d}"
    lines, machines, section, machine = [], [], None, None
    for r in rows:
        c0 = r[0]
        if c0 == "Location (Line no.)": section = "line"; continue
        if c0 == "Location (Machine)": section = "machine"; continue
        if section == "line":
            if not isinstance(c0, str) or not re.match(r"^[A-Z]\d", c0):
                if c0 is None and r[1] is None and r[12] is None and lines: section = None
                continue
            std = num(r[8])
            # CCR placeholders (0.2 t) mean the load cell could not be read
            ccr = lambda v: None if v is None or v < 0.5 else v
            lines.append(dict(
                id=c0, length=num(r[1]), lift_h=num(r[2]), lift_t=num(r[3]), lift_diff=num(r[4]),
                std=std, std_levels=[num(x) for x in r[5:12]],
                before=num(r[12]), after=num(r[13]),
                noload_stop=ccr(num(r[14])), noload_run=ccr(num(r[15])), load=ccr(num(r[16])),
                helix_kn=num(r[19]), helix_ton=num(r[20]), remark=text(r[21]),
                standby=(text(r[21]) or "").lower() == "standby" or r[1] == "-",
            ))
        elif section == "machine":
            if c0 is None and r[2] is None:
                if machines: section = None
                continue
            if isinstance(c0, str) and c0.startswith(("Reported", "Checked")): section = None; continue
            if c0: machine = c0.strip()
            if r[2] is None: continue
            machines.append(dict(
                machine=machine, location=r[2].strip(), std=num(r[8]),
                std_levels=[num(x) for x in r[5:12]],
                left=num(r[12]), right=num(r[13]), remark=text(r[19]),
            ))
    return dict(month=MONTHS[month_idx], month_idx=month_idx, date=date,
                file=os.path.relpath(path, sys.argv[1]).replace("\\", "/"),
                lines=lines, machines=machines)

def main():
    root, out = sys.argv[1], sys.argv[2]
    reports = []
    for p in glob.glob(os.path.join(root, "2026", "*", "*.xlsx")):
        folder = os.path.basename(os.path.dirname(p))
        m = re.match(r"(\d{2})", folder)
        if m and not os.path.basename(p).startswith("~$"):
            reports.append(parse(p, int(m[1]) - 1))
    reports.sort(key=lambda r: r["month_idx"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    data = dict(year=2026, levels=LEVELS, reports=reports)
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # Same data as a script so index.html also works when opened straight from disk
    with open(os.path.splitext(out)[0] + ".js", "w", encoding="utf-8") as f:
        f.write("window.TENSION_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n")
    for r in reports:
        print(r["month"], r["date"], len(r["lines"]), "lines", len(r["machines"]), "machine pts")

if __name__ == "__main__":
    main()

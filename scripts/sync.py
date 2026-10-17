"""Rebuild data/tension.db from the Excel folders and push it to GitHub if anything changed.

Usage (from anywhere):  python scripts/sync.py [excel_root]
excel_root defaults to the folder that contains this repo (the one holding 2026/, 2027/, ...).
"""
import os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(REPO, "data", "tension.db")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parse_excel  # noqa: E402

def git(*args):
    # safe.directory: the repo sits on a network share owned by another account
    return subprocess.run(["git", "-c", "safe.directory=*", "-C", REPO, *args],
                          check=True, capture_output=True, text=True).stdout.strip()

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(REPO)
    reports = parse_excel.collect(root)
    if not reports:
        sys.exit(f"No Excel reports found under {root}")
    old = parse_excel.read_hash(DB)
    new = parse_excel.write_db(reports, DB)
    last = reports[-1]
    print(f"{len(reports)} reports, latest {last['month']} {last['year']} ({last['date']})")
    if old == new:
        git("checkout", "--", "data/tension.db")  # only the timestamp changed; keep the committed file
        print("No data changes - nothing to push.")
        return
    git("add", "data/tension.db")
    git("commit", "-m", f"Update tension data (latest {last['month']} {last['year']})")
    git("pull", "--rebase", "--quiet")
    git("push", "--quiet")
    print("Pushed updated data/tension.db to GitHub.")

if __name__ == "__main__":
    main()

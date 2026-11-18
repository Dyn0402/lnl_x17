"""Build the feasibility-run page for dylan-cern-site.

    python3 site/build_page.py [--site ~/PycharmProjects/dylan-cern-site]

1. runs planning/plan.py (which reruns two_arm_estimates.py) -> planning/out/plan.json;
2. writes site/out/lnl-feasibility.html (template + data);
3. if the site checkout exists: copies it to pages/facilities/lnl-feasibility.html and the proposal
   PDF + LaTeX zip to facilities/lnl/ (served next to the page; the Overleaf project is linked from plan.py LINKS).

Then, in the site repo: python3 scripts/build.py && scripts/deploy-eos.sh (or rsync the three files).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "out"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=str(Path.home() / "PycharmProjects" / "dylan-cern-site"))
    a = ap.parse_args()
    subprocess.run([sys.executable, str(ROOT / "planning" / "plan.py")], check=True, stdout=subprocess.DEVNULL)
    data = json.loads((ROOT / "planning" / "out" / "plan.json").read_text(encoding="utf-8"))
    tpl = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
    html = tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "lnl-feasibility.html").write_text(html, encoding="utf-8")
    print("wrote", OUT / "lnl-feasibility.html")

    site = Path(a.site).expanduser()
    if not site.is_dir():
        print("no site checkout at", site, "- skipped the copy")
        return
    (site / "pages" / "facilities" / "lnl-feasibility.html").write_text(html, encoding="utf-8")
    dst = site / "facilities" / "lnl"
    dst.mkdir(parents=True, exist_ok=True)
    pdf = ROOT / "proposal" / "latex" / "proposal.pdf"
    zp = ROOT / "proposal" / "out" / "lnl_x17_pac_proposal.zip"
    for src, name in [(pdf, "lnl_x17_pac_proposal.pdf"), (zp, "lnl_x17_pac_proposal.zip")]:
        if src.exists():
            shutil.copy2(src, dst / name)
            print("copied", name, "->", dst)
        else:
            print("missing", src, "(run make zip in proposal/latex)")


if __name__ == "__main__":
    main()

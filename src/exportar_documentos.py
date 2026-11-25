"""Exporta relatórios Markdown do repositório em PDF e DOCX com gráficos anexos."""
from pathlib import Path
import re
import markdown
from weasyprint import HTML
from docx import Document
from docx.shared import Cm, Pt
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "docs/escopo-1/AE2-2/PLANEJAMENTO.md",
    ROOT / "entrega-final/docs/escopo-1/AE2-2/PLANEJAMENTO.md",
    ROOT / "docs/escopo-1/AE1-2/RELATORIO_FINAL.md",
    ROOT / "entrega-final/docs/escopo-1/AE1-2/RELATORIO_FINAL.md",
    ROOT / "docs/final/RELATORIO_FINAL.md",
    ROOT / "entrega-final/docs/final/RELATORIO_FINAL.md",
]
CSS = """
@page { size: A4; margin: 17mm 18mm; }
body { font-family: DejaVu Sans, Arial, sans-serif; font-size: 9pt; color: #1c2930; line-height: 1.35; }
h1 { color: #234e62; font-size: 17pt; margin-bottom: 10px; }
h2 { color: #234e62; font-size: 11pt; margin-top: 18px; }
h3 { color: #234e62; font-size: 10pt; }
table { border-collapse: collapse; font-size: 8pt; width: 100%; margin: 9px 0 13px; }
th,td { border: 1px solid #c4d2d9; padding: 5px; vertical-align: top; }
th { background: #e4eef3; }
img { max-width: 100%; max-height: 140mm; object-fit: contain; }
blockquote { border-left: 3px solid #789cae; padding: 7px 13px; color: #42555f; }
code { font-size: 8pt; }
p { margin: 5px 0 8px; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; font-size: 7.5pt; line-height: 1.2; padding: 5px 7px; background: #f5f8fa; }
h2, h3, table thead { break-after: avoid; }
tr { break-inside: avoid; }
"""
def simplify(s):
    return re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1",
        re.sub(r"`([^\x60]+)`", r"\1", re.sub(r"\*\*(.*?)\*\*", r"\1", s))).strip()

def export(src):
    out_pdf=src.with_suffix(".pdf")
    out_docx=src.with_suffix(".docx")
    raw=src.read_text(encoding="utf-8")
    body=markdown.markdown(raw, extensions=["tables","fenced_code"])
    html=f"<html><meta charset='utf-8'><style>{CSS}</style><body>{body}</body></html>"
    HTML(string=html,base_url=str(src.parent)).write_pdf(str(out_pdf))
    d=Document()
    sec=d.sections[0]
    sec.top_margin=Cm(1.6);sec.bottom_margin=Cm(1.6)
    sec.left_margin=Cm(2);sec.right_margin=Cm(2)
    d.styles["Normal"].font.size=Pt(9)
    lines=raw.splitlines()
    i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:
            i+=1;continue
        if line.startswith("!["):
            m=re.match(r"!\[([^]]*)\]\(([^)]+)\)",line)
            if m:
                p=(src.parent/m.group(2)).resolve()
                if p.suffix.lower()==".svg":
                    png=p.with_suffix(".export.png")
                    cairosvg.svg2png(url=str(p),write_to=str(png),output_width=950)
                    d.add_picture(str(png),width=Cm(16))
                    png.unlink()
                elif p.exists(): d.add_picture(str(p),width=Cm(16))
            i+=1;continue
        if line.startswith("|") and i+1<len(lines) and re.match(r"^\|[\s:\-|]+\|$",lines[i+1].strip()):
            heads=[simplify(c) for c in line.strip("|").split("|")]
            i+=2; data=[]
            while i<len(lines) and lines[i].strip().startswith("|"):
                data.append([simplify(c) for c in lines[i].strip().strip("|").split("|")])
                i+=1
            t=d.add_table(rows=1,cols=len(heads));t.style="Light Shading Accent 1"
            for j,v in enumerate(heads): t.rows[0].cells[j].text=v
            for row in data:
                c=t.add_row().cells
                for j,v in enumerate(row[:len(c)]):c[j].text=v
            continue
        if line.startswith("#"):
            level=len(line)-len(line.lstrip("#"))
            d.add_heading(simplify(line.lstrip("# ")),level=min(level,3))
        elif line.startswith("- "):
            d.add_paragraph(simplify(line[2:]),style="List Bullet")
        elif re.match(r"^\d+\. ",line):
            d.add_paragraph(simplify(re.sub(r"^\d+\. ","",line)),style="List Number")
        else:
            d.add_paragraph(simplify(line.replace("> ","")))
        i+=1
    d.save(out_docx)
    print(f"Exportado: {out_pdf.relative_to(ROOT)} e {out_docx.relative_to(ROOT)}")

if __name__=="__main__":
    for f in SOURCES: export(f)

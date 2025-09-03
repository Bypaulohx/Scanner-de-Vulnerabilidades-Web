
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

def _md_section(title: str) -> str:
    return f"# {title}\n\n"

def _md_table(rows: List[Dict], headers: List[str]) -> str:
    if not rows:
        return "Nenhum resultado.\n\n"
    head = " | ".join(headers)
    sep = " | ".join(["---"] * len(headers))
    body = "\n".join([" | ".join(str(r.get(h, "")) for h in headers) for r in rows])
    return f"{head}\n{sep}\n{body}\n\n"

def to_markdown(results: List[Dict]) -> str:
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    md = _md_section("Relatório de Varredura Web")
    md += f"Gerado em: **{ts}**\n\n"
    for r in results:
        md += _md_section(r["type"].upper())
        if r["type"] in ("xss", "sqli"):
            md += f"Alvos testados: **{r.get('tested', 0)}**\n\n"
            md += _md_table(r.get("findings", []), ["param", "payload", "url", "evidence"])
        elif r["type"] == "headers":
            md += "Cabeçalhos ausentes:\n\n"
            md += _md_table(r.get("missing", []), ["header", "hint"])
            md += "Observações:\n\n"
            md += "\n".join(f"- {n}" for n in r.get("notes", [])) + "\n\n"
    return md

def save_reports(results: List[Dict], outdir: str = "reports", basename: str = "scan") -> Dict[str, str]:
    Path(outdir).mkdir(parents=True, exist_ok=True)
    json_path = str(Path(outdir) / f"{basename}.json")
    md_path = str(Path(outdir) / f"{basename}.md")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(to_markdown(results))
    return {"json": json_path, "markdown": md_path}

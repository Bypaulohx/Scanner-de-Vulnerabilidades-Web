
import argparse
from .core import build_session, normalize_url
from .checks import scan_xss, scan_sqli, scan_headers
from .reporting import save_reports

def parse_args():
    p = argparse.ArgumentParser(
        prog="webscan",
        description="Scanner simples de vulnerabilidades (XSS, SQLi, headers inseguros)"
    )
    p.add_argument("-u", "--url", required=True, help="URL alvo (ex: https://site.com/page.php?id=1)")
    p.add_argument("--no-xss", action="store_true", help="Não executar teste de XSS")
    p.add_argument("--no-sqli", action="store_true", help="Não executar teste de SQLi")
    p.add_argument("--no-headers", action="store_true", help="Não checar headers de segurança")
    p.add_argument("--timeout", type=float, default=10.0, help="Timeout das requisições (s)")
    p.add_argument("--insecure", action="store_true", help="Não verificar TLS/SSL (verify=False)")
    p.add_argument("--report-dir", default="reports", help="Pasta para salvar relatórios")
    p.add_argument("--basename", default="scan", help="Nome base dos arquivos de relatório")
    return p.parse_args()

def main():
    args = parse_args()
    url = normalize_url(args.url)
    session = build_session(timeout=args.timeout, verify_tls=not args.insecure)

    results = []

    if not args.no_headers:
        print("[*] Checando headers de segurança...")
        results.append(scan_headers(session, url))

    if not args.no_xss:
        print("[*] Testando XSS refletido...")
        results.append(scan_xss(session, url))

    if not args.no_sqli:
        print("[*] Testando SQL injection...")
        results.append(scan_sqli(session, url))

    paths = save_reports(results, outdir=args.report_dir, basename=args.basename)
    print(f"[+] Relatórios salvos: {paths['json']} e {paths['markdown']}")

if __name__ == "__main__":
    main()

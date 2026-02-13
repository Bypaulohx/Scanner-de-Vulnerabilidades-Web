
# Arquitetura Detalhada

- `scanner/core.py`: cliente HTTP com `requests`, normalização de URL e utilidades de detecção.
- `scanner/checks/*.py`: módulos independentes para cada tipo de teste (XSS, SQLi, Headers).
- `scanner/reporting/report.py`: geração de relatórios em **JSON** e **Markdown**.
- `scanner/cli.py`: interface de linha de comando.

Decisões:
- Foco em **simplicidade** e **legibilidade**.
- Dependência mínima (apenas `requests`).

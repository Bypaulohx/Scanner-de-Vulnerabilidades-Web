# WebVulnScanner (Python)

Ferramenta estilo **Nikto** (bem mais simples) que verifica falhas comuns em aplicações web:
- **XSS refletido**
- **SQL Injection (erro-based)**
- **Headers de segurança ausentes**

> ⚠️ **Uso ético**: utilize **somente** em sistemas que você possui autorização explícita para testar.

---

## Arquitetura

```mermaid
flowchart TD
    A[CLI (argparse)] --> B[Core (requests Session)]
    B --> C[XSS Check]
    B --> D[SQLi Check]
    B --> E[Headers Check]
    C --> F[Results]
    D --> F[Results]
    E --> F[Results]
    F --> G[Reporting (JSON/Markdown)]
```

Estrutura de pastas:

```
webvulnscanner/
  scanner/
    checks/
      xss.py
      sqli.py
      headers.py
      common.py
    reporting/
      report.py
    core.py
    cli.py
  tests/
  README.md
  requirements.txt
```

---

## Passo a passo no VSCode

1. **Criar e abrir a pasta do projeto**
   ```bash
   mkdir webvulnscanner && cd webvulnscanner
   ```

2. **Criar ambiente virtual e ativar**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   # ou via pyproject
   pip install .
   ```

4. **Configurar o VSCode**
   - Abra a pasta `webvulnscanner` no VSCode.
   - Selecione o interpretador Python da `.venv` (Ctrl+Shift+P → "Python: Select Interpreter").
   - Opcional: instale extensões **Python** e **Pylance**.

5. **Executar o scanner (exemplos)**
   ```bash
   # checar apenas headers
   python -m scanner.cli -u https://exemplo.com --no-xss --no-sqli

   # rodar tudo e salvar relatórios na pasta padrão "reports/"
   python -m scanner.cli -u "https://exemplo.com/produto.php?id=1"

   # binário via entrypoint (após pip install .)
   webscan -u https://exemplo.com
   ```

6. **Ver relatórios**
   - JSON: `reports/scan.json`
   - Markdown: `reports/scan.md`

7. **Rodar testes (opcional)**
   ```bash
   python -m pytest -q
   ```

---

## Como funciona

- **XSS**: injeta payloads em parâmetros de query (reais e comuns) e verifica **reflexão do payload** (incluindo encoding simples).
- **SQLi**: injeta payloads clássicos e procura **assinaturas de erro de banco** na resposta.
- **Headers**: verifica presença dos cabeçalhos recomendados (CSP, X-Frame-Options, etc.) e anota observações.

> Limitações: não faz *crawler*, não autentica, não executa *DOM-based XSS*, não faz *time-based blind SQLi*, etc. É intencionalmente simples.

---

## Opções de linha de comando

```
usage: webscan [-h] -u URL [--no-xss] [--no-sqli] [--no-headers] [--timeout TIMEOUT]
               [--insecure] [--report-dir REPORT_DIR] [--basename BASENAME]

Scanner simples de vulnerabilidades (XSS, SQLi, headers inseguros)

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL alvo (ex: https://site.com/page.php?id=1)
  --no-xss              Não executar teste de XSS
  --no-sqli             Não executar teste de SQLi
  --no-headers          Não checar headers de segurança
  --timeout TIMEOUT     Timeout das requisições (s)
  --insecure            Não verificar TLS/SSL (verify=False)
  --report-dir REPORT_DIR
                        Pasta para salvar relatórios
  --basename BASENAME   Nome base dos arquivos de relatório
```

---

## Aviso Legal

Não me **responsabilizo** por usos indevidos. Teste **apenas** com permissão.

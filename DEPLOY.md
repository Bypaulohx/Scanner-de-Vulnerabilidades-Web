# Como colocar o WebVulnScanner na internet (de graça) com Vercel

Este guia mostra como hospedar o projeto na Vercel usando um repositório no GitHub.

---

## Pré-requisitos

- Conta no [GitHub](https://github.com)
- Conta na [Vercel](https://vercel.com) (login com GitHub)

---

## Passo 1: Criar o repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Crie um novo repositório (ex: `scanner-web` ou `webvulnscanner`)
3. **Não** marque "Initialize with README" se o projeto já tiver arquivos
4. Clique em **Create repository**

---

## Passo 2: Enviar o código para o GitHub

No terminal, na pasta do projeto:

```bash
# Inicializar Git (se ainda não tiver)
git init

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "Projeto WebVulnScanner pronto para deploy"

# Adicionar o repositório remoto (troque SEU_USUARIO e SEU_REPO pelo seu)
git remote add origin https://github.com/Bypaulohx/SEU_REPO.git

# Enviar para o GitHub
git branch -M main
git push -u origin main
```

> Substitua `Bypaulohx/SEU_REPO` pela URL do seu repositório.

---

## Passo 3: Deploy na Vercel

1. Acesse [vercel.com](https://vercel.com) e faça login com GitHub
2. Clique em **Add New** → **Project**
3. Selecione o repositório que acabou de criar
4. A Vercel deve detectar o `vercel.json` e usar:
   - **Framework Preset:** Other
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Output Directory:** `frontend/dist`
5. Clique em **Deploy**
6. Aguarde alguns minutos

---

## Passo 4: Configurar a API Python (se necessário)

O projeto já está configurado para rodar o frontend e a API na mesma URL:

- **Frontend:** `/` (página principal)
- **API:** `/api/scan` (endpoint do scanner)

A pasta `api/` contém o código Python que roda como **Serverless Function** na Vercel. As dependências são instaladas automaticamente a partir do `requirements.txt`.

> Se o deploy da API falhar, verifique se o `requirements.txt` está na raiz do projeto.

---

## URLs após o deploy

Após o deploy, você terá algo como:

- **Site:** `https://seu-projeto.vercel.app`
- **API:** `https://seu-projeto.vercel.app/api/scan`

O frontend já chama `/api/scan` na mesma origem, então tudo funciona automaticamente.

---

## Atualizar o site

Sempre que você fizer alterações e enviar para o GitHub:

```bash
git add .
git commit -m "Descrição das alterações"
git push
```

A Vercel detecta o push e faz um novo deploy automaticamente.

---

## Possíveis problemas

### "Build failed"
- Confirme que o `vercel.json` está na raiz do projeto
- Verifique se o `requirements.txt` inclui `mangum>=0.17.0`

### API retorna 404
- Verifique se a pasta `api/` está na raiz e contém `scan.py`
- Confira os logs do deploy na Vercel

### Erro de CORS
- O `api/main.py` já permite todas as origens (`allow_origins=["*"]`). Se mudou, restaure essa configuração.

---

## Resumo

| Etapa | O que fazer |
|-------|-------------|
| 1 | Criar repo no GitHub |
| 2 | `git push` do código |
| 3 | Conectar repo na Vercel e fazer deploy |
| 4 | Usar o link `*.vercel.app` gerado |

Pronto. Seu scanner estará online e gratuito.

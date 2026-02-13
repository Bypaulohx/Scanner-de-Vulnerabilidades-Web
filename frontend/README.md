# WebVulnScanner — Frontend

Interface React + TypeScript para o scanner de vulnerabilidades web.

## Como rodar

1. **Instale as dependências:**
   ```bash
   npm install
   ```

2. **Suba a API** (em outro terminal, na raiz do projeto):
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

3. **Inicie o frontend:**
   ```bash
   npm run dev
   ```

4. Acesse: http://localhost:5173

O Vite já está configurado para fazer proxy de `/api` para `http://127.0.0.1:8000`, então as requisições funcionam automaticamente.

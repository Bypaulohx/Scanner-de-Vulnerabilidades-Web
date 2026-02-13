import { useState, FormEvent } from 'react'
import { runScan } from '../api'
import type { ScanRequest } from '../types'

interface Props {
  onResult: (data: Awaited<ReturnType<typeof runScan>>) => void
  onError: (msg: string) => void
  onLoading: (loading: boolean) => void
  disabled?: boolean
}

export function ScanForm({ onResult, onError, onLoading, disabled }: Props) {
  const [url, setUrl] = useState('http://testphp.vulnweb.com/')
  const [xss, setXss] = useState(true)
  const [sqli, setSqli] = useState(true)
  const [headers, setHeaders] = useState(true)
  const [insecure, setInsecure] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!url.trim()) {
      onError('Informe a URL alvo.')
      return
    }

    onLoading(true)
    try {
      const req: ScanRequest = {
        url: url.trim(),
        xss,
        sqli,
        headers,
        timeout: 10,
        insecure,
      }
      const data = await runScan(req)
      onResult(data)
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Erro ao executar varredura.')
    } finally {
      onLoading(false)
    }
  }

  return (
    <form className="scan-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="url">URL alvo</label>
        <input
          id="url"
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://exemplo.com/page.php?id=1"
          disabled={disabled}
        />
      </div>

      <div className="form-group form-checks">
        <span className="checks-label">Testes a executar:</span>
        <label className="checkbox">
          <input
            type="checkbox"
            checked={headers}
            onChange={(e) => setHeaders(e.target.checked)}
            disabled={disabled}
          />
          Headers de segurança
        </label>
        <label className="checkbox">
          <input
            type="checkbox"
            checked={xss}
            onChange={(e) => setXss(e.target.checked)}
            disabled={disabled}
          />
          XSS refletido
        </label>
        <label className="checkbox">
          <input
            type="checkbox"
            checked={sqli}
            onChange={(e) => setSqli(e.target.checked)}
            disabled={disabled}
          />
          SQL Injection
        </label>
        <label className="checkbox">
          <input
            type="checkbox"
            checked={insecure}
            onChange={(e) => setInsecure(e.target.checked)}
            disabled={disabled}
          />
          Ignorar erros TLS (--insecure)
        </label>
      </div>

      <button type="submit" className="btn-primary" disabled={disabled}>
        Iniciar varredura
      </button>
    </form>
  )
}

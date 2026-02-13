import type { ScanResponse, ScanResult } from '../types'

interface Props {
  data: ScanResponse
}

export function ScanResults({ data }: Props) {
  return (
    <section className="results">
      <h2 className="results-title">Resultados — {data.target}</h2>

      {data.results.map((r) => (
        <ResultBlock key={r.type} result={r} />
      ))}
    </section>
  )
}

function ResultBlock({ result }: { result: ScanResult }) {
  if (result.type === 'headers') {
    return (
      <div className="result-card">
        <div className="result-header">
          <h3>Headers de Segurança</h3>
          <StatusBadge ok={result.ok} />
        </div>
        {result.missing.length > 0 ? (
          <table className="result-table">
            <thead>
              <tr>
                <th>Header ausente</th>
                <th>Recomendação</th>
              </tr>
            </thead>
            <tbody>
              {result.missing.map((m) => (
                <tr key={m.header}>
                  <td><code>{m.header}</code></td>
                  <td>{m.hint}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="result-ok">✓ Todos os headers recomendados estão presentes.</p>
        )}
        {result.notes.length > 0 && (
          <ul className="result-notes">
            {result.notes.map((n, i) => (
              <li key={i}>{n}</li>
            ))}
          </ul>
        )}
      </div>
    )
  }

  if (result.type === 'xss') {
    return (
      <div className="result-card">
        <div className="result-header">
          <h3>XSS Refletido</h3>
          <StatusBadge ok={!result.vulnerable} />
        </div>
        <p className="result-meta">Parâmetros testados: {result.tested}</p>
        {result.vulnerable && result.findings.length > 0 ? (
          <table className="result-table">
            <thead>
              <tr>
                <th>Parâmetro</th>
                <th>Payload</th>
                <th>URL</th>
                <th>Evidência</th>
              </tr>
            </thead>
            <tbody>
              {result.findings.map((f, i) => (
                <tr key={i}>
                  <td><code>{f.param}</code></td>
                  <td><code className="payload">{f.payload}</code></td>
                  <td><a href={f.url} target="_blank" rel="noopener noreferrer">{f.url}</a></td>
                  <td>{f.evidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="result-ok">Nenhuma vulnerabilidade XSS refletida encontrada.</p>
        )}
      </div>
    )
  }

  if (result.type === 'sqli') {
    return (
      <div className="result-card">
        <div className="result-header">
          <h3>SQL Injection</h3>
          <StatusBadge ok={!result.vulnerable} />
        </div>
        <p className="result-meta">Payloads testados: {result.tested}</p>
        {result.vulnerable && result.findings.length > 0 ? (
          <table className="result-table">
            <thead>
              <tr>
                <th>Parâmetro</th>
                <th>Payload</th>
                <th>URL</th>
                <th>Evidência</th>
              </tr>
            </thead>
            <tbody>
              {result.findings.map((f, i) => (
                <tr key={i}>
                  <td><code>{f.param}</code></td>
                  <td><code className="payload">{f.payload}</code></td>
                  <td><a href={f.url} target="_blank" rel="noopener noreferrer">{f.url}</a></td>
                  <td>{f.evidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="result-ok">Nenhuma vulnerabilidade SQLi (erro-based) encontrada.</p>
        )}
      </div>
    )
  }

  return null
}

function StatusBadge({ ok }: { ok: boolean }) {
  return (
    <span className={`badge ${ok ? 'badge-ok' : 'badge-warn'}`}>
      {ok ? 'OK' : 'Atenção'}
    </span>
  )
}

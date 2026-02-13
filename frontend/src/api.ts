import type { ScanRequest, ScanResponse } from './types'

const API_BASE = '/api'

export async function runScan(req: ScanRequest): Promise<ScanResponse> {
  const res = await fetch(`${API_BASE}/scan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Erro ao executar varredura')
  }

  return res.json()
}

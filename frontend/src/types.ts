/** Resultado de varredura de headers */
export interface HeadersResult {
  type: 'headers'
  target: string
  ok: boolean
  missing: Array<{ header: string; hint: string }>
  headers_seen: Record<string, string>
  notes: string[]
}

/** Resultado de varredura XSS */
export interface XssResult {
  type: 'xss'
  target: string
  tested: number
  vulnerable: boolean
  findings: Array<{
    param: string
    payload: string
    url: string
    evidence: string
  }>
}

/** Resultado de varredura SQLi */
export interface SqliResult {
  type: 'sqli'
  target: string
  tested: number
  vulnerable: boolean
  findings: Array<{
    param: string
    payload: string
    url: string
    evidence: string
  }>
}

export type ScanResult = HeadersResult | XssResult | SqliResult

export interface ScanResponse {
  success: boolean
  target: string
  results: ScanResult[]
}

export interface ScanRequest {
  url: string
  xss?: boolean
  sqli?: boolean
  headers?: boolean
  timeout?: number
  insecure?: boolean
}

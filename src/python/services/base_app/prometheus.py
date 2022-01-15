from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('request_count', 'App Request Count', ['app_name', 'method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['app_name', 'endpoint'])

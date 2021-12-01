from mitmproxy import http
TOKEN_HEADER = 'Px-Token'
TOKEN_VALUE = 'mysecuretoken'
HOST_HEADER = 'Px-Host'
IP_HEADER = 'Px-IP'

def request(flow: http.HTTPFlow) -> None:
    flow.request.headers[TOKEN_HEADER] = TOKEN_VALUE
    flow.request.headers[HOST_HEADER] = flow.request.host_header
    flow.request.host = "yourproxy.workers.dev"
    #flow.request.port = 443
    #flow.request.scheme = "https"


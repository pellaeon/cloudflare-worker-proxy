# Use Cloudflare Worker as HTTP proxy

This project is inspired by https://github.com/jychp/cloudflare-bypass , which enables the use of Cloudflare Workers as proxies by providing a Python API to send requests. This is however quite limiting.

To enable the Cloudflare worker proxy to be used in regular applications, I wrote a small `mitmproxy` script to rewrite HTTP requests and transparently forwards them to Cloudflare worker proxy.

## Basic usage

1. Change `TOKEN_VALUE` in (`worker.js`)[https://github.com/jychp/cloudflare-bypass/blob/main/worker.js] to your own secret value.
2. Deploy `worker.js` to Cloudflare worker.
3. Download `mitm_cf.py` and change `TOKEN_VALUE` to match the value in `worker.js`.
4. Change `flow.request.host` to your Cloudflare worker hostname.
5. Run mitmproxy with the mitm_cf.py:
```
./mitmproxy --mode transparent --showhost -s mitm_cf.py -p 2000 --no-http2
```

Now you have a transparent proxy listening on port 2000.

## Easy usage with iptables

1. `adduser proxieduser`
2. `sudo iptables -t nat -A OUTPUT -p tcp -m owner --uid-owner proxieduser --dport 443 -j REDIRECT --to-port 2000`
3. Now, simply run any application in `proxieduser`, the traffic will be redirected over to mitmproxy:
```
sudo -u proxieduser curl --cacert ~/.mitmproxy/mitmproxy-ca-cert.pem -v -d '{"key": "value"}' https://httpbin.org/post
```

## Note

- HTTP is stateless, so is Cloudflare workers. Each individual request made by the application, regardless of host or IP, will be treated individually by the Cloudflare worker. The worker will handle application requests by making another request of its own, each request made by a Cloudflare worker will use a random Cloudflare IP address. This characteristic will make some websites break when using this proxy, these mostly include websites that require logins.

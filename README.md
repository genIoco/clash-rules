## 自用配置文件

### 使用说明

​		此配置文件为自用配置文件，无法直接使用，需要添加parsers配置，去除样例，并添加自动节点内容。

parsers示例如下：

```yaml
  - url: https://raw.githubusercontent.com/genIoco/clash-rules/main/config.yaml
    yaml:
      prepend-proxies:
        - name: 自己的节点
          server: url
          type: trojan
          port: 443
          password: password
          udp: true
          sni: sni
          skip-cert-verify: true
      mix-proxy-providers:
        自己的机场:
          type: http
          url: 订阅链接
          interval: 86400
          proxy: DIRECT
          format: yaml

      commands:
        # 删除样例节点
        - proxies.proxy-example-
        - proxy-groups.🥷PROXY.proxies.0-
```


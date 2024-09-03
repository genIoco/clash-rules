## 自用配置文件

### 使用说明

​		此配置文件为自用配置文件，无法直接使用，需要添加parsers配置，去除样例，并添加自动节点内容。

parsers示例如下：

```yaml
  - url: https://raw.githubusercontent.com/genIoco/clash-rules/main/config.yaml
    yaml:
      prepend-proxies:
        - name: node
          server: url
          type: trojan
          port: 443
          password: password
          udp: true
          sni: sni
          skip-cert-verify: true
      mix-proxy-providers:
        providers1:
          type: http
          url: 订阅链接
          interval: 86400
          proxy: DIRECT
          format: yaml

      commands:
        # 删除样例node
        - proxies.proxy-example-
        - proxy-groups.🥷PROXY.proxies.0-
        
        # 添加自己的node和providers
        - proxy-groups.🥷PROXY.proxies.0+node
        - proxy-groups.🥷PROXY.use.0=providers1
```

clash Verge rev扩展脚本示例如下：

```
// Define main function (script entry)
// 国内DNS服务器
const domesticNameservers = [
  "https://dns.alidns.com/dns-query", // 阿里云公共DNS
  "https://doh.pub/dns-query", // 腾讯DNSPod
  "https://doh.360.cn/dns-query" // 360安全DNS
];

// 国外DNS服务器
const foreignNameservers = [
  "https://1.1.1.1/dns-query", // Cloudflare(主)
  "https://1.0.0.1/dns-query", // Cloudflare(备)
  "https://208.67.222.222/dns-query", // OpenDNS(主)
  "https://208.67.220.220/dns-query", // OpenDNS(备)
  "https://194.242.2.2/dns-query", // Mullvad(主)
  "https://194.242.2.3/dns-query" // Mullvad(备)
];

// DNS配置
const dnsConfig = {
  "enable": true,
  "listen": "0.0.0.0:1053",
  "ipv6": true,
  "use-system-hosts": false,
  "cache-algorithm": "arc",
  "enhanced-mode": "fake-ip",
  "fake-ip-range": "198.18.0.1/16",
  "fake-ip-filter": [
    // 本地主机/设备
    "+.lan",
    "+.local",
    // Windows网络出现小地球图标
    "+.msftconnecttest.com",
    "+.msftncsi.com",
    // QQ快速登录检测失败
    "localhost.ptlogin2.qq.com",
    "localhost.sec.qq.com",
    // 微信快速登录检测失败
    "localhost.work.weixin.qq.com"
  ],
  "default-nameserver": ["223.5.5.5", "119.29.29.29", "1.1.1.1", "8.8.8.8"],
  "nameserver": [...domesticNameservers, ...foreignNameservers],
  "proxy-server-nameserver": [...domesticNameservers, ...foreignNameservers],
  "nameserver-policy": {
    "geosite:private,cn,geolocation-cn": domesticNameservers,
    "geosite:google,youtube,telegram,gfw,geolocation-!cn": foreignNameservers
  }
};

// 规则
const rules = [
  // 自定义规则
  "IP-CIDR,10.0.0.0/16,👆SELECT",
]

// 自定义添加proxies
// TODO:修改为需要添加的节点
const proxies = [
  {
    "name": "Azure",
    "server": "https://url",
    "type": "trojan",
    "port": "443",
    "password": "password",
    "udp": true,
    "sni": "u",
    "skip-cert-verify": true
  }
]

// 代理provider通用配置
const proxyProvidersBase = {
  type: "http",
  interval: 3600,
  "health-check": {
    enable: true,
    url: "https://www.google.com/generate_204",
    interval: 300,
  }
};

// 代理provider配置
// TODO:修改为需要添加的机场地址
const proxyProvider = {
    订阅1: {
    ...proxyProvidersBase,
    url: "订阅地址",
    path: "./proxies/jichang.yaml"
  },
};

function main(config, profileName) {

  //-------------------------------------------删除样例节点
  config["proxies"] = config["proxies"].filter(proxy => !proxy["name"].endsWith("example"));
  config["proxy-groups"][0].proxies = config["proxy-groups"][0].proxies.filter(proxy => !proxy.endsWith("example"));

  //-------------------------------------------插入自定义 proxies 和 proxies provider
  const proxyCount =
    config?.["proxies"] === "undefined"
      ? (config = { ...config, "proxies": proxies })["proxies"].length
      : (config.proxies = [...config.proxies, ...proxies]).length;
  const proxyProviderCount =
    config?.["proxy-providers"] === "undefined"
      ? (config = { ...config, "proxy-providers": proxyProvider })["proxy-providers"].length
      : (config["proxy-providers"] = { ...config["proxy-providers"], ...proxyProvider }).length;
  //-------------------------------------------插入自定义 proxies 和 proxies provider END

  config["proxy-groups"][0]["include-all-providers"] = true

  //-------------------------------------------空检测
  if (proxyCount === 0 && proxyProviderCount === 0) {
    throw new Error("配置文件中未找到任何代理");
  }

  //-------------------------------------------覆盖原配置中DNS配置
  config["dns"] = dnsConfig;

  return config;
}

```



### scripts说明

​		scripts内保存了部分常用脚本，具体功能对应如下：

- `get_wechat_ips.py`:用于获取微信服务器的ip地址


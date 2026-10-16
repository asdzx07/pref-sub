# 优选 IP 订阅生成器

为 VLESS+WS+TLS 节点批量生成优选 IP 订阅的 Web 工具。

## 功能

- 📝 节点配置：手动填写或从订阅 URL 一键导入（支持 sb-onekey 的 v2rayn 订阅）
- ⚡️ 优选 IP 管理：一行一个，格式 `IP:端口#备注`
- 📋 生成订阅：
  - VLESS 链接（每个优选 IP 一条）
  - Base64 订阅
  - Clash YAML（含 url-test 自动测速组）
  - sing-box JSON
- 📱 二维码、复制按钮
- 💾 配置保存在浏览器 localStorage

## 部署

纯静态单页，扔到 Cloudflare Pages / GitHub Pages / 任何静态托管即可：

```bash
# Cloudflare Pages：连接本仓库，构建命令留空，输出目录 /
```

## 原理

优选 IP 替换 vless 链接中的服务器地址，SNI/Host 保持为你的 CDN 域名：

```
vless://UUID@优选IP:443?security=tls&sni=你的域名&type=ws&path=/xxx&host=你的域名&fp=chrome#备注
```

流量路径：客户端 → 优选 IP（Cloudflare 边缘）→ 按 SNI 回源到你的 VPS。

# 🚀 部署指南 - 股票查询 API

## 方式一：部署到 Railway (推荐) ⭐

### 步骤 1: 准备 GitHub 仓库

```bash
cd /Users/huan/.openclaw/workspace

# 登录 GitHub (如果还没登录)
gh auth login

# 创建仓库并推送
gh repo create stock-api --public --push
```

### 步骤 2: 部署到 Railway

#### 方法 A: 一键部署

1. 访问 Railway: https://railway.app
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择 `stock-api` 仓库
5. Railway 会自动检测 `railway.toml` 并部署

#### 方法 B: 使用 Railway CLI

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录 Railway
railway login

# 初始化项目
railway init

# 关联现有项目
railway link

# 部署
railway up
```

### 步骤 3: 配置环境变量

在 Railway 项目面板中设置：

| 变量名 | 值 |
|--------|-----|
| `MARKETSTACK_API_KEY` | `a3e52a1083788b9f3afa054fe53cda7f` |
| `PORT` | `8000` |

### 步骤 4: 获取部署 URL

部署完成后，Railway 会分配一个公网 URL，格式类似：
```
https://stock-api-production.up.railway.app
```

访问 `https://你的 URL.up.railway.app/docs` 查看 API 文档

---

## 方式二：部署到其他平台

### Heroku

创建 `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

部署命令:
```bash
heroku create stock-api
git push heroku main
heroku config:set MARKETSTACK_API_KEY=你的 API Key
```

### Vercel

创建 `vercel.json`:
```json
{
  "builds": [{
    "src": "main.py",
    "use": "@vercel/python"
  }],
  "routes": [{
    "src": "/(.*)",
    "dest": "main.py"
  }]
}
```

### Docker

创建 `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 测试部署

部署完成后，测试 API:

```bash
# 替换为你的 Railway URL
BASE_URL="https://你的 URL.up.railway.app"

# 测试首页
curl $BASE_URL/

# 测试股票查询
curl $BASE_URL/stock/AAPL

# 测试多只股票
curl "$BASE_URL/stocks?symbols=AAPL,GOOG,MSFT"

# 测试健康检查
curl $BASE_URL/health
```

---

## 本地开发

```bash
# 安装依赖
pip3 install -r requirements.txt

# 运行开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 访问 API 文档
# http://localhost:8000/docs
```

---

## 故障排除

### 部署失败

1. 检查 `requirements.txt` 是否完整
2. 确认 `railway.toml` 配置正确
3. 查看 Railway 部署日志

### API 返回错误

1. 检查 API Key 是否有效
2. 确认 MarketStack 配额未用完
3. 检查网络连接

### 端口问题

Railway 使用 `$PORT` 环境变量，确保 `railway.toml` 中正确配置

---

## 快速命令汇总

```bash
# 1. 更新代码
git add -A
git commit -m "Update"
git push

# 2. Railway 重新部署 (自动)
# Railway 会在 push 后自动部署

# 3. 查看部署日志
railway logs

# 4. 打开部署 URL
railway open
```

---

**部署成功后，记得更新 README.md 中的在线演示链接！** 🤖

# 🚀 一键部署到 Railway

## 方式 A: 使用 Railway 网页部署 (推荐) ⭐

### 步骤 1: 访问 Railway

打开浏览器，访问：**https://railway.app**

### 步骤 2: 创建新项目

1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 授权 Railway 访问你的 GitHub
4. 选择 **`moonwalk92/stock-api`** 仓库

### 步骤 3: 自动部署

Railway 会自动检测 `railway.toml` 并开始部署！

### 步骤 4: 配置环境变量

在 Railway 项目面板中，点击 **"Variables"**，添加：

| 变量名 | 值 |
|--------|-----|
| `MARKETSTACK_API_KEY` | `a3e52a1083788b9f3afa054fe53cda7f` |
| `PORT` | `8000` |

### 步骤 5: 获取部署 URL

部署完成后，点击 **"Generate Domain"**，你会得到类似这样的 URL：

```
https://stock-api-production.up.railway.app
```

访问 `https://你的 URL/docs` 查看 API 文档！

---

## 方式 B: 使用 Railway CLI (高级)

```bash
# 登录 Railway (会打开浏览器)
railway login

# 初始化项目
railway init

# 选择 "Link existing project" 或 "Create new project"

# 部署
railway up

# 设置环境变量
railway variables set MARKETSTACK_API_KEY=a3e52a1083788b9f3afa054fe53cda7f
railway variables set PORT=8000

# 打开部署 URL
railway open
```

---

## 测试 API

部署完成后，测试你的 API：

```bash
# 替换为你的 Railway URL
BASE_URL="https://你的 URL.up.railway.app"

# 测试首页
curl $BASE_URL/

# 查询股票
curl $BASE_URL/stock/AAPL

# 查询多只股票
curl "$BASE_URL/stocks?symbols=AAPL,GOOG,MSFT"

# 查看 API 文档
# 浏览器访问：$BASE_URL/docs
```

---

## 快速链接

- **GitHub 仓库**: https://github.com/moonwalk92/stock-api
- **Railway**: https://railway.app
- **MarketStack**: https://marketstack.com

---

**部署成功后，告诉你的 URL，我来帮你测试！** 🤖

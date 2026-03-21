# 🚀 部署指南

## 步骤 1: 上传到 GitHub

### 1.1 登录 GitHub CLI

```bash
gh auth login
```

按提示操作：
1. 选择 **GitHub.com**
2. 选择 **HTTPS**
3. 选择 **Login with a web browser**
4. 复制 One-Time Code
5. 在浏览器中打开 https://github.com/login/device
6. 粘贴代码并授权
7. 回到终端，按 Enter

### 1.2 创建 Git 仓库

```bash
cd /Users/huan/.openclaw/workspace

# 初始化 git
git init
git branch -M main

# 添加所有文件
git add -A

# 提交
git commit -m "Initial commit: Stock query & Super Mario game"
```

### 1.3 创建 GitHub 仓库

```bash
# 创建新仓库 (替换 <username> 为你的 GitHub 用户名)
gh repo create stock-mario-game --public --source=. --remote=origin --push
```

或者手动创建：
1. 访问 https://github.com/new
2. 仓库名：`stock-mario-game`
3. 选择 **Public**
4. 点击 **Create repository**
5. 按页面提示推送代码：

```bash
git remote add origin https://github.com/<你的用户名>/stock-mario-game.git
git push -u origin main
```

---

## 步骤 2: 部署到 Railway

### 2.1 准备 Railway

1. 访问 https://railway.app
2. 点击 **Start a New Project**
3. 选择 **Deploy from GitHub repo**
4. 授权 Railway 访问你的 GitHub
5. 选择 `stock-mario-game` 仓库

### 2.2 配置 Railway

**注意**: Railway 主要用于部署 Web 服务。这个项目包含：
- 📊 股票查询 (命令行工具)
- 🎮 超级玛丽 (桌面游戏)

这两个都**不适合**直接部署到 Railway（需要图形界面）。

### 替代方案 A: 部署为 Web API

如果要部署股票查询为 Web 服务，需要创建 Flask/FastAPI 应用。

### 替代方案 B: 使用 Railway 作为运行环境

创建 `railway.toml`:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python3 stock_marketstack.py AAPL"
restartPolicyType = "ON_FAILURE"
```

但这只适合运行脚本，不适合游戏。

---

## 推荐方案

### 对于股票查询工具:
✅ **GitHub Releases** - 发布可执行版本
✅ **PyPI** - 发布为 Python 包
✅ **Railway/Heroku** - 部署为 Web API (需要额外开发)

### 对于超级玛丽游戏:
❌ **不适合云端部署** (需要图形界面)
✅ **GitHub** - 分享源代码
✅ **itch.io** - 发布游戏 (打包为桌面应用)

---

## 快速命令汇总

```bash
# 1. 登录 GitHub
gh auth login

# 2. 初始化仓库
cd /Users/huan/.openclaw/workspace
git init
git add -A
git commit -m "Initial commit"

# 3. 创建并推送
gh repo create stock-mario-game --public --push

# 4. 后续更新
git add -A
git commit -m "Update"
git push
```

---

## 需要我帮你做什么？

1. **仅上传 GitHub** - 我可以帮你完成所有 git 命令
2. **创建 Web 版本** - 把股票查询改成 Web API 再部署
3. **打包游戏** - 把超级玛丽打包成独立应用

告诉我你的选择！🤖

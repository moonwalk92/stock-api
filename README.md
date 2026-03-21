# 📊 股票查询 API

一个基于 FastAPI 的股票价格查询 Web 服务，使用 MarketStack API 获取美股数据。

**在线演示**: [部署到 Railway 后填写]

**API 文档**: `/docs` (Swagger UI)

---

## 🚀 快速开始

### 本地运行

```bash
# 1. 安装依赖
pip3 install -r requirements.txt

# 2. 运行服务
python3 main.py

# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档

### 命令行查询

```bash
# 查询单只股票
python3 stock_marketstack.py AAPL

# 查询多只股票
python3 stock_marketstack.py AAPL GOOG MSFT NVDA TSLA
```

---

## 📡 API 端点

### `GET /`
API 首页，显示可用端点

### `GET /stock/{symbol}`
查询单只股票的最新价格

**参数**:
- `symbol` - 股票代码 (如：AAPL, GOOG, TSLA)

**示例**:
```bash
curl http://localhost:8000/stock/AAPL
```

**响应**:
```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "name": "AAPL",
    "price": 247.99,
    "open": 248.11,
    "high": 249.20,
    "low": 246.00,
    "volume": 87981315,
    "change": -0.12,
    "change_percent": -0.05,
    "date": "2026-03-20",
    "source": "MarketStack EOD"
  }
}
```

### `GET /stocks?symbols=AAPL,GOOG,MSFT`
查询多只股票

**参数**:
- `symbols` - 股票代码列表，逗号分隔

**示例**:
```bash
curl "http://localhost:8000/stocks?symbols=AAPL,GOOG,MSFT"
```

### `GET /default`
查询默认监控股票列表 (AAPL, GOOG, MSFT, NVDA, TSLA)

**示例**:
```bash
curl http://localhost:8000/default
```

### `GET /history/{symbol}?limit=30`
获取股票历史数据

**参数**:
- `symbol` - 股票代码
- `limit` - 返回天数 (1-100, 默认 30)

**示例**:
```bash
curl "http://localhost:8000/history/AAPL?limit=7"
```

### `GET /health`
健康检查

---

## 📦 部署到 Railway

### 一键部署

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new)

### 手动部署

1. **Fork 本仓库** 或 直接使用你的 GitHub 仓库

2. **访问 Railway**
   - 前往 https://railway.app
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"

3. **选择仓库**
   - 授权 Railway 访问 GitHub
   - 选择 `stock-mario-game` 仓库

4. **配置环境变量**
   ```
   MARKETSTACK_API_KEY=你的 API Key
   PORT=8000
   ```

5. **部署**
   - Railway 会自动检测 `railway.toml` 并部署
   - 部署完成后会分配一个公网 URL

### Railway 配置说明

项目包含 `railway.toml` 配置文件：

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "ON_FAILURE"
```

---

## 🔑 API Key 配置

### MarketStack API

1. 访问 https://marketstack.com/product
2. 免费注册获取 API Key
3. 免费额度：每天 1000 次请求

### 设置 API Key

**本地运行**:
```bash
export MARKETSTACK_API_KEY="你的 API Key"
```

**Railway 部署**:
在 Railway 项目设置中添加环境变量 `MARKETSTACK_API_KEY`

**代码中** (不推荐):
编辑 `main.py` 中的 `API_KEY` 变量

---

## 🛠️ 技术栈

- **框架**: FastAPI
- **服务器**: Uvicorn (ASGI)
- **数据源**: MarketStack API
- **部署**: Railway
- **依赖管理**: pip / requirements.txt

---

## 📝 文件说明

| 文件 | 说明 |
|------|------|
| `main.py` | FastAPI Web 服务主程序 |
| `stock_marketstack.py` | 命令行版本 |
| `requirements.txt` | Python 依赖 |
| `railway.toml` | Railway 部署配置 |
| `README.md` | 项目文档 |

---

## ⚠️ 注意事项

1. **数据延迟**: 免费计划提供 EOD (日线) 数据，非实时
2. **交易时间**: 仅美股交易日更新
3. **速率限制**: MarketStack 免费计划每天 1000 次请求
4. **CORS**: API 已配置允许所有来源，生产环境建议限制

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Made with ❤️ by 月光**

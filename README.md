# 📊 股票查询 & 🎮 超级玛丽游戏

一个包含股票价格查询和经典游戏的 Python 项目集合。

## 📁 项目内容

### 1. 股票价格查询 (MarketStack API)

使用 MarketStack API 查询美股实时价格数据。

**文件**: `stock_marketstack.py`

**功能**:
- ✅ 查询多只股票价格
- ✅ 显示开盘价、最高价、最低价、收盘价
- ✅ 计算涨跌幅
- ✅ 显示成交量
- ✅ 支持历史数据查询

**使用方法**:
```bash
# 查询单只股票
python3 stock_marketstack.py AAPL

# 查询多只股票
python3 stock_marketstack.py AAPL GOOG MSFT NVDA TSLA

# 查询默认列表
python3 stock_marketstack.py
```

**配置 API Key**:
1. 访问 https://marketstack.com/product
2. 免费注册获取 API Key
3. 编辑 `stock_marketstack.py`，填入你的 API Key

**免费额度**: 每天 1000 次请求

---

### 2. 超级玛丽风格游戏

使用 Pygame 开发的经典平台跳跃游戏。

**文件**: `super_mario.py`

**游戏特性**:
- 🎮 经典玛丽奥造型
- 🧱 砖块平台、问号方块
- 🟡 金币收集系统
- 🍄 栗子怪敌人
- ❤️ 生命系统 (3 条命)
- 🏆 分数统计

**控制方式**:
| 按键 | 动作 |
|------|------|
| `←` `→` 或 `A` `D` | 左右移动 |
| `空格` 或 `W` | 跳跃 |
| `R` | 重新开始 |
| `ESC` | 退出游戏 |

**安装依赖**:
```bash
pip3 install pygame
```

**运行游戏**:
```bash
python3 super_mario.py
```

---

## 🚀 快速开始

### 安装依赖

```bash
# 安装所有依赖
pip3 install requests pygame

# 或者使用 requirements.txt
pip3 install -r requirements.txt
```

### 运行示例

```bash
# 查询股票
python3 stock_marketstack.py AAPL

# 玩游戏
python3 super_mario.py
```

---

## 📋 依赖列表

- `requests` - HTTP 请求库 (股票查询)
- `pygame` - 游戏开发库 (超级玛丽)

---

## 📝 其他脚本

| 文件 | 说明 |
|------|------|
| `stock_price.py` | yfinance 版本 (可能限流) |
| `stock_query.py` | 多数据源版本 |
| `stock_simple.py` | 简化版本 |

---

## ⚠️ 注意事项

1. **股票市场数据**: 仅在交易日更新，周末/节假日无新数据
2. **网络要求**: 需要能访问 MarketStack API
3. **游戏显示**: 需要图形界面环境运行 Pygame

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Made with ❤️ by 月光**

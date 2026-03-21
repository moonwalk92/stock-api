#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票价格查询 - MarketStack API (EOD 日线数据)
免费注册：https://marketstack.com/product (每天 1000 次请求)

用法:
    python3 stock_marketstack.py AAPL        # 查询单只股票
    python3 stock_marketstack.py AAPL GOOG   # 查询多只股票
    python3 stock_marketstack.py             # 查询默认股票列表
"""

import requests
import sys
from datetime import datetime

# ============== 配置区域 ==============
API_KEY = "a3e52a1083788b9f3afa054fe53cda7f"
# ====================================

# 默认监控股票列表
DEFAULT_STOCKS = ['AAPL', 'GOOG', 'MSFT', 'NVDA', 'TSLA']

def get_stock_price(symbol):
    """获取股票最新价格 (使用 EOD API)"""
    
    if not API_KEY:
        print("⚠️  请先配置 API Key!")
        print("   注册：https://marketstack.com/product")
        return None
    
    try:
        # 使用 EOD API (免费计划支持)
        url = "http://api.marketstack.com/v1/eod"
        params = {
            'access_key': API_KEY,
            'symbols': symbol,
            'limit': 1  # 只取最新一条
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'error' in data:
            err = data['error']
            print(f"❌ API 错误：{err.get('message', 'Unknown error')}")
            return None
        
        if 'data' in data and len(data['data']) > 0:
            quote = data['data'][0]
            
            open_price = quote.get('open', 0)
            close_price = quote.get('close', 0)
            change = close_price - open_price
            change_pct = (change / open_price * 100) if open_price else 0
            
            return {
                'symbol': quote['symbol'],
                'name': quote['symbol'],
                'price': close_price,
                'open': open_price,
                'high': quote.get('high', 0),
                'low': quote.get('low', 0),
                'volume': quote.get('volume', 0),
                'previous_close': quote.get('close', 0),
                'change': change,
                'change_percent': change_pct,
                'date': quote.get('date', ''),
                'source': 'MarketStack EOD'
            }
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误：{e}")
        return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def get_daily_data(symbol, limit=30):
    """获取历史日线数据"""
    
    if not API_KEY:
        return None
    
    try:
        url = "http://api.marketstack.com/v1/eod"
        params = {
            'access_key': API_KEY,
            'symbols': symbol,
            'limit': limit
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'data' in data:
            return data['data']
    except:
        pass
    
    return None


def print_stock_card(data):
    """打印股票信息卡片"""
    if not data:
        print(f"❌ 数据获取失败")
        return
    
    symbol = data['symbol']
    price = data['price']
    change = data.get('change', 0)
    change_pct = data.get('change_percent', 0)
    
    # 涨跌显示
    if change >= 0:
        trend = "📈"
        sign = "+"
    else:
        trend = "📉"
        sign = ""
    
    print(f"\n{trend} {symbol}")
    print(f"   收盘价：${price:.2f}")
    print(f"   涨跌：{sign}{change:.2f} ({sign}{change_pct:.2f}%)")
    print(f"   开盘：${data['open']:.2f} | 最高：${data.get('high', 0):.2f} | 最低：${data.get('low', 0):.2f}")
    print(f"   成交量：{data.get('volume', 0):,}")
    
    if 'date' in data and data['date']:
        print(f"   数据日期：{data['date'][:10]}")
    print(f"   数据源：{data.get('source', 'MarketStack')}")


def print_history(symbol):
    """打印历史数据"""
    print(f"\n📊 {symbol} 历史数据 (最近 5 天)")
    print("-" * 55)
    
    data = get_daily_data(symbol, limit=5)
    if data:
        print(f"{'日期':<12} {'开盘':<10} {'最高':<10} {'最低':<10} {'收盘':<10} {'成交量':<12}")
        print("-" * 55)
        for day in reversed(data):  # 从旧到新
            date = day.get('date', '')[:10]
            open_p = day.get('open', 0)
            high = day.get('high', 0)
            low = day.get('low', 0)
            close = day.get('close', 0)
            vol = day.get('volume', 0)
            print(f"{date:<12} ${open_p:<9.2f} ${high:<9.2f} ${low:<9.2f} ${close:<9.2f} {vol:<12,}")
    else:
        print("无法获取历史数据")


def main():
    print("=" * 60)
    print("📊 股票价格查询 - MarketStack")
    print(f"   更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 检查 API Key
    if not API_KEY:
        print("\n⚠️  未配置 API Key!")
        print("\n配置步骤:")
        print("   1. 访问 https://marketstack.com/product")
        print("   2. 点击 'Get API Key' 免费注册")
        print("   3. 将 API Key 填入脚本中的 API_KEY 变量")
        print("\n免费额度：每天 1000 次请求，无需信用卡")
        return
    
    # 获取要查询的股票
    if len(sys.argv) > 1:
        stocks = sys.argv[1:]
    else:
        stocks = DEFAULT_STOCKS
    
    # 查询每只股票
    print(f"\n正在查询 {len(stocks)} 只股票...")
    
    for symbol in stocks:
        data = get_stock_price(symbol.upper())
        if data:
            print_stock_card(data)
        else:
            print(f"\n❌ {symbol.upper()} 数据获取失败")
    
    print("\n" + "=" * 60)
    print("💡 提示:")
    print("   - 用法：python3 stock_marketstack.py AAPL GOOG TSLA")
    print("   - 查看历史：python3 stock_marketstack.py AAPL --history")
    print("   - API 文档：https://marketstack.com/documentation")
    print("   - 注意：免费计划提供 EOD (日线) 数据，非实时")

if __name__ == '__main__':
    main()

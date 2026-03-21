#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票价格查询工具 - 多数据源备份
优先使用 yfinance，失败时切换到其他免费 API

用法:
    python3 stock_query.py AAPL        # 查询单只股票
    python3 stock_query.py AAPL GOOG   # 查询多只股票
"""

import requests
import time
import sys
from datetime import datetime

# 默认监控股票列表
DEFAULT_STOCKS = ['AAPL', 'GOOG', 'MSFT', 'NVDA', 'TSLA']

def query_yahoo_finance(symbol):
    """Yahoo Finance API (通过 query2.finance.yahoo.com)"""
    try:
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            result = data['chart']['result'][0]
            meta = result['meta']
            
            return {
                'symbol': symbol,
                'name': meta.get('symbol', symbol),
                'price': meta.get('regularMarketPrice', 0),
                'open': meta.get('regularMarketOpen', 0),
                'high': meta.get('regularMarketDayHigh', 0),
                'low': meta.get('regularMarketDayLow', 0),
                'volume': meta.get('regularMarketVolume', 0),
                'previous_close': meta.get('chartPreviousClose', 0),
                'change': meta.get('regularMarketPrice', 0) - meta.get('regularMarketOpen', 0),
                'change_percent': ((meta.get('regularMarketPrice', 0) - meta.get('regularMarketOpen', 0)) / meta.get('regularMarketOpen', 1)) * 100,
                'source': 'Yahoo Finance'
            }
    except Exception as e:
        pass
    return None

def query_alpha_vantage(symbol, api_key=None):
    """Alpha Vantage API (如果有 API key)"""
    if not api_key:
        return None
    
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'symbol': symbol,
                    'name': symbol,
                    'price': float(quote.get('05. price', 0)),
                    'open': float(quote.get('02. open', 0)),
                    'high': float(quote.get('03. high', 0)),
                    'low': float(quote.get('04. low', 0)),
                    'volume': int(quote.get('06. volume', 0)),
                    'previous_close': float(quote.get('07. previous close', 0)),
                    'change': float(quote.get('09. change', 0)),
                    'change_percent': float(quote.get('10. change percent', '0%').replace('%', '')),
                    'source': 'Alpha Vantage'
                }
    except:
        pass
    return None

def query_finnhub(symbol, api_key=None):
    """Finnhub API (如果有 API key)"""
    if not api_key:
        return None
    
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'c' in data:
                return {
                    'symbol': symbol,
                    'name': symbol,
                    'price': data['c'],
                    'open': data['o'],
                    'high': data['h'],
                    'low': data['l'],
                    'previous_close': data['pc'],
                    'change': data['c'] - data['pc'],
                    'change_percent': ((data['c'] - data['pc']) / data['pc']) * 100 if data['pc'] else 0,
                    'source': 'Finnhub'
                }
    except:
        pass
    return None

def get_stock_price(symbol, api_keys=None):
    """获取股票价格，多数据源 fallback"""
    if api_keys is None:
        api_keys = {}
    
    # 1. 尝试 Yahoo Finance
    result = query_yahoo_finance(symbol)
    if result:
        return result
    
    # 2. 尝试 Alpha Vantage (如果有 key)
    if api_keys.get('alpha_vantage'):
        time.sleep(0.5)
        result = query_alpha_vantage(symbol, api_keys['alpha_vantage'])
        if result:
            return result
    
    # 3. 尝试 Finnhub (如果有 key)
    if api_keys.get('finnhub'):
        time.sleep(0.5)
        result = query_finnhub(symbol, api_keys['finnhub'])
        if result:
            return result
    
    return None

def print_stock_card(data):
    """打印股票信息卡片"""
    if not data:
        print(f"❌ {data.get('symbol', 'UNKNOWN')} 数据获取失败")
        return
    
    symbol = data['symbol']
    price = data['price']
    change = data.get('change', 0)
    change_pct = data.get('change_percent', 0)
    
    # 涨跌颜色
    if change >= 0:
        trend = "📈"
        sign = "+"
    else:
        trend = "📉"
        sign = ""
    
    print(f"\n{trend} {symbol}")
    print(f"   当前价格：${price:.2f}")
    print(f"   涨跌：{sign}{change:.2f} ({sign}{change_pct:.2f}%)")
    if 'open' in data:
        print(f"   开盘：${data['open']:.2f} | 最高：${data.get('high', 0):.2f} | 最低：${data.get('low', 0):.2f}")
    if 'volume' in data:
        print(f"   成交量：{data['volume']:,}")
    print(f"   数据源：{data.get('source', 'Unknown')}")

def main():
    print("=" * 50)
    print("📊 股票价格查询 - 多数据源")
    print(f"   更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # API Keys (可选)
    api_keys = {
        # 'alpha_vantage': 'YOUR_API_KEY',  # 免费，https://www.alphavantage.co
        # 'finnhub': 'YOUR_API_KEY',        # 免费，https://finnhub.io
    }
    
    # 获取要查询的股票
    if len(sys.argv) > 1:
        stocks = sys.argv[1:]
    else:
        stocks = DEFAULT_STOCKS
    
    # 查询每只股票
    for i, symbol in enumerate(stocks):
        if i > 0:
            time.sleep(1)  # 避免限流
        
        data = get_stock_price(symbol.upper(), api_keys)
        if data:
            print_stock_card(data)
        else:
            print(f"\n❌ {symbol.upper()} 获取失败，所有数据源均不可用")
    
    print("\n" + "=" * 50)
    print("💡 提示:")
    print("   - 如遇限流，请稍等片刻后重试")
    print("   - 添加 API key 可获得更稳定数据")
    print("   - 用法：python3 stock_query.py AAPL GOOG TSLA")

if __name__ == '__main__':
    main()

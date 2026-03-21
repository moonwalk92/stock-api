#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票价格查询工具 - 使用 yfinance
完全免费，无需 API key

用法:
    python3 stock_price.py AAPL        # 查询单只股票
    python3 stock_price.py AAPL GOOG   # 查询多只股票
    python3 stock_price.py             # 查询默认股票列表
"""

import yfinance as yf
import time
import sys
from datetime import datetime

# 默认监控股票列表
DEFAULT_STOCKS = ['AAPL', 'GOOG', 'MSFT', 'NVDA', 'TSLA']

def get_stock_info(symbol, retry=3):
    """获取股票信息，带重试机制"""
    for attempt in range(retry):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1d')
            
            if hist.empty:
                return None
            
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('shortName', info.get('longName', symbol)),
                'price': hist['Close'].iloc[-1],
                'open': hist['Open'].iloc[-1],
                'high': hist['High'].iloc[-1],
                'low': hist['Low'].iloc[-1],
                'volume': hist['Volume'].iloc[-1],
                'previous_close': hist['Close'].iloc[0] if len(hist) > 1 else None,
                'change': hist['Close'].iloc[-1] - hist['Open'].iloc[-1],
                'change_percent': ((hist['Close'].iloc[-1] - hist['Open'].iloc[-1]) / hist['Open'].iloc[-1]) * 100,
            }
        except Exception as e:
            if attempt < retry - 1:
                wait_time = 2 ** attempt  # 指数退避
                print(f"⚠️  请求失败，{wait_time}秒后重试... ({attempt + 1}/{retry})")
                time.sleep(wait_time)
            else:
                print(f"❌ {symbol} 获取失败：{str(e)[:50]}")
                return None
    return None

def print_stock_card(data):
    """打印股票信息卡片"""
    if not data:
        return
    
    symbol = data['symbol']
    name = data['name']
    price = data['price']
    change = data['change']
    change_pct = data['change_percent']
    
    # 涨跌颜色
    if change >= 0:
        trend = "📈"
        sign = "+"
    else:
        trend = "📉"
        sign = ""
    
    print(f"\n{trend} {symbol} - {name}")
    print(f"   当前价格：${price:.2f}")
    print(f"   涨跌：{sign}{change:.2f} ({sign}{change_pct:.2f}%)")
    print(f"   开盘：${data['open']:.2f} | 最高：${data['high']:.2f} | 最低：${data['low']:.2f}")
    print(f"   成交量：{data['volume']:,}")

def main():
    print("=" * 50)
    print("📊 股票价格查询 - yfinance")
    print(f"   更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 获取要查询的股票
    if len(sys.argv) > 1:
        stocks = sys.argv[1:]
    else:
        stocks = DEFAULT_STOCKS
    
    # 查询每只股票
    for i, symbol in enumerate(stocks):
        if i > 0:
            time.sleep(1)  # 避免限流
        
        data = get_stock_info(symbol.upper())
        print_stock_card(data)
    
    print("\n" + "=" * 50)
    print("💡 提示：如遇限流，请稍等片刻后重试")
    print("   用法：python3 stock_price.py AAPL GOOG TSLA")

if __name__ == '__main__':
    main()

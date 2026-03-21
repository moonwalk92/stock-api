#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票价格查询 - 使用 MarketStack API
免费注册：https://marketstack.com/product (每天 1000 次请求)

用法:
    python3 stock_simple.py AAPL
"""

import requests
import sys
from datetime import datetime

# 免费 API Key (注册后替换为你的)
# 注册地址：https://marketstack.com/product
API_KEY = ""  # 留空时使用测试模式

def get_stock_price(symbol):
    """获取股票价格"""
    
    if API_KEY:
        # 使用 MarketStack
        url = f"http://api.marketstack.com/v1/intraday/latest"
        params = {
            'access_key': API_KEY,
            'symbols': symbol
        }
    else:
        # 测试模式 - 返回模拟数据
        print("⚠️  测试模式 (未配置 API Key)")
        print("   请注册 https://marketstack.com/product 获取免费 Key")
        print("   每天 1000 次请求，无需信用卡\n")
        
        # 模拟数据用于测试
        return {
            'symbol': symbol,
            'price': 175.50,
            'change': 2.30,
            'change_percent': 1.33,
            'open': 173.20,
            'high': 176.00,
            'low': 172.80,
            'volume': 52000000,
            'source': 'Test Mode'
        }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            quote = data['data'][0]
            return {
                'symbol': quote['symbol'],
                'price': quote['close'],
                'open': quote['open'],
                'high': quote['high'],
                'low': quote['low'],
                'volume': quote['volume'],
                'source': 'MarketStack'
            }
    except Exception as e:
        print(f"错误：{e}")
    
    return None

def main():
    print("=" * 50)
    print("📊 股票价格查询")
    print(f"   更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    
    data = get_stock_price(symbol.upper())
    
    if data:
        trend = "📈" if data.get('change', 0) >= 0 else "📉"
        sign = "+" if data.get('change', 0) >= 0 else ""
        
        print(f"\n{trend} {data['symbol']}")
        print(f"   当前价格：${data['price']:.2f}")
        if 'change' in data:
            print(f"   涨跌：{sign}{data['change']:.2f} ({sign}{data['change_percent']:.2f}%)")
        if 'open' in data:
            print(f"   开盘：${data['open']:.2f} | 最高：${data.get('high', 0):.2f} | 最低：${data.get('low', 0):.2f}")
        print(f"   数据源：{data.get('source', 'Unknown')}")
    
    print("\n" + "=" * 50)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票查询 Web API - FastAPI 版本
部署到 Railway: https://railway.app

API 文档：http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
from datetime import datetime
import os

# ============== 配置 ==============
API_KEY = os.getenv("MARKETSTACK_API_KEY", "a3e52a1083788b9f3afa054fe53cda7f")
# ==================================

app = FastAPI(
    title="📊 股票查询 API",
    description="使用 MarketStack API 查询美股价格数据",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== 数据模型 ==============

class StockData(BaseModel):
    symbol: str
    name: str
    price: float
    open: float
    high: float
    low: float
    volume: int
    change: float
    change_percent: float
    date: str
    source: str


class StockResponse(BaseModel):
    success: bool
    data: Optional[StockData] = None
    error: Optional[str] = None


class MultiStockResponse(BaseModel):
    success: bool
    data: List[StockData] = []
    errors: List[str] = []


# ============== API 端点 ==============

@app.get("/", tags=["Root"])
async def root():
    """API 首页"""
    return {
        "message": "📊 股票查询 API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "stock": "/stock/{symbol} - 查询单只股票",
            "stocks": "/stocks - 查询多只股票",
            "history": "/history/{symbol} - 历史数据"
        }
    }


@app.get("/stock/{symbol}", response_model=StockResponse, tags=["Stock"])
async def get_stock(symbol: str):
    """
    查询单只股票的最新价格
    
    - **symbol**: 股票代码 (如：AAPL, GOOG, TSLA)
    """
    result = fetch_stock_price(symbol.upper())
    
    if result:
        return StockResponse(success=True, data=StockData(**result))
    else:
        return StockResponse(success=False, error=f"无法获取 {symbol} 的数据")


@app.get("/stocks", response_model=MultiStockResponse, tags=["Stock"])
async def get_stocks(symbols: str = Query(..., description="股票代码列表，逗号分隔 (如：AAPL,GOOG,MSFT)")):
    """
    查询多只股票
    
    - **symbols**: 股票代码列表，逗号分隔
    """
    symbol_list = [s.strip().upper() for s in symbols.split(",")]
    
    results = []
    errors = []
    
    for symbol in symbol_list:
        data = fetch_stock_price(symbol)
        if data:
            results.append(StockData(**data))
        else:
            errors.append(f"{symbol} 数据获取失败")
    
    return MultiStockResponse(
        success=len(results) > 0,
        data=results,
        errors=errors
    )


@app.get("/history/{symbol}", tags=["Stock"])
async def get_history(symbol: str, limit: int = Query(30, ge=1, le=100)):
    """
    获取股票历史数据
    
    - **symbol**: 股票代码
    - **limit**: 返回天数 (1-100)
    """
    data = fetch_daily_data(symbol.upper(), limit)
    
    if data:
        return {"success": True, "symbol": symbol.upper(), "data": data, "count": len(data)}
    else:
        raise HTTPException(status_code=404, detail=f"无法获取 {symbol} 的历史数据")


@app.get("/default", response_model=MultiStockResponse, tags=["Stock"])
async def get_default_stocks():
    """
    查询默认监控股票列表
    """
    default_stocks = ['AAPL', 'GOOG', 'MSFT', 'NVDA', 'TSLA']
    
    results = []
    errors = []
    
    for symbol in default_stocks:
        data = fetch_stock_price(symbol)
        if data:
            results.append(StockData(**data))
        else:
            errors.append(f"{symbol} 数据获取失败")
    
    return MultiStockResponse(
        success=len(results) > 0,
        data=results,
        errors=errors
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_configured": bool(API_KEY and API_KEY != "YOUR_API_KEY")
    }


# ============== 工具函数 ==============

def fetch_stock_price(symbol: str) -> Optional[dict]:
    """获取股票最新价格"""
    if not API_KEY:
        return None
    
    try:
        url = "http://api.marketstack.com/v1/eod"
        params = {
            'access_key': API_KEY,
            'symbols': symbol,
            'limit': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'error' in data:
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
                'volume': int(quote.get('volume', 0)),
                'change': round(change, 2),
                'change_percent': round(change_pct, 2),
                'date': quote.get('date', '')[:10],
                'source': 'MarketStack EOD'
            }
    except:
        pass
    
    return None


def fetch_daily_data(symbol: str, limit: int = 30) -> Optional[list]:
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
数据获取模块 - 从加密货币交易所获取数据
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import logging
import time

logger = logging.getLogger(__name__)


class CryptoDataFetcher:
    """加密货币数据获取器"""
    
    def __init__(self, exchange='binance'):
        """
        初始化数据获取器
        
        Args:
            exchange: 交易所名称，默认为binance
        """
        self.exchange = exchange
        self.base_url = 'https://api.binance.com/api/v3'
        
    def get_historical_data(self, symbol, start_date, end_date, interval='1d'):
        """
        获取历史K线数据
        
        Args:
            symbol: 交易对符号 (例如: BTCUSDT)
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            interval: K线间隔 (1m, 5m, 15m, 1h, 4h, 1d等)
        
        Returns:
            DataFrame: 包含OHLCV数据
        """
        try:
            # 转换日期为时间戳
            start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
            end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)
            
            all_data = []
            current_ts = start_ts
            
            logger.info(f"开始获取 {symbol} 的历史数据...")
            
            while current_ts < end_ts:
                url = f"{self.base_url}/klines"
                params = {
                    'symbol': symbol,
                    'interval': interval,
                    'startTime': current_ts,
                    'endTime': end_ts,
                    'limit': 1000
                }
                
                response = requests.get(url, params=params)
                
                if response.status_code != 200:
                    logger.error(f"API请求失败: {response.status_code}")
                    break
                
                data = response.json()
                
                if not data:
                    break
                
                all_data.extend(data)
                current_ts = data[-1][0] + 1
                
                # 避免API限流
                time.sleep(0.5)
            
            if not all_data:
                logger.warning("未获取到任何数据")
                return None
            
            # 转换为DataFrame
            df = pd.DataFrame(all_data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ])
            
            # 数据类型转换
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            
            df.set_index('timestamp', inplace=True)
            df = df[['open', 'high', 'low', 'close', 'volume']]
            
            logger.info(f"成功获取 {len(df)} 条历史数据")
            return df
            
        except Exception as e:
            logger.error(f"获取历史数据时出错: {str(e)}")
            return None
    
    def get_realtime_data(self, symbol, limit=100, interval='1h'):
        """
        获取实时数据
        
        Args:
            symbol: 交易对符号
            limit: 获取的K线数量
            interval: K线间隔
        
        Returns:
            DataFrame: 最新的K线数据
        """
        try:
            url = f"{self.base_url}/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                logger.error(f"API请求失败: {response.status_code}")
                return None
            
            data = response.json()
            
            df = pd.DataFrame(data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ])
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            
            df.set_index('timestamp', inplace=True)
            df = df[['open', 'high', 'low', 'close', 'volume']]
            
            return df
            
        except Exception as e:
            logger.error(f"获取实时数据时出错: {str(e)}")
            return None
    
    def get_market_info(self, symbol):
        """
        获取市场信息
        
        Args:
            symbol: 交易对符号
        
        Returns:
            dict: 市场信息
        """
        try:
            # 获取24小时ticker
            url = f"{self.base_url}/ticker/24hr"
            params = {'symbol': symbol}
            
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                logger.error(f"API请求失败: {response.status_code}")
                return None
            
            data = response.json()
            
            info = {
                '交易对': symbol,
                '当前价格': f"${float(data['lastPrice']):.2f}",
                '24h涨跌幅': f"{float(data['priceChangePercent']):.2f}%",
                '24h最高价': f"${float(data['highPrice']):.2f}",
                '24h最低价': f"${float(data['lowPrice']):.2f}",
                '24h成交量': f"{float(data['volume']):.2f}",
                '24h成交额': f"${float(data['quoteVolume']):.2f}"
            }
            
            return info
            
        except Exception as e:
            logger.error(f"获取市场信息时出错: {str(e)}")
            return None
    
    def get_current_price(self, symbol):
        """
        获取当前价格
        
        Args:
            symbol: 交易对符号
        
        Returns:
            float: 当前价格
        """
        try:
            url = f"{self.base_url}/ticker/price"
            params = {'symbol': symbol}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return float(data['price'])
            else:
                return None
                
        except Exception as e:
            logger.error(f"获取当前价格时出错: {str(e)}")
            return None

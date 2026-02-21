"""
技术指标计算模块
"""

import pandas as pd
import numpy as np


class TechnicalIndicators:
    """技术指标计算类"""
    
    @staticmethod
    def moving_average(data, period, column='close'):
        """
        计算移动平均线
        
        Args:
            data: DataFrame
            period: 周期
            column: 计算列名
        
        Returns:
            Series: 移动平均值
        """
        return data[column].rolling(window=period).mean()
    
    @staticmethod
    def exponential_moving_average(data, period, column='close'):
        """
        计算指数移动平均线
        
        Args:
            data: DataFrame
            period: 周期
            column: 计算列名
        
        Returns:
            Series: EMA值
        """
        return data[column].ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def rsi(data, period=14, column='close'):
        """
        计算相对强弱指标 (RSI)
        
        Args:
            data: DataFrame
            period: 周期
            column: 计算列名
        
        Returns:
            Series: RSI值
        """
        delta = data[column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def macd(data, fast_period=12, slow_period=26, signal_period=9, column='close'):
        """
        计算MACD指标
        
        Args:
            data: DataFrame
            fast_period: 快线周期
            slow_period: 慢线周期
            signal_period: 信号线周期
            column: 计算列名
        
        Returns:
            tuple: (MACD线, 信号线, MACD柱)
        """
        ema_fast = data[column].ewm(span=fast_period, adjust=False).mean()
        ema_slow = data[column].ewm(span=slow_period, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        macd_histogram = macd_line - signal_line
        
        return macd_line, signal_line, macd_histogram
    
    @staticmethod
    def bollinger_bands(data, period=20, std_dev=2, column='close'):
        """
        计算布林带
        
        Args:
            data: DataFrame
            period: 周期
            std_dev: 标准差倍数
            column: 计算列名
        
        Returns:
            tuple: (上轨, 中轨, 下轨)
        """
        middle_band = data[column].rolling(window=period).mean()
        std = data[column].rolling(window=period).std()
        
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        
        return upper_band, middle_band, lower_band
    
    @staticmethod
    def stochastic_oscillator(data, period=14):
        """
        计算随机震荡指标
        
        Args:
            data: DataFrame
            period: 周期
        
        Returns:
            Series: %K值
        """
        low_min = data['low'].rolling(window=period).min()
        high_max = data['high'].rolling(window=period).max()
        
        k = 100 * ((data['close'] - low_min) / (high_max - low_min))
        
        return k
    
    @staticmethod
    def atr(data, period=14):
        """
        计算平均真实波幅 (ATR)
        
        Args:
            data: DataFrame
            period: 周期
        
        Returns:
            Series: ATR值
        """
        high_low = data['high'] - data['low']
        high_close = np.abs(data['high'] - data['close'].shift())
        low_close = np.abs(data['low'] - data['close'].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def obv(data):
        """
        计算能量潮 (OBV)
        
        Args:
            data: DataFrame
        
        Returns:
            Series: OBV值
        """
        obv = (np.sign(data['close'].diff()) * data['volume']).fillna(0).cumsum()
        return obv
    
    @staticmethod
    def add_all_indicators(data):
        """
        添加所有常用技术指标
        
        Args:
            data: DataFrame
        
        Returns:
            DataFrame: 添加了技术指标的数据
        """
        df = data.copy()
        
        # 移动平均线
        df['ma_7'] = TechnicalIndicators.moving_average(df, 7)
        df['ma_25'] = TechnicalIndicators.moving_average(df, 25)
        df['ma_50'] = TechnicalIndicators.moving_average(df, 50)
        df['ma_200'] = TechnicalIndicators.moving_average(df, 200)
        
        # EMA
        df['ema_12'] = TechnicalIndicators.exponential_moving_average(df, 12)
        df['ema_26'] = TechnicalIndicators.exponential_moving_average(df, 26)
        
        # RSI
        df['rsi'] = TechnicalIndicators.rsi(df, 14)
        
        # MACD
        macd_line, signal_line, macd_histogram = TechnicalIndicators.macd(df)
        df['macd'] = macd_line
        df['macd_signal'] = signal_line
        df['macd_histogram'] = macd_histogram
        
        # 布林带
        upper, middle, lower = TechnicalIndicators.bollinger_bands(df)
        df['bb_upper'] = upper
        df['bb_middle'] = middle
        df['bb_lower'] = lower
        
        # 随机震荡指标
        df['stoch_k'] = TechnicalIndicators.stochastic_oscillator(df)
        
        # ATR
        df['atr'] = TechnicalIndicators.atr(df)
        
        # OBV
        df['obv'] = TechnicalIndicators.obv(df)
        
        return df

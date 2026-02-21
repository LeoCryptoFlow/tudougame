"""
交易策略模块
"""

import pandas as pd
import numpy as np
from indicators import TechnicalIndicators
import logging

logger = logging.getLogger(__name__)


class TradingStrategy:
    """交易策略类"""
    
    def __init__(self, strategy_name='ma_crossover'):
        """
        初始化交易策略
        
        Args:
            strategy_name: 策略名称
        """
        self.strategy_name = strategy_name
        self.strategies = {
            'ma_crossover': self.ma_crossover_strategy,
            'rsi': self.rsi_strategy,
            'macd': self.macd_strategy,
            'combined': self.combined_strategy
        }
    
    def generate_signals(self, data):
        """
        生成交易信号
        
        Args:
            data: DataFrame包含OHLCV数据
        
        Returns:
            DataFrame: 添加了交易信号的数据
        """
        if self.strategy_name not in self.strategies:
            logger.error(f"未知策略: {self.strategy_name}")
            return data
        
        # 添加技术指标
        df = TechnicalIndicators.add_all_indicators(data)
        
        # 应用策略
        df = self.strategies[self.strategy_name](df)
        
        return df
    
    def ma_crossover_strategy(self, data):
        """
        移动平均线交叉策略
        
        当短期均线上穿长期均线时买入，下穿时卖出
        
        Args:
            data: DataFrame
        
        Returns:
            DataFrame: 添加了信号的数据
        """
        df = data.copy()
        
        # 初始化信号
        df['signal'] = 'HOLD'
        
        # 金叉：短期均线上穿长期均线
        golden_cross = (df['ma_7'] > df['ma_25']) & (df['ma_7'].shift(1) <= df['ma_25'].shift(1))
        
        # 死叉：短期均线下穿长期均线
        death_cross = (df['ma_7'] < df['ma_25']) & (df['ma_7'].shift(1) >= df['ma_25'].shift(1))
        
        df.loc[golden_cross, 'signal'] = 'BUY'
        df.loc[death_cross, 'signal'] = 'SELL'
        
        logger.info(f"MA交叉策略 - 买入信号: {golden_cross.sum()}, 卖出信号: {death_cross.sum()}")
        
        return df
    
    def rsi_strategy(self, data):
        """
        RSI策略
        
        RSI < 30 超卖买入，RSI > 70 超买卖出
        
        Args:
            data: DataFrame
        
        Returns:
            DataFrame: 添加了信号的数据
        """
        df = data.copy()
        
        df['signal'] = 'HOLD'
        
        # 超卖区买入
        oversold = (df['rsi'] < 30) & (df['rsi'].shift(1) >= 30)
        
        # 超买区卖出
        overbought = (df['rsi'] > 70) & (df['rsi'].shift(1) <= 70)
        
        df.loc[oversold, 'signal'] = 'BUY'
        df.loc[overbought, 'signal'] = 'SELL'
        
        logger.info(f"RSI策略 - 买入信号: {oversold.sum()}, 卖出信号: {overbought.sum()}")
        
        return df
    
    def macd_strategy(self, data):
        """
        MACD策略
        
        MACD线上穿信号线买入，下穿卖出
        
        Args:
            data: DataFrame
        
        Returns:
            DataFrame: 添加了信号的数据
        """
        df = data.copy()
        
        df['signal'] = 'HOLD'
        
        # MACD金叉
        macd_bullish = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1))
        
        # MACD死叉
        macd_bearish = (df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1))
        
        df.loc[macd_bullish, 'signal'] = 'BUY'
        df.loc[macd_bearish, 'signal'] = 'SELL'
        
        logger.info(f"MACD策略 - 买入信号: {macd_bullish.sum()}, 卖出信号: {macd_bearish.sum()}")
        
        return df
    
    def combined_strategy(self, data):
        """
        组合策略
        
        结合MA、RSI和MACD的多重确认
        
        Args:
            data: DataFrame
        
        Returns:
            DataFrame: 添加了信号的数据
        """
        df = data.copy()
        
        df['signal'] = 'HOLD'
        
        # 买入条件：多个指标确认
        buy_conditions = (
            # MA金叉
            (df['ma_7'] > df['ma_25']) &
            # RSI不在超买区
            (df['rsi'] < 70) &
            # MACD为正或即将金叉
            ((df['macd'] > df['macd_signal']) | (df['macd_histogram'] > df['macd_histogram'].shift(1))) &
            # 价格在中期均线之上
            (df['close'] > df['ma_50'])
        )
        
        # 卖出条件：多个指标确认
        sell_conditions = (
            # MA死叉
            (df['ma_7'] < df['ma_25']) &
            # RSI不在超卖区
            (df['rsi'] > 30) &
            # MACD为负或即将死叉
            ((df['macd'] < df['macd_signal']) | (df['macd_histogram'] < df['macd_histogram'].shift(1))) &
            # 价格在中期均线之下
            (df['close'] < df['ma_50'])
        )
        
        df.loc[buy_conditions, 'signal'] = 'BUY'
        df.loc[sell_conditions, 'signal'] = 'SELL'
        
        logger.info(f"组合策略 - 买入信号: {buy_conditions.sum()}, 卖出信号: {sell_conditions.sum()}")
        
        return df
    
    def get_strategy_description(self):
        """获取策略描述"""
        descriptions = {
            'ma_crossover': '移动平均线交叉策略 - 短期MA(7)与长期MA(25)交叉',
            'rsi': 'RSI策略 - 超卖(<30)买入，超买(>70)卖出',
            'macd': 'MACD策略 - MACD线与信号线交叉',
            'combined': '组合策略 - 结合MA、RSI、MACD的多重确认'
        }
        return descriptions.get(self.strategy_name, '未知策略')

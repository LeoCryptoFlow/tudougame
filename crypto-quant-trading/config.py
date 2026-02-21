"""
配置文件
"""

class Config:
    """系统配置类"""
    
    # 交易所配置
    EXCHANGE = 'binance'
    BASE_URL = 'https://api.binance.com/api/v3'
    
    # 默认交易对
    DEFAULT_SYMBOL = 'BTCUSDT'
    
    # 回测配置
    INITIAL_CAPITAL = 10000  # 初始资金（美元）
    COMMISSION = 0.001  # 手续费率 (0.1%)
    
    # 数据配置
    DEFAULT_INTERVAL = '1d'  # K线间隔
    DEFAULT_LIMIT = 100  # 默认获取数据条数
    
    # 策略配置
    MA_SHORT_PERIOD = 7
    MA_LONG_PERIOD = 25
    MA_MID_PERIOD = 50
    MA_SUPER_LONG_PERIOD = 200
    
    RSI_PERIOD = 14
    RSI_OVERSOLD = 30
    RSI_OVERBOUGHT = 70
    
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    BOLLINGER_PERIOD = 20
    BOLLINGER_STD = 2
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'trading.log'
    
    # 图表配置
    PLOT_STYLE = 'seaborn'
    FIGURE_SIZE = (14, 10)
    DPI = 300
    
    # 风险管理
    MAX_POSITION_SIZE = 1.0  # 最大仓位比例
    STOP_LOSS_PCT = 0.05  # 止损比例 (5%)
    TAKE_PROFIT_PCT = 0.15  # 止盈比例 (15%)
    
    @classmethod
    def get_config(cls):
        """获取所有配置"""
        return {
            'exchange': cls.EXCHANGE,
            'initial_capital': cls.INITIAL_CAPITAL,
            'commission': cls.COMMISSION,
            'default_symbol': cls.DEFAULT_SYMBOL,
            'ma_periods': {
                'short': cls.MA_SHORT_PERIOD,
                'long': cls.MA_LONG_PERIOD,
                'mid': cls.MA_MID_PERIOD
            },
            'rsi': {
                'period': cls.RSI_PERIOD,
                'oversold': cls.RSI_OVERSOLD,
                'overbought': cls.RSI_OVERBOUGHT
            }
        }

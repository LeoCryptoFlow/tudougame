#!/usr/bin/env python3
"""
加密货币量化交易系统 - 主程序
"""

import argparse
import logging
from datetime import datetime
from data_fetcher import CryptoDataFetcher
from strategy import TradingStrategy
from backtester import Backtester
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_backtest(symbol, start_date, end_date, strategy_name='ma_crossover', initial_capital=10000):
    """运行回测"""
    logger.info(f"开始回测 {symbol} 从 {start_date} 到 {end_date}")
    logger.info(f"使用策略: {strategy_name}, 初始资金: ${initial_capital}")
    
    # 获取历史数据
    fetcher = CryptoDataFetcher()
    df = fetcher.get_historical_data(symbol, start_date, end_date)
    
    if df is None or df.empty:
        logger.error("无法获取历史数据")
        return
    
    logger.info(f"成功获取 {len(df)} 条历史数据")
    
    # 初始化策略
    strategy = TradingStrategy(strategy_name)
    
    # 运行回测
    backtester = Backtester(initial_capital)
    results = backtester.run(df, strategy)
    
    # 显示结果
    backtester.print_results(results)
    backtester.plot_results(results, symbol)


def run_live_trading(symbol, strategy_name='ma_crossover', initial_capital=10000):
    """运行实时交易模拟"""
    logger.info(f"开始实时交易模拟 {symbol}")
    logger.info(f"使用策略: {strategy_name}, 初始资金: ${initial_capital}")
    
    fetcher = CryptoDataFetcher()
    strategy = TradingStrategy(strategy_name)
    
    # 获取最新数据
    df = fetcher.get_realtime_data(symbol, limit=100)
    
    if df is None or df.empty:
        logger.error("无法获取实时数据")
        return
    
    # 生成信号
    signals = strategy.generate_signals(df)
    latest_signal = signals.iloc[-1]
    
    logger.info(f"当前价格: ${df['close'].iloc[-1]:.2f}")
    logger.info(f"交易信号: {latest_signal['signal']}")
    
    if latest_signal['signal'] == 'BUY':
        logger.info("💰 建议买入！")
    elif latest_signal['signal'] == 'SELL':
        logger.info("📉 建议卖出！")
    else:
        logger.info("⏸️ 持有当前仓位")


def show_market_info(symbol):
    """显示市场信息"""
    fetcher = CryptoDataFetcher()
    info = fetcher.get_market_info(symbol)
    
    if info:
        print("\n" + "="*50)
        print(f"市场信息: {symbol}")
        print("="*50)
        for key, value in info.items():
            print(f"{key}: {value}")
        print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(description='加密货币量化交易系统')
    parser.add_argument('--mode', choices=['backtest', 'live', 'info'], 
                       default='backtest', help='运行模式')
    parser.add_argument('--symbol', default='BTCUSDT', 
                       help='交易对符号 (例如: BTCUSDT, ETHUSDT)')
    parser.add_argument('--strategy', default='ma_crossover',
                       choices=['ma_crossover', 'rsi', 'macd', 'combined'],
                       help='交易策略')
    parser.add_argument('--start', default='2024-01-01', 
                       help='回测开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end', default=datetime.now().strftime('%Y-%m-%d'),
                       help='回测结束日期 (YYYY-MM-DD)')
    parser.add_argument('--capital', type=float, default=10000,
                       help='初始资金')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🚀 加密货币量化交易系统")
    print("="*60 + "\n")
    
    if args.mode == 'backtest':
        run_backtest(args.symbol, args.start, args.end, 
                    args.strategy, args.capital)
    elif args.mode == 'live':
        run_live_trading(args.symbol, args.strategy, args.capital)
    elif args.mode == 'info':
        show_market_info(args.symbol)


if __name__ == '__main__':
    main()

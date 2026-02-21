"""
回测系统模块
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Backtester:
    """回测系统类"""
    
    def __init__(self, initial_capital=10000, commission=0.001):
        """
        初始化回测系统
        
        Args:
            initial_capital: 初始资金
            commission: 交易手续费率
        """
        self.initial_capital = initial_capital
        self.commission = commission
    
    def run(self, data, strategy):
        """
        运行回测
        
        Args:
            data: DataFrame包含OHLCV数据
            strategy: 交易策略对象
        
        Returns:
            dict: 回测结果
        """
        logger.info("开始运行回测...")
        
        # 生成交易信号
        df = strategy.generate_signals(data)
        
        # 初始化回测变量
        capital = self.initial_capital
        position = 0  # 持仓数量
        portfolio_value = []
        trades = []
        
        # 遍历数据进行回测
        for i, (timestamp, row) in enumerate(df.iterrows()):
            current_price = row['close']
            signal = row['signal']
            
            # 计算当前组合价值
            current_value = capital + position * current_price
            portfolio_value.append({
                'timestamp': timestamp,
                'value': current_value,
                'capital': capital,
                'position': position,
                'price': current_price
            })
            
            # 执行交易
            if signal == 'BUY' and position == 0:
                # 买入：使用所有可用资金
                position = capital / current_price * (1 - self.commission)
                capital = 0
                trades.append({
                    'timestamp': timestamp,
                    'type': 'BUY',
                    'price': current_price,
                    'quantity': position,
                    'value': position * current_price
                })
                logger.info(f"买入 - 时间: {timestamp}, 价格: ${current_price:.2f}, 数量: {position:.6f}")
                
            elif signal == 'SELL' and position > 0:
                # 卖出：清空所有持仓
                capital = position * current_price * (1 - self.commission)
                trades.append({
                    'timestamp': timestamp,
                    'type': 'SELL',
                    'price': current_price,
                    'quantity': position,
                    'value': capital
                })
                logger.info(f"卖出 - 时间: {timestamp}, 价格: ${current_price:.2f}, 数量: {position:.6f}")
                position = 0
        
        # 如果最后还有持仓，按最后价格卖出
        if position > 0:
            final_price = df['close'].iloc[-1]
            capital = position * final_price * (1 - self.commission)
            trades.append({
                'timestamp': df.index[-1],
                'type': 'SELL',
                'price': final_price,
                'quantity': position,
                'value': capital
            })
            position = 0
        
        # 计算回测指标
        results = self._calculate_metrics(df, portfolio_value, trades)
        
        logger.info("回测完成！")
        return results
    
    def _calculate_metrics(self, data, portfolio_value, trades):
        """
        计算回测指标
        
        Args:
            data: 原始数据
            portfolio_value: 组合价值历史
            trades: 交易记录
        
        Returns:
            dict: 回测指标
        """
        pv_df = pd.DataFrame(portfolio_value)
        
        # 最终价值
        final_value = pv_df['value'].iloc[-1]
        
        # 总收益
        total_return = final_value - self.initial_capital
        total_return_pct = (total_return / self.initial_capital) * 100
        
        # 买入持有策略收益
        buy_hold_return = (data['close'].iloc[-1] / data['close'].iloc[0] - 1) * 100
        
        # 最大回撤
        cumulative_max = pv_df['value'].cummax()
        drawdown = (pv_df['value'] - cumulative_max) / cumulative_max * 100
        max_drawdown = drawdown.min()
        
        # 夏普比率 (简化版本，假设无风险利率为0)
        returns = pv_df['value'].pct_change().dropna()
        if len(returns) > 0 and returns.std() != 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)  # 年化
        else:
            sharpe_ratio = 0
        
        # 胜率
        if len(trades) >= 2:
            profitable_trades = 0
            for i in range(1, len(trades), 2):
                if i < len(trades):
                    buy_trade = trades[i-1]
                    sell_trade = trades[i]
                    if sell_trade['price'] > buy_trade['price']:
                        profitable_trades += 1
            win_rate = (profitable_trades / (len(trades) // 2)) * 100 if len(trades) > 0 else 0
        else:
            win_rate = 0
        
        # 交易次数
        num_trades = len(trades)
        
        results = {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'buy_hold_return': buy_hold_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'num_trades': num_trades,
            'portfolio_value': pv_df,
            'trades': trades,
            'price_data': data
        }
        
        return results
    
    def print_results(self, results):
        """
        打印回测结果
        
        Args:
            results: 回测结果字典
        """
        print("\n" + "="*60)
        print("📊 回测结果")
        print("="*60)
        print(f"初始资金:        ${results['initial_capital']:,.2f}")
        print(f"最终价值:        ${results['final_value']:,.2f}")
        print(f"总收益:          ${results['total_return']:,.2f}")
        print(f"收益率:          {results['total_return_pct']:.2f}%")
        print(f"买入持有收益率:  {results['buy_hold_return']:.2f}%")
        print("-"*60)
        print(f"最大回撤:        {results['max_drawdown']:.2f}%")
        print(f"夏普比率:        {results['sharpe_ratio']:.2f}")
        print(f"胜率:            {results['win_rate']:.2f}%")
        print(f"交易次数:        {results['num_trades']}")
        print("="*60 + "\n")
        
        # 打印交易记录
        if results['trades']:
            print("📝 交易记录（最近10笔）:")
            print("-"*60)
            for trade in results['trades'][-10:]:
                print(f"{trade['timestamp']} | {trade['type']:4s} | "
                      f"价格: ${trade['price']:,.2f} | "
                      f"数量: {trade['quantity']:.6f}")
            print("-"*60 + "\n")
    
    def plot_results(self, results, symbol='BTC'):
        """
        绘制回测结果图表
        
        Args:
            results: 回测结果字典
            symbol: 交易对符号
        """
        try:
            fig, axes = plt.subplots(3, 1, figsize=(14, 10))
            fig.suptitle(f'{symbol} 回测结果', fontsize=16, fontweight='bold')
            
            pv_df = results['portfolio_value']
            price_data = results['price_data']
            
            # 1. 价格图表
            ax1 = axes[0]
            ax1.plot(price_data.index, price_data['close'], label='价格', color='blue', linewidth=1.5)
            
            # 标记买卖点
            buy_trades = [t for t in results['trades'] if t['type'] == 'BUY']
            sell_trades = [t for t in results['trades'] if t['type'] == 'SELL']
            
            if buy_trades:
                buy_times = [t['timestamp'] for t in buy_trades]
                buy_prices = [t['price'] for t in buy_trades]
                ax1.scatter(buy_times, buy_prices, color='green', marker='^', 
                           s=100, label='买入', zorder=5)
            
            if sell_trades:
                sell_times = [t['timestamp'] for t in sell_trades]
                sell_prices = [t['price'] for t in sell_trades]
                ax1.scatter(sell_times, sell_prices, color='red', marker='v', 
                           s=100, label='卖出', zorder=5)
            
            ax1.set_ylabel('价格 (USD)', fontsize=12)
            ax1.legend(loc='upper left')
            ax1.grid(True, alpha=0.3)
            ax1.set_title('价格走势与交易信号', fontsize=12)
            
            # 2. 组合价值图表
            ax2 = axes[1]
            ax2.plot(pv_df['timestamp'], pv_df['value'], label='组合价值', 
                    color='green', linewidth=2)
            ax2.axhline(y=self.initial_capital, color='gray', linestyle='--', 
                       label='初始资金', alpha=0.7)
            ax2.set_ylabel('组合价值 (USD)', fontsize=12)
            ax2.legend(loc='upper left')
            ax2.grid(True, alpha=0.3)
            ax2.set_title(f'组合价值变化 (收益: {results["total_return_pct"]:.2f}%)', 
                         fontsize=12)
            
            # 3. 回撤图表
            ax3 = axes[2]
            cumulative_max = pv_df['value'].cummax()
            drawdown = (pv_df['value'] - cumulative_max) / cumulative_max * 100
            ax3.fill_between(pv_df['timestamp'], drawdown, 0, color='red', alpha=0.3)
            ax3.plot(pv_df['timestamp'], drawdown, color='red', linewidth=1)
            ax3.set_ylabel('回撤 (%)', fontsize=12)
            ax3.set_xlabel('时间', fontsize=12)
            ax3.grid(True, alpha=0.3)
            ax3.set_title(f'回撤分析 (最大回撤: {results["max_drawdown"]:.2f}%)', 
                         fontsize=12)
            
            plt.tight_layout()
            
            # 保存图表
            filename = f'backtest_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            logger.info(f"图表已保存: {filename}")
            
            plt.show()
            
        except Exception as e:
            logger.error(f"绘制图表时出错: {str(e)}")

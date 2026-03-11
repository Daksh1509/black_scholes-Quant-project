import numpy as np
import matplotlib.pyplot as plt
import os
from src.black_scholes import BlackScholes
from src.real_data import get_live_estimate

os.makedirs('outputs', exist_ok=True)


def print_sample_pricing():
    print("\n--- Sample Pricing (S=150, K=155, T=0.5, r=5%, σ=25%) ---")
    bs = BlackScholes(S=150, K=155, T=0.5, r=0.05, sigma=0.25)
    print(f"Call Price : ${bs.call_price():.2f}")
    print(f"Put Price  : ${bs.put_price():.2f}")
    print("\nGreeks (Call):")
    for name, val in bs.all_greeks('call').items():
        print(f"  {name:<8}: {val:.4f}")


def generate_price_chart():
    stock_prices = np.linspace(100, 200, 300)
    call_prices  = [BlackScholes(s, 155, 0.5, 0.05, 0.25).call_price() for s in stock_prices]
    put_prices   = [BlackScholes(s, 155, 0.5, 0.05, 0.25).put_price()  for s in stock_prices]

    plt.figure(figsize=(10, 5))
    plt.plot(stock_prices, call_prices, label='Call Price', color='green', linewidth=2)
    plt.plot(stock_prices, put_prices,  label='Put Price',  color='red',   linewidth=2)
    plt.axvline(x=155, linestyle='--', color='gray', label='Strike (K=155)')
    plt.title('Black-Scholes Option Prices vs Stock Price')
    plt.xlabel('Stock Price ($)')
    plt.ylabel('Option Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/bs_option_prices.png', dpi=150)
    plt.close()
    print("\nSaved → outputs/bs_option_prices.png")


def generate_greeks_chart():
    stock_range = np.linspace(80, 220, 300)
    params = dict(K=155, T=0.5, r=0.05, sigma=0.25)

    greeks_data = {
        'Delta (Call)': [BlackScholes(s, **params).delta('call') for s in stock_range],
        'Gamma':        [BlackScholes(s, **params).gamma()        for s in stock_range],
        'Vega':         [BlackScholes(s, **params).vega()         for s in stock_range],
        'Theta (Call)': [BlackScholes(s, **params).theta('call')  for s in stock_range],
        'Rho (Call)':   [BlackScholes(s, **params).rho('call')    for s in stock_range],
    }

    colors = ['steelblue', 'darkorange', 'green', 'red', 'purple']
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    for ax, (name, values), color in zip(axes.flat, greeks_data.items(), colors):
        ax.plot(stock_range, values, color=color, linewidth=2)
        ax.axvline(x=155, linestyle='--', color='gray', alpha=0.5)
        ax.set_title(name, fontsize=13)
        ax.set_xlabel('Stock Price ($)')
        ax.grid(True, alpha=0.3)
    axes.flat[-1].set_visible(False)
    fig.suptitle('Black-Scholes Greeks Sensitivity', fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/greeks_plot.png', dpi=150)
    plt.close()
    print("Saved → outputs/greeks_plot.png")


if __name__ == '__main__':
    print_sample_pricing()
    generate_price_chart()
    generate_greeks_chart()
    get_live_estimate(ticker='AAPL')

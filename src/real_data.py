import yfinance as yf
import numpy as np
from src.black_scholes import BlackScholes


def get_historical_volatility(ticker: str, period: str = '1y') -> float:
    """Download historical data and compute annualized volatility."""
    data = yf.download(ticker, period=period, progress=False)
    log_returns = np.log(data['Close'] / data['Close'].shift(1)).dropna()
    return float(log_returns.std() * np.sqrt(252))


def get_current_price(ticker: str) -> float:
    """Get the latest closing price for a ticker."""
    data = yf.download(ticker, period='5d', progress=False)
    return float(data['Close'].iloc[-1])


def get_live_estimate(ticker: str = 'AAPL', T: float = 0.25, r: float = 0.05,
                       strike_offset: float = 1.05):
    """
    Price an ATM option using live data.
    strike_offset: strike = S * offset (1.05 = 5% OTM call)
    """
    print(f"\n{'='*50}")
    print(f"  Live Black-Scholes Estimate for {ticker}")
    print(f"{'='*50}")

    S = get_current_price(ticker)
    sigma = get_historical_volatility(ticker)
    K = S * strike_offset

    bs = BlackScholes(S=S, K=K, T=T, r=r, sigma=sigma)

    print(f"  Current Price (S):    ${S:.2f}")
    print(f"  Strike Price (K):     ${K:.2f}")
    print(f"  Historical Vol (σ):   {sigma:.2%}")
    print(f"  Time to Expiry (T):   {T} years")
    print(f"  Risk-Free Rate (r):   {r:.2%}")
    print(f"\n  Call Price:  ${bs.call_price():.2f}")
    print(f"  Put Price:   ${bs.put_price():.2f}")
    print(f"\n  Greeks (Call):")
    for name, val in bs.all_greeks('call').items():
        print(f"    {name:<8}: {val:.4f}")
    print(f"{'='*50}\n")

    return bs

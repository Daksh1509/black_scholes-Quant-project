import numpy as np
from scipy.stats import norm


class BlackScholes:
    def __init__(self, S, K, T, r, sigma):
        """
        S     = Current stock price
        K     = Strike price
        T     = Time to expiry in years (e.g., 0.5 = 6 months)
        r     = Risk-free interest rate (e.g., 0.05 = 5%)
        sigma = Volatility of the underlying (e.g., 0.2 = 20%)
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        self.d2 = self.d1 - sigma * np.sqrt(T)

    def call_price(self):
        return self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)

    def put_price(self):
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)

    def delta(self, option='call'):
        if option == 'call':
            return norm.cdf(self.d1)
        return norm.cdf(self.d1) - 1

    def gamma(self):
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) / 100

    def theta(self, option='call'):
        common = -(self.S * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T))
        if option == 'call':
            return (common - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)) / 365
        return (common + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)) / 365

    def rho(self, option='call'):
        if option == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) / 100
        return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2) / 100

    def all_greeks(self, option='call'):
        return {
            'Delta': self.delta(option),
            'Gamma': self.gamma(),
            'Vega':  self.vega(),
            'Theta': self.theta(option),
            'Rho':   self.rho(option)
        }

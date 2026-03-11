import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from src.black_scholes import BlackScholes


def test_call_price_known_value():
    bs = BlackScholes(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert abs(bs.call_price() - 10.45) < 0.10, f"Call price unexpected: {bs.call_price()}"
    print("✅ test_call_price_known_value passed")


def test_put_call_parity():
    bs = BlackScholes(S=100, K=100, T=1, r=0.05, sigma=0.2)
    lhs = bs.call_price() - bs.put_price()
    rhs = bs.S - bs.K * np.exp(-bs.r * bs.T)
    assert abs(lhs - rhs) < 0.01, f"Put-Call Parity violated! LHS={lhs:.4f}, RHS={rhs:.4f}"
    print("✅ test_put_call_parity passed")


def test_delta_call_range():
    bs = BlackScholes(S=150, K=155, T=0.5, r=0.05, sigma=0.25)
    assert 0 <= bs.delta('call') <= 1, f"Call delta out of range: {bs.delta('call')}"
    print("✅ test_delta_call_range passed")


def test_delta_put_range():
    bs = BlackScholes(S=150, K=155, T=0.5, r=0.05, sigma=0.25)
    assert -1 <= bs.delta('put') <= 0, f"Put delta out of range: {bs.delta('put')}"
    print("✅ test_delta_put_range passed")


def test_gamma_positive():
    bs = BlackScholes(S=150, K=155, T=0.5, r=0.05, sigma=0.25)
    assert bs.gamma() > 0, "Gamma must always be positive"
    print("✅ test_gamma_positive passed")


def test_vega_positive():
    bs = BlackScholes(S=150, K=155, T=0.5, r=0.05, sigma=0.25)
    assert bs.vega() > 0, "Vega must always be positive"
    print("✅ test_vega_positive passed")


def test_deep_itm_call_delta_near_1():
    bs = BlackScholes(S=200, K=100, T=1, r=0.05, sigma=0.2)
    assert bs.delta('call') > 0.95, "Deep ITM call delta should be near 1"
    print("✅ test_deep_itm_call_delta_near_1 passed")


if __name__ == '__main__':
    test_call_price_known_value()
    test_put_call_parity()
    test_delta_call_range()
    test_delta_put_range()
    test_gamma_positive()
    test_vega_positive()
    test_deep_itm_call_delta_near_1()
    print("\n🎉 All 7 tests passed!")

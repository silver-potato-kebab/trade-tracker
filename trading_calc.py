def get_max_risk_per_day(risk_percentage: float, account_size: float) -> float:
    """Return the maximum dollar risk per day."""
    return risk_percentage / 100 * account_size

def get_max_risk_per_trade(max_risk_per_day: float) -> float:
    """Return the maximum dollar risk per trade."""
    return max_risk_per_day / 2

def get_max_shares_per_trade(account_size: float, share_price: float, stop_price: float, max_dollar_risk_per_trade: float) -> int:
    """Return the maximum purchasable shares allowed per trade."""
    max_purchasable_shares = account_size / share_price
    calculated_shares_to_buy = account_size / (share_price - stop_price)
    return calculated_shares_to_buy if calculated_shares_to_buy < max_purchasable_shares else max_purchasable_shares


max_risk_percentage = 2.0
account_size = 1500
share_price = 8.57
stop_price = 8.50
max_dollar_risk_per_day = get_max_risk_per_day(max_risk_percentage, account_size)
max_dollar_risk_per_trade = get_max_risk_per_trade(max_dollar_risk_per_day)
max_shares_per_trade = round(get_max_shares_per_trade(account_size, share_price, stop_price, max_dollar_risk_per_trade))
print(f"Max Shares Per Trade: {max_shares_per_trade}")

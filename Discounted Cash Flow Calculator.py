import yfinance as yf

def get_discounted_cash_flow(ticker_symbol, shares_outstanding):
    # Fetch financial data
    faang = yf.Ticker(ticker_symbol)
    financial_data = faang.history(period="1y")

    # Check if the necessary columns are available
    if 'Open' not in financial_data.columns or 'Close' not in financial_data.columns:
        print("Financial data is incomplete or unavailable.")
        return

    # Calculate the relevant financial metrics
    ocf = financial_data['Close']
    capex = financial_data['Open']
    rrr = float(input("Enter a desired rate of return (.075 for a conservative return): "))
    pgr = 0.025  # Adjust as needed

    # Use the user-provided shares_outstanding
    sharesout = shares_outstanding

    # Projection period (5 years)
    years = 5

    # Calculate projected cash flows for each year
    proj_cash_flows = []
    for i in range(years):
        proj_ocf = ocf.iloc[i]
        proj_capex = capex.iloc[i]
        proj_fcf = proj_ocf - proj_capex
        proj_cash_flows.append(proj_fcf)

    # Calculate terminal value using Gordon Growth Model
    terminal_ocf = ocf.iloc[years - 1] * (1 + pgr)
    terminal_capex = capex.iloc[years - 1] * (1 + pgr)
    terminal_fcf = terminal_ocf - terminal_capex
    terminal_value = (terminal_fcf * (1 + pgr)) / (rrr - pgr)

    # Calculate the present value of all cash flows
    pv_cash_flows = [cf / (1 + rrr) ** (i + 1) for i, cf in enumerate(proj_cash_flows)]
    pv_cash_flows.append(terminal_value)

    # Calculate fair value
    fcf_fair_value = sum(pv_cash_flows) / sharesout

    return fcf_fair_value

# Input the ticker symbol and shares outstanding
tckr = input("Enter a ticker symbol: ")
shares_outstanding = float(input("Enter the number of shares outstanding:"))

fair_value = get_discounted_cash_flow(tckr, shares_outstanding)

if fair_value is not None:
    print(tckr, "fair value:", fair_value)


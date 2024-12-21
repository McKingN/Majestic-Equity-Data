from utils import MagesticEquityData

if __name__ == '__main__' :
    etf_data = MagesticEquityData()
#     concat_df = etf_data.history(
#     tickers=["Dividend", "Value", "LowVol", "MarketCap", "Momentum", "Quality", "Value"],
#     start="2023-01-01",
#     end="2023-03-31"
# )
#     etf_data.plotter(ticker="Value", color="blue")  # Plot without date filtering
#     etf_data.plotter(ticker="Value", color="green", start="2020-01-03")  # Plot from a start date
#     etf_data.plotter(ticker="Value", color="red", end="2024-01-04")  # Plot until an end date
#     etf_data.plotter(ticker="Value", color="purple", start="2020-01-02", end="2023-01-04")  # Plot between start and end dates
    
#     etf_data.download(ticker="Value", start='2019-12-31')
#     print(concat_df)


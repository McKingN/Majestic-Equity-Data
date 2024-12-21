import json
import pandas as pd
from typing import List
from datetime import datetime
import matplotlib.pyplot as plt

class MagesticEquityData:
    def __init__(self, tickers: List[str] = None):
        """
        Initialize the MagesticEquityData class with a list of tickers.

        Parameters:
            tickers (List[str], optional): The list of tickers for which ETF data is processed.
                                           Defaults to ["Dividend", "Value", "LowVol", "MarketCap",
                                                        "Momentum", "Quality", "Value"] if not provided.
        """
        # Set default tickers if none are provided
        self.tickers = tickers if tickers is not None else [
            "Dividend", "Value", "LowVol", "MarketCap", 
            "Momentum", "Quality", "Value"
        ]

    def process_etf_data(self, ticker: str) -> pd.DataFrame:
        """
        Creates a Pandas DataFrame indexed by dates, containing the ETF prices and the weights of each stock for a specific ticker.

        Parameters:
            ticker (str): The ticker for which the data is processed.

        Returns:
            pd.DataFrame: DataFrame with the "Close Price" column for ETF prices and tickers for weights.
        """
        prices_path = f"./data/{ticker}/SP500{ticker}ETFPrices.json"
        weights_path = f"./data/{ticker}/SP500{ticker}ETFWeights.json"

        # Load the JSON files
        with open(prices_path, 'r') as f:
            prices_data = json.load(f)

        with open(weights_path, 'r') as f:
            weights_data = json.load(f)

        # Convert prices to DataFrame
        prices_df = pd.DataFrame.from_dict(prices_data, orient='index', columns=['Close Price'])

        # Convert weights to DataFrame
        weights_df = pd.DataFrame.from_dict(weights_data, orient='index')

        # Combine the two DataFrames
        combined_df = pd.concat([prices_df, weights_df], axis=1)

        # Ensure the index is of datetime type for future analysis
        combined_df.index = pd.to_datetime(combined_df.index)

        return combined_df

    def filter_df_by_date(self, df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
        """
        Filters a DataFrame between two given dates.

        Parameters:
            df (pd.DataFrame): DataFrame to filter.
            start (str): Start date in "YYYY-MM-DD" format.
            end (str): End date in "YYYY-MM-DD" format.

        Returns:
            pd.DataFrame: DataFrame filtered between the two dates.

        Raises:
            ValueError: If start >= end or if the dates are not within the range of the DataFrame's index.
        """
        # Convert dates to datetime
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)

        # Check that start < end
        if start_date >= end_date:
            raise ValueError("The start date must be strictly earlier than the end date.")

        # Check that the dates are within the range of the DataFrame's index
        if start_date < df.index.min() or end_date > df.index.max():
            raise ValueError("The dates must be within the range of the DataFrame's index.")

        # Find the closest indices if the dates are not exact indices
        if start_date not in df.index:
            start_date = df.index[df.index.searchsorted(start_date, side="left")]

        if end_date not in df.index:
            end_date = df.index[df.index.searchsorted(end_date, side="right") - 1]

        # Filter the DataFrame
        filtered_df = df.loc[start_date:end_date]

        return filtered_df

    def retrieve_etf_data(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """
        Retrieves and filters ETF data between two given dates for a specific ticker.

        Parameters:
            ticker (str): The ticker for which the data is retrieved.
            start (str): Start date in "YYYY-MM-DD" format.
            end (str): End date in "YYYY-MM-DD" format.

        Returns:
            pd.DataFrame: DataFrame filtered between the two dates, containing ETF prices and stock weights.
        """
        # Process the ETF data to create a combined DataFrame with prices and weights
        df = self.process_etf_data(ticker)

        # Filter the DataFrame to include only the data between the specified start and end dates
        filtered_df = self.filter_df_by_date(df, start=start, end=end)

        # Return the filtered DataFrame
        return filtered_df

    def download(self, ticker: str, start: str = None, end: str = None) -> pd.DataFrame:
        """
        Retrieves and optionally filters ETF data between two given dates for a specific ticker.

        Parameters:
            ticker (str): The ticker for which the data is retrieved.
            start (str, optional): Start date in "YYYY-MM-DD" format. If not provided, no start filter is applied.
            end (str, optional): End date in "YYYY-MM-DD" format. If not provided, no end filter is applied.

        Returns:
            pd.DataFrame: DataFrame filtered between the two dates, or all data if no dates are specified.
        """
        # Process the ETF data to create a combined DataFrame with prices and weights
        df = self.process_etf_data(ticker)

        # Apply filtering logic based on the presence of start and end
        if start and end:
            return self.filter_df_by_date(df, start=start, end=end)
        elif start:
            start_date = pd.to_datetime(start)
            return df.loc[start_date:]
        elif end:
            end_date = pd.to_datetime(end)
            return df.loc[:end_date]
        else:
            return df

    def history(self, tickers: List[str], start: str = None, end: str = None) -> pd.DataFrame:
        """
        Retrieves and concatenates the `Close Price` data for a list of tickers, renaming the column to the ticker name.

        Parameters:
            tickers (List[str]): A list of tickers to retrieve and concatenate.
            start (str, optional): Start date in "YYYY-MM-DD" format. If not provided, no start filter is applied.
            end (str, optional): End date in "YYYY-MM-DD" format. If not provided, no end filter is applied.

        Returns:
            pd.DataFrame: DataFrame with concatenated `Close Price` columns for the specified tickers.

        Raises:
            ValueError: If a ticker in the list is not part of the class's tickers.
        """
        # Ensure all tickers are valid
        invalid_tickers = [ticker for ticker in tickers if ticker not in self.tickers]
        if invalid_tickers:
            raise ValueError(f"The following tickers are invalid: {', '.join(invalid_tickers)}")

        # Initialize an empty DataFrame for concatenation
        concatenated_df = pd.DataFrame()

        for ticker in tickers:
            # Retrieve the ETF data for the ticker
            df = self.download(ticker, start=start, end=end)

            # Extract the `Close Price` column and rename it to the ticker
            df = df[['Close Price']].rename(columns={'Close Price': ticker})

            # Concatenate the DataFrame
            concatenated_df = pd.concat([concatenated_df, df], axis=1)

        return concatenated_df

    def plot_etf_prices(self, etf_prices, etf_name, color='blue', start=None, end=None):
        """
        Plots a graph of ETF prices with optional filtering by start and end dates.

        Parameters:
            etf_prices (dict): Dictionary containing dates as keys and ETF prices as values.
            etf_name (str): Name of the ETF to be displayed in the plot.
            color (str): Color of the plot line. Default is 'blue'.
            start (str, optional): Start date in "YYYY-MM-DD" format. Default is None.
            end (str, optional): End date in "YYYY-MM-DD" format. Default is None.
        """
        # Convert dates (keys) to datetime objects
        dates = [datetime.strptime(date, "%Y-%m-%d") for date in etf_prices.keys()]
        values = list(etf_prices.values())

        # Apply date filtering if start or end dates are provided
        if start:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            dates, values = zip(*[(date, value) for date, value in zip(dates, values) if date >= start_date])
        if end:
            end_date = datetime.strptime(end, "%Y-%m-%d")
            dates, values = zip(*[(date, value) for date, value in zip(dates, values) if date <= end_date])

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(dates, values, label=f"ETF {etf_name} Prices", color=color, marker='.')

        # Add titles and labels
        plt.title(f"Evolution of {etf_name} prices")
        plt.xlabel("Date")
        plt.ylabel(f"{etf_name} Prices")
        plt.xticks(rotation=45)  # Rotate dates to avoid overlap
        plt.grid(True)
        plt.tight_layout()

        # Display the plot
        plt.legend()
        plt.show()

    def plotter(self, ticker, color, start=None, end=None):
        """
        Plots the ETF prices for a given ticker with optional filtering by start and end dates.

        Parameters:
            ticker (str): The ticker symbol of the ETF.
            color (str): The color of the plot line.
            start (str, optional): Start date in "YYYY-MM-DD" format. Default is None.
            end (str, optional): End date in "YYYY-MM-DD" format. Default is None.
        """
        # Construct the file path for the JSON file containing the ETF prices
        filePath = f"./data/{ticker}/SP500{ticker}ETFPrices.json"
        
        # Load the ETF prices from the JSON file
        with open(filePath, 'r') as file:
            data = json.load(file)
        
        # Plot the ETF prices using the updated plot_etf_prices function
        self.plot_etf_prices(data, f"SP500{ticker}", color, start=start, end=end)



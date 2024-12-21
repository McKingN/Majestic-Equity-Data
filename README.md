## Majestic-Equity-Data

Welcome to the **MagesticEquityData** project! This project provides tools to process and analyze ETF (Exchange-Traded Fund) data, including prices and stock weights. It is organized into a clean structure to make it easy to understand and maintain.

#### Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

### Description
The **MagesticEquityData** class helps you retrieve and analyze ETF data based on criteria such as date ranges and specific ETFs. It allows you to filter data by dates, plot graphs of ETF prices, and generate a DataFrame containing ETF data.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/McKingN/Majestic-Equity-Data.git
   ```
2. Navigate to the project directory:
   ```bash
   cd MagesticEquityData
   ```
3. Create a virtual environment (recommended) and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # on Windows use env\Scripts\activate
   ```
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
The primary class `MagesticEquityData` can be used to process ETF data. Here's an example of how you can use it:

```python
from utils import MagesticEquityData

# Create an instance of the MagesticEquityData class
equity_data = MagesticEquityData()

# Retrieve ETF data for a specific ticker and date range
df = equity_data.retrieve_etf_data(ticker='Dividend', start='2020-01-01', end='2020-12-31')

# Display the DataFrame
print(df)
```

- `ticker`: The specific ETF (e.g., 'Dividend', 'Value', etc.).
- `start` and `end`: Filter dates to retrieve data between these dates.

### Directory Structure
```
.
├── data
│   ├── Dividend
│   │   ├── SP500DividendETFPrices.json
│   │   └── SP500DividendETFWeights.json
│   ├── LowVol
│   │   ├── SP500LowVolETFPrices.json
│   │   └── SP500LowVolETFWeights.json
│   ├── MarketCap
│   │   ├── SP500MarketCapETFPrices.json
│   │   └── SP500MarketCapETFWeights.json
│   ├── Momentum
│   │   ├── SP500MomentumETFPrices.json
│   │   └── SP500MomentumETFWeights.json
│   ├── Quality
│   │   ├── SP500QualityETFPrices.json
│   │   └── SP500QualityETFWeights.json
│   └── Value
│       ├── SP500ValueETFPrices.json
│       └── SP500ValueETFWeights.json
├── main.py
├── requirements.txt
├── utils.py
└── README.md
```

- `data`: Contains ETF data organized by strategy type (Dividend, LowVol, etc.) with `Prices.json` and `Weights.json` for each.
- `main.py`: Entry point script where you can execute the data analysis and processing.
- `requirements.txt`: Lists the necessary Python packages.
- `utils.py`: Python utilities and methods that process ETF data.
- `README.md`: This file provides documentation for the project.

### Contributing
Contributions are always welcome! Please fork the project, create a new branch, make your changes, and submit a pull request. Ensure your changes do not break existing functionality, and add relevant tests if necessary.

### License
This project is licensed under the terms of the **GNU GENERAL PUBLIC LICENSE**. See the `LICENSE` file for more details.


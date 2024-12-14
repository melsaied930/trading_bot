# Trading Bot Project Documentation

## **Project Overview**
This project is a fully functional trading bot built using Python. It integrates with the **Interactive Brokers API (IBKR)** using the `ib_insync` library for real-time trading, order execution, and market data retrieval.

### **Key Features:**
- **Automated Market Data Fetching:** Retrieves live market data using the IBKR API.
- **Trading Strategies:** Includes a moving average strategy for automated trading.
- **Order Execution:** Places market orders using the broker API.
- **Risk Management:** Supports stop-loss, take-profit, and position sizing.
- **Logging & Monitoring:** Logs events, orders, and market data.

---

# **Project Structure**
```
trading_bot/
│
├── README.md               # Project description
├── config/                 # Configuration settings
│   ├── __init__.py
│   └── config.py
│
├── data/                   # Market data fetching logic
│   ├── __init__.py
│   └── data_fetcher.py
│
├── strategies/             # Trading strategy implementations
│   ├── __init__.py
│   ├── base_strategy.py
│   ├── backtest_strategy.py
│   └── moving_average.py
│
├── models/                 # Portfolio management logic
│   ├── __init__.py
│   └── portfolio.py
│
├── risk/                   # Risk management
│   └── risk_manager.py
│
├── brokers/                # API wrapper for brokers/exchanges
│   ├── __init__.py
│   ├── broker_api.py
│   └── verify_api_access.py
│
├── utils/                  # Logging and indicators
│   ├── __init__.py
│   ├── indicators.py
│   └── logger.py
│
├── main.py                 # Main entry point
├── requirements.txt        # Dependencies
└── .env                    # Secret environment variables
```

---

# **Module Breakdown**

### **1. Configuration Management (`config/`)**
Manages API keys, broker URLs, and trading pairs.

### **2. Market Data Fetching (`data/`)**
Connects to IBKR API and fetches live market data.

### **3. Trading Strategies (`strategies/`)**
Implements strategies such as moving average crossover.

### **4. Portfolio Management (`models/`)**
Handles portfolio balances, holdings, and trade updates.

### **5. Order Placement (`brokers/`)**
Manages order placement using the broker API.

### **6. Risk Management (`risk/`)**
Manages stop-loss, take-profit, and position sizing strategies.

### **7. Logging and Indicators (`utils/`)**
Logs events and calculates trading indicators.

---

# **Package Management**

### **1. Managing Dependencies**
- All required packages are listed in `requirements.txt`.
- Use the following command to install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### **2. Adding a New Package**
- Install the desired package:
  ```bash
  pip install <package-name>
  ```
- Freeze the current environment and update `requirements.txt`:
  ```bash
  pip freeze > requirements.txt
  ```

### **3. Virtual Environment Management**
- Create a new virtual environment:
  ```bash
  python3 -m venv .venv
  ```
- Activate the virtual environment:
  ```bash
  source .venv/bin/activate  # On macOS/Linux
  .\.venv\Scripts\activate  # On Windows
  ```

### **4. Updating Packages**
- Upgrade a specific package:
  ```bash
  pip install --upgrade <package-name>
  ```
- Upgrade all packages:
  ```bash
  pip list --outdated | awk '{print $1}' | xargs -n1 pip install -U
  ```

---

# **How to Run the Project**

1. **Create a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   ```

2. **Activate the Virtual Environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Bot:**
   ```bash
   python main.py
   ```

---

This documentation outlines the project's overall architecture, main modules, package management, and setup instructions, focusing on high-level design without code details.


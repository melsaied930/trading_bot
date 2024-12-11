from ib_insync import IB

# Connect to IBKR TWS
ib = IB()
ib.connect("127.0.0.1", 7497, clientId=1)

# Check account summary
account_summary = ib.accountSummary()
print(account_summary)

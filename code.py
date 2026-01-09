

import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# 1. Load Dataset
# -----------------------------
file_name = "SuperMarket Analysis.csv"

if not os.path.exists(file_name):
    print("❌ CSV file not found. Please upload the file first.")
    raise SystemExit

df = pd.read_csv(file_name)

print("="*60)
print("Dataset Preview:")
print(df.head())

print("\nDataset Columns:")
print(df.columns)

print("\nDataset Info:")
print(df.info())

# -----------------------------
# 2. Fix column names (IMPORTANT)
# -----------------------------
# Detect total sales column automatically
possible_total_cols = ['Total', 'total', 'Sales', 'sales', 'Total Sales']

total_col = None
for col in possible_total_cols:
    if col in df.columns:
        total_col = col
        break

if total_col is None:
    raise KeyError("❌ No Total/Sales column found in dataset")

print(f"\n✅ Using '{total_col}' as total sales column")

# -----------------------------
# 3. Data Cleaning
# -----------------------------
df['Date'] = pd.to_datetime(df['Date'])
df['Time'] = df['Time'].astype(str)  # remove warning

print("\nMissing Values:")
print(df.isnull().sum())

# -----------------------------
# 4. Basic Analysis
# -----------------------------
print("\nBranch Statistics:")
branch_stats = df.groupby('Branch')[total_col].agg(['mean','median','min','max'])
print(branch_stats)

# -----------------------------
# 5. Visualizations
# -----------------------------
plt.figure()
plt.hist(df[total_col], bins=30)
plt.title("Distribution of Total Sales")
plt.xlabel("Total Sales")
plt.ylabel("Frequency")
plt.show()

plt.figure()
df['Customer type'].value_counts().plot(kind='bar')
plt.title("Customer Type Frequency")
plt.ylabel("Count")
plt.show()

daily_sales = df.groupby('Date')[total_col].sum()
plt.figure()
daily_sales.plot()
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.show()

plt.figure()
plt.scatter(df['Unit price'], df['Quantity'])
plt.title("Unit Price vs Quantity")
plt.xlabel("Unit price")
plt.ylabel("Quantity")
plt.show()

plt.figure(figsize=(10,5))
df.boxplot(column='gross income', by='Product line', rot=45)
plt.title("Gross Income by Product Line")
plt.suptitle("")
plt.show()

# -----------------------------
# 6. Correlation Matrix
# -----------------------------
corr_cols = ['Unit price','Quantity', total_col,'gross income','Rating']
corr = df[corr_cols].corr()

plt.figure()
plt.imshow(corr)
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns, rotation=45)
plt.yticks(range(len(corr)), corr.columns)
plt.title("Correlation Matrix")
plt.show()

# -----------------------------
# 7. Advanced Analysis (FINAL ANSWERS)
# -----------------------------
print("\nAdvanced Analysis Answers:")
print("="*40)

top_branch = df.groupby('Branch')[total_col].sum().idxmax()
print(f"Q1: Highest revenue branch: {top_branch}")

member_avg = df[df['Customer type']=='Member'][total_col].mean()
normal_avg = df[df['Customer type']=='Normal'][total_col].mean()
print(f"Q2: Members spend more? {'Yes' if member_avg > normal_avg else 'No'}")

top_payment = df['Payment'].value_counts().idxmax()
print(f"Q3: Most used payment method: {top_payment}")

top_product = df.groupby('Product line')['Rating'].mean().idxmax()
print(f"Q4: Highest rated product line: {top_product}")

corr_price_qty = df['Unit price'].corr(df['Quantity'])
print(f"Q5: Correlation between unit price and quantity: {corr_price_qty:.3f}")

print("\n✅ Analysis Completed Successfully (No Errors)")

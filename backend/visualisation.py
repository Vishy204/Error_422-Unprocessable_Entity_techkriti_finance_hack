import spacy
import yahooquery as yq
import pandas as pd
from fuzzywuzzy import process
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Mapping of company names to NSE tickers (extend as needed)
company_ticker_map = {
    "Reliance Industries": "RELIANCE.NS",
    "Reliance Industries Limited": "RELIANCE.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Tata Consultancy Services (TCS)": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Wipro": "WIPRO.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "ITC": "ITC.NS",
    "L&T": "LT.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Adani Ports and Special Economic Zone": "ADANIPORTS.NS",
    "Axis Bank": "AXISBANK.NS",
    "Indian Oil Corporation": "IOC.NS",
    "Life Insurance Corporation of India (LIC)": "LICI.NS",
    "Oil and Natural Gas Corporation (ONGC)": "ONGC.NS",
    "State Bank of India (SBI)": "SBIN.NS",
    "Tata Steel": "TATASTEEL.NS"
}
ner_model = pipeline("ner", model="dslim/bert-base-NER")  # Named Entity Recognition

# Function to extract company name from text
def extract_comp_name(text="Reliance is very good"):
    ner_results = ner_model(text[:500])
    company_names = [result['word'] for result in ner_results if result['entity'].startswith("B-ORG")]
    
    if not company_names:
        print("No company name detected!")
        return "Reliance Industries"  # Default to Reliance Industries
    
    # Use fuzzy matching to map extracted name to the closest known company
    best_match, score = process.extractOne(company_names[0], company_ticker_map.keys())
    
    if score > 80:  # Only consider matches with high confidence
        return best_match
    else:
        print("No accurate match found!")
        return "Reliance Industries"  # Default to Reliance Industries

# Function to fetch financial data
def fetch_financial_data(ticker="RELIANCE.NS"):
    stock = yq.Ticker(ticker)
    
    # Fetch financial statements (quarterly)
    balance_sheet = stock.balance_sheet(frequency="q")
    income_statement = stock.income_statement(frequency="q")
    cash_flow = stock.cash_flow(frequency="q")

    # Convert to CSV
    balance_sheet.to_csv("balance_sheet.csv")
    income_statement.to_csv("income_statement.csv")
    cash_flow.to_csv("cash_flow.csv")

def process_balance_sheet(file_path="balance_sheet.csv", output_file="cleaned_balance_sheet.csv"):
    # Load the dataset
    df = pd.read_csv(file_path)  

    # Keep only the most important financial metrics
    important_columns = [
        "symbol", "asOfDate", "currencyCode", "CurrentAssets", "CurrentLiabilities", 
        "WorkingCapital", "CashAndCashEquivalents", "AccountsReceivable", 
        "TotalDebt", "NetDebt", "LongTermDebt", "TotalAssets", "NetPPE", 
        "Inventory", "RetainedEarnings", "StockholdersEquity", "TotalCapitalization", 
        "TangibleBookValue"
    ]
    
    df = df[important_columns]

    # Feature Engineering
    df["DebtToEquity"] = df["TotalDebt"] / df["StockholdersEquity"]  
    df["CurrentRatio"] = df["CurrentAssets"] / df["CurrentLiabilities"]  
    df["WorkingCapitalRatio"] = df["WorkingCapital"] / df["TotalAssets"]  
    df["InventoryTurnover"] = df["TotalAssets"] / df["Inventory"]  
    df["DebtToAssets"] = df["TotalDebt"] / df["TotalAssets"]  
    df["NetDebtRatio"] = df["NetDebt"] / df["TotalCapitalization"]  

    # Handling NaN values
    df.fillna(method='ffill', inplace=True)  # Forward fill missing values (best for financial time series)
    df.fillna(method='bfill', inplace=True)  # Backward fill for remaining NaNs

    # Additional strategy for critical ratios
    finance_columns = ["DebtToEquity", "CurrentRatio", "WorkingCapitalRatio", "InventoryTurnover", "DebtToAssets", "NetDebtRatio"]
    df[finance_columns] = df[finance_columns].fillna(df[finance_columns].median())  # Fill remaining NaNs with median

    # Save cleaned dataset
    df.to_csv(output_file, index=False)

def process_income_statement(file_path="income_statement.csv", output_file="cleaned_income_statement.csv"):
    # Load the dataset
    df = pd.read_csv(file_path)  

    # Select essential financial metrics
    important_columns = [
        "asOfDate", "currencyCode", "TotalRevenue", "GrossProfit", "OperatingIncome",
        "EBITDA", "NetIncome", "BasicEPS", "DilutedEPS", "OperatingExpense", "InterestExpense",
        "TaxProvision", "TotalExpenses", "PretaxIncome", "EBIT"
    ]
    
    df = df[important_columns]

    # Feature Engineering - Financial Ratios
    df["NetProfitMargin"] = df["NetIncome"] / df["TotalRevenue"]  # Profitability
    df["OperatingMargin"] = df["OperatingIncome"] / df["TotalRevenue"]  # Efficiency
    df["EBITDAMargin"] = df["EBITDA"] / df["TotalRevenue"]  # Financial health
    df["InterestCoverage"] = df["EBIT"] / df["InterestExpense"]  # Debt risk
    df["TaxRate"] = df["TaxProvision"] / df["PretaxIncome"]  # Effective tax rate

    # Identify numeric columns (excluding non-numeric ones)
    numeric_cols = df.select_dtypes(include=['number']).columns

    # Handle NaN values *only for numeric columns*
    df[numeric_cols] = df[numeric_cols].fillna(method='ffill')  # Forward fill for missing values
    df[numeric_cols] = df[numeric_cols].fillna(method='bfill')  # Backward fill for remaining gaps
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())  # Median fill for last remaining NaNs

    # Save the cleaned dataset
    df.to_csv(output_file, index=False)
    
    print(f"Income statement data cleaned & saved as '{output_file}'!")



def plot_financial_data(file1_path, file2_path):
    # Load the CSV files
    df_income = pd.read_csv(file1_path)
    df_financial = pd.read_csv(file2_path)

    # Convert 'asOfDate' to datetime for proper plotting
    df_income["asOfDate"] = pd.to_datetime(df_income["asOfDate"])
    df_financial["asOfDate"] = pd.to_datetime(df_financial["asOfDate"])

    # Apply Seaborn theme for stylish plots
    sns.set_theme(style="darkgrid")

    # Set figure size
    fig, axes = plt.subplots(7, 1, figsize=(14, 35))

    # Color Palette
    palette = sns.color_palette("coolwarm", 4)

    # --- 1. Revenue & Profitability (Line Plot) ---
    axes[0].plot(df_income["asOfDate"], df_income["TotalRevenue"], label="Total Revenue", marker="o", linestyle="-", color=palette[0])
    axes[0].plot(df_income["asOfDate"], df_income["GrossProfit"], label="Gross Profit", marker="s", linestyle="--", color=palette[1])
    axes[0].plot(df_income["asOfDate"], df_income["OperatingIncome"], label="Operating Income", marker="^", linestyle="-.", color=palette[2])
    axes[0].plot(df_income["asOfDate"], df_income["NetIncome"], label="Net Income", marker="d", linestyle=":", color=palette[3])
    axes[0].set_title("Revenue & Profitability", fontsize=14, fontweight="bold")
    axes[0].legend()
    axes[0].grid(alpha=0.4)

    # --- 2. Profit Margins (Area Plot) ---
    axes[1].fill_between(df_income["asOfDate"], df_income["NetProfitMargin"], alpha=0.5, label="Net Profit Margin", color=palette[0])
    axes[1].fill_between(df_income["asOfDate"], df_income["OperatingMargin"], alpha=0.5, label="Operating Margin", color=palette[1])
    axes[1].fill_between(df_income["asOfDate"], df_income["EBITDAMargin"], alpha=0.5, label="EBITDA Margin", color=palette[2])
    axes[1].set_title("Profit Margins Over Time", fontsize=14, fontweight="bold")
    axes[1].legend()
    axes[1].grid(alpha=0.4)

    # --- 3. Debt & Cash Position (Line Plot with Markers) ---
    axes[2].plot(df_financial["asOfDate"], df_financial["TotalDebt"], label="Total Debt", marker="o", linestyle="-", color=palette[0])
    axes[2].plot(df_financial["asOfDate"], df_financial["NetDebt"], label="Net Debt", marker="s", linestyle="--", color=palette[1])
    axes[2].plot(df_financial["asOfDate"], df_financial["CashAndCashEquivalents"], label="Cash & Equivalents", marker="^", linestyle="-.", color=palette[2])
    axes[2].set_title("Debt & Cash Position", fontsize=14, fontweight="bold")
    axes[2].legend()
    axes[2].grid(alpha=0.4)

    # --- 4. Debt-to-Equity & Current Ratio (Scatter Plot) ---
    axes[3].scatter(df_financial["asOfDate"], df_financial["DebtToEquity"], label="Debt-to-Equity", color=palette[0], s=100)
    axes[3].scatter(df_financial["asOfDate"], df_financial["CurrentRatio"], label="Current Ratio", color=palette[1], s=100)
    axes[3].set_title("Liquidity & Solvency Ratios (Scatter Plot)", fontsize=14, fontweight="bold")
    axes[3].legend()
    axes[3].grid(alpha=0.4)

    # --- 5. Working Capital & Inventory Turnover (Step Plot) ---
    axes[4].step(df_financial["asOfDate"], df_financial["WorkingCapital"], label="Working Capital", color=palette[0], linewidth=2, where="mid")
    axes[4].step(df_financial["asOfDate"], df_financial["InventoryTurnover"], label="Inventory Turnover", color=palette[1], linewidth=2, where="mid")
    axes[4].set_title("Working Capital & Inventory Turnover (Step Plot)", fontsize=14, fontweight="bold")
    axes[4].legend()
    axes[4].grid(alpha=0.4)

    # --- 6. Retained Earnings & Stockholders Equity (Horizontal Bar Chart) ---
    axes[5].barh(df_financial["asOfDate"].astype(str), df_financial["RetainedEarnings"], label="Retained Earnings", color=palette[0], alpha=0.6)
    axes[5].barh(df_financial["asOfDate"].astype(str), df_financial["StockholdersEquity"], label="Stockholders Equity", color=palette[1], alpha=0.6)
    axes[5].set_title("Retained Earnings & Stockholders Equity (Horizontal Bar)", fontsize=14, fontweight="bold")
    axes[5].legend()
    axes[5].grid(alpha=0.4)

    # --- 7. Total Assets & Tangible Book Value (Pie Chart) ---
    latest_index = -1  # Take the latest data point
    data_labels = ["Total Assets", "Tangible Book Value"]
    data_values = [df_financial["TotalAssets"].iloc[latest_index], df_financial["TangibleBookValue"].iloc[latest_index]]
    axes[6].pie(data_values, labels=data_labels, autopct="%1.1f%%", colors=[palette[0], palette[1]], startangle=140)
    axes[6].set_title("Total Assets & Tangible Book Value (Pie Chart)", fontsize=14, fontweight="bold")

     # Rotate x-axis labels for better readability
    for ax in axes[:-1]:  # Exclude pie chart
        ax.set_xlabel("Date", fontsize=12)
        ax.tick_params(axis='x', rotation=45)

    # Adjust layout
    plt.tight_layout()

    # Save the figure in memory
    img_io = io.BytesIO()
    fig.savefig(img_io, format="png", bbox_inches="tight")
    img_io.seek(0)

    # Convert to base64
    visualization = base64.b64encode(img_io.getvalue()).decode("utf-8")

    plt.close(fig)  # Close the figure to free memory

    return visualization
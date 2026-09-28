"""Core analytics for the Nassau Candy product profitability project."""
from __future__ import annotations
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "Row ID","Order ID","Order Date","Ship Date","Ship Mode","Customer ID",
    "Country/Region","City","State/Province","Postal Code","Division","Region",
    "Product ID","Product Name","Sales","Units","Gross Profit","Cost"
]

FACTORY_MAP = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory",
}

def load_data(path: str = "data/Nassau_Candy_Distributor.csv") -> pd.DataFrame:
    """Load and validate the source dataset."""
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df

def add_profit_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Add date, margin, unit-profit and factory fields."""
    out = df.copy()
    out["Order Date"] = pd.to_datetime(out["Order Date"], dayfirst=True, errors="coerce")
    out["Ship Date"] = pd.to_datetime(out["Ship Date"], dayfirst=True, errors="coerce")
    if (out["Sales"] <= 0).any():
        raise ValueError("Sales contains non-positive values.")
    if (out["Units"] <= 0).any():
        raise ValueError("Units contains non-positive values.")
    out["Gross_Margin_Pct"] = out["Gross Profit"] / out["Sales"] * 100
    out["Profit_per_Unit"] = out["Gross Profit"] / out["Units"]
    out["Factory"] = out["Product Name"].map(FACTORY_MAP).fillna("Not mapped")
    return out

def product_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate profitability at product level."""
    out = (
        df.groupby(["Product ID","Product Name","Factory"], as_index=False)
        .agg(
            Division=("Division","first"),
            Sales=("Sales","sum"),
            Units=("Units","sum"),
            Gross_Profit=("Gross Profit","sum"),
            Cost=("Cost","sum"),
            Orders=("Order ID","nunique"),
        )
    )
    out["Gross_Margin_Pct"] = out["Gross_Profit"]/out["Sales"]*100
    out["Profit_per_Unit"] = out["Gross_Profit"]/out["Units"]
    total_sales = out["Sales"].sum()
    total_profit = out["Gross_Profit"].sum()
    out["Revenue_Contribution_Pct"] = out["Sales"]/total_sales*100
    out["Profit_Contribution_Pct"] = out["Gross_Profit"]/total_profit*100
    sales_median = out["Sales"].median()
    margin_median = out["Gross_Margin_Pct"].median()
    out["Portfolio_Class"] = np.select(
        [
            (out["Sales"] >= sales_median) & (out["Gross_Margin_Pct"] >= margin_median),
            (out["Sales"] >= sales_median) & (out["Gross_Margin_Pct"] < margin_median),
            (out["Sales"] < sales_median) & (out["Gross_Margin_Pct"] >= margin_median),
        ],
        ["High Sales / High Margin","High Sales / Low Margin","Low Sales / High Margin"],
        default="Low Sales / Low Margin",
    )
    return out

def division_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate profitability at division level."""
    out = (
        df.groupby("Division", as_index=False)
        .agg(
            Sales=("Sales","sum"),
            Gross_Profit=("Gross Profit","sum"),
            Cost=("Cost","sum"),
            Units=("Units","sum"),
            Orders=("Order ID","nunique"),
        )
    )
    out["Gross_Margin_Pct"] = out["Gross_Profit"]/out["Sales"]*100
    out["Profit_per_Unit"] = out["Gross_Profit"]/out["Units"]
    return out

def pareto_tables(product: pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame]:
    """Return revenue and profit Pareto tables."""
    rev = product.sort_values("Sales", ascending=False).reset_index(drop=True)
    prof = product.sort_values("Gross_Profit", ascending=False).reset_index(drop=True)
    rev["Cum_Revenue_Pct"] = rev["Revenue_Contribution_Pct"].cumsum()
    prof["Cum_Profit_Pct"] = prof["Profit_Contribution_Pct"].cumsum()
    return rev, prof

def margin_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """Return monthly gross-margin standard deviation by product."""
    temp = df.copy()
    temp["YearMonth"] = temp["Order Date"].dt.to_period("M").astype(str)
    monthly = (
        temp.groupby(["Product ID","Product Name","YearMonth"], as_index=False)
        .agg(Sales=("Sales","sum"), Gross_Profit=("Gross Profit","sum"))
    )
    monthly["Margin_Pct"] = monthly["Gross_Profit"]/monthly["Sales"]*100
    return (
        monthly.groupby(["Product ID","Product Name"], as_index=False)["Margin_Pct"]
        .std(ddof=0)
        .rename(columns={"Margin_Pct":"Margin_Volatility_Ppt"})
    )

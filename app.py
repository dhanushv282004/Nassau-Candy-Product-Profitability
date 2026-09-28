import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from analysis import load_data, add_profit_metrics, product_summary, division_summary, pareto_tables, margin_volatility

st.set_page_config(page_title="Nassau Candy Profitability Analytics", page_icon="🍬", layout="wide")

st.title("🍬 Product Line Profitability & Margin Performance")
st.caption("Nassau Candy Distributor — product, division, cost and profit analytics")

@st.cache_data
def get_data():
    return add_profit_metrics(load_data())

df = get_data()

with st.sidebar:
    st.header("Filters")
    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()
    dates = st.date_input("Date range", (min_date, max_date), min_value=min_date, max_value=max_date)
    divisions = st.multiselect(
        "Division",
        sorted(df["Division"].unique()),
        default=sorted(df["Division"].unique()),
    )
    margin_threshold = st.slider(
        "Margin risk threshold (%)",
        min_value=0.0, max_value=100.0, value=50.0, step=1.0
    )
    product_search = st.text_input("Product search", "")

f = df[df["Division"].isin(divisions)].copy()
if isinstance(dates, tuple) and len(dates) == 2:
    f = f[(f["Order Date"].dt.date >= dates[0]) & (f["Order Date"].dt.date <= dates[1])]
if product_search:
    f = f[f["Product Name"].str.contains(product_search, case=False, na=False)]
if f.empty:
    st.warning("No records match the selected filters. Broaden the filters.")
    st.stop()

p = product_summary(f)
d = division_summary(f)
pareto_rev, pareto_profit = pareto_tables(p)
vol = margin_volatility(f)

total_sales = p["Sales"].sum()
total_profit = p["Gross_Profit"].sum()
overall_margin = total_profit / total_sales * 100
top5_profit_share = pareto_profit.head(5)["Profit_Contribution_Pct"].sum()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Sales", f"{total_sales:,.2f}")
c2.metric("Gross profit", f"{total_profit:,.2f}")
c3.metric("Gross margin", f"{overall_margin:.2f}%")
c4.metric("Top 5 profit contribution", f"{top5_profit_share:.2f}%")

st.subheader("1. Product Profitability Overview")
col1,col2 = st.columns(2)
with col1:
    top = p.sort_values("Gross_Profit", ascending=False).head(10)
    fig = px.bar(top.sort_values("Gross_Profit"), x="Gross_Profit", y="Product Name",
                 orientation="h", title="Top Products by Gross Profit")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.dataframe(
        p.sort_values("Gross_Profit", ascending=False)[
            ["Product Name","Division","Sales","Gross_Profit","Gross_Margin_Pct","Profit_per_Unit",
             "Revenue_Contribution_Pct","Profit_Contribution_Pct","Portfolio_Class"]
        ].round(3),
        use_container_width=True, height=430
    )

st.subheader("2. Division Performance Dashboard")
col1,col2 = st.columns(2)
with col1:
    melt = d.melt(id_vars=["Division"], value_vars=["Sales","Gross_Profit"],
                  var_name="Metric", value_name="Value")
    fig = px.bar(melt, x="Division", y="Value", color="Metric", barmode="group",
                 title="Revenue vs Gross Profit by Division")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.box(f, x="Division", y="Gross_Margin_Pct", title="Margin Distribution by Division")
    st.plotly_chart(fig, use_container_width=True)
st.dataframe(d.round(3), use_container_width=True)

st.subheader("3. Cost vs Margin Diagnostics")
risk = p[p["Gross_Margin_Pct"] < margin_threshold].copy()
col1,col2 = st.columns(2)
with col1:
    fig = px.scatter(
        p, x="Cost", y="Sales", size="Gross_Profit", hover_name="Product Name",
        hover_data=["Gross_Margin_Pct","Profit_per_Unit","Division"],
        title="Product Cost vs Sales"
    )
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.metric("Products below selected margin threshold", len(risk))
    if len(risk):
        st.dataframe(
            risk[["Product Name","Sales","Gross_Profit","Gross_Margin_Pct","Profit_per_Unit"]]
            .sort_values("Gross_Margin_Pct").round(3),
            use_container_width=True, height=350
        )
    else:
        st.success("No products are below the selected threshold.")

st.subheader("4. Profit Concentration Analysis")
col1,col2 = st.columns(2)
with col1:
    show = pareto_profit.copy()
    show["Product Rank"] = np.arange(1, len(show)+1)
    fig = px.bar(show, x="Product Rank", y="Profit_Contribution_Pct",
                 hover_name="Product Name", title="Product Profit Contribution")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    n80p = int((pareto_profit["Cum_Profit_Pct"] < 80).sum() + 1)
    n80r = int((pareto_rev["Cum_Revenue_Pct"] < 80).sum() + 1)
    st.metric("Products needed for 80% of profit", f"{n80p} / {len(p)}")
    st.metric("Products needed for 80% of revenue", f"{n80r} / {len(p)}")
    st.metric("Top 5 profit share", f"{pareto_profit.head(5)['Profit_Contribution_Pct'].sum():.2f}%")
    st.metric("Top 5 revenue share", f"{pareto_rev.head(5)['Revenue_Contribution_Pct'].sum():.2f}%")

st.dataframe(
    pareto_profit[["Product Name","Gross_Profit","Profit_Contribution_Pct","Cum_Profit_Pct"]]
    .round(3),
    use_container_width=True
)

st.subheader("5. Margin Volatility")
vol2 = p[["Product ID","Product Name"]].merge(vol, on=["Product ID","Product Name"], how="left").fillna(0)
st.dataframe(vol2.sort_values("Margin_Volatility_Ppt", ascending=False).round(4), use_container_width=True)
st.info("Margin volatility is the standard deviation of monthly product gross margin. Zero means the observed product margin did not vary across the available months.")

st.subheader("6. Factory & Product Mapping Reference")
st.dataframe(
    p[["Product Name","Factory","Division","Sales","Gross_Profit","Gross_Margin_Pct"]]
    .sort_values(["Factory","Product Name"]).round(3),
    use_container_width=True
)

st.download_button(
    "Download filtered profitability data",
    p.to_csv(index=False).encode("utf-8"),
    "filtered_product_profitability.csv",
    "text/csv",
)

# Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor

## Objective
Analyze product and division profitability using gross margin, profit per unit, revenue/profit contribution, margin risk, cost structure and Pareto concentration.

## Dataset
`data/Nassau_Candy_Distributor.csv`
- Rows: 10,194
- Original columns: 18
- Unique products: 15
- Order date range: 2024-01-02 to 2025-12-31
- Missing cells: 0
- Duplicate rows: 0

## Metrics
- Gross Margin (%) = Gross Profit / Sales × 100
- Profit per Unit = Gross Profit / Units
- Revenue Contribution = Product Sales / Total Sales × 100
- Profit Contribution = Product Profit / Total Profit × 100
- Margin Volatility = standard deviation of monthly product gross margin

## Reproducible margin-risk rule
The project asks for high-sales/low-margin diagnostics but does not specify a numeric cutoff. This implementation uses:
- High Sales: product sales >= median product sales
- Low Margin: product gross margin < median product gross margin
The Streamlit dashboard additionally provides a user-controlled margin threshold slider.

## Key actual findings
- Total sales: 141,783.63
- Total gross profit: 93,442.80
- Overall gross margin: 65.91%
- Top 5 products contribute 92.88% of revenue.
- Top 5 products by profit contribute 95.06% of profit.
- 5 of 15 products reach 80% of revenue.
- 5 of 15 products reach 80% of profit.
- 3 products meet the median-based high-sales/low-margin rule.
- Mean product margin volatility is 0.0000 percentage points.

## Streamlit
Run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

Dashboard modules:
1. Product Profitability Overview
2. Division Performance Dashboard
3. Cost vs Margin Diagnostics
4. Profit Concentration Analysis
5. Margin Volatility
6. Factory & Product Mapping Reference

Filters:
- Date range
- Division
- Margin threshold
- Product search

## Note on the supplied project page
The page includes a conclusion mentioning shipping-route efficiency, while the project title, problem statement, dataset fields and KPIs focus on product profitability and margin performance. This implementation follows the profitability-focused scope because it is supported by the dataset and methodology.

# Research Report
## Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor

### Abstract
This study evaluates product and division profitability using a 2025 Nassau Candy Distributor dataset containing 10,194 order rows and 18 original fields. The analysis calculates gross margin, profit per unit, revenue contribution, profit contribution and margin volatility, and uses product-level and division-level diagnostics to identify margin-risk patterns and profit concentration.

The dataset contains 15 unique products. Total sales are 141,783.63, total gross profit is 93,442.80, and the overall gross margin is 65.91%. The five highest-revenue products account for 92.88% of revenue, while the five highest-profit products account for 95.06% of profit. Under the documented median-based rule, 3 products are high-sales/low-margin candidates. Product-level monthly gross margin volatility is zero in the observed data.

### 1. Background
Profitability analysis helps organizations distinguish revenue-generating products from products that generate strong financial returns. Gross margin and profit contribution provide different perspectives: a product may have a high margin percentage but contribute little total profit if its sales volume is small.

### 2. Problem Statement
The study addresses:
- Which product lines deliver the highest gross margin and profit?
- Whether high-sales products are actually profitable
- How profitability varies across product divisions
- Which products represent potential margin risk

### 3. Dataset and Data Quality
The dataset includes 18 original fields covering order identifiers, dates, shipping information, customer/location fields, division and region, product identity, sales, units, gross profit and cost.

Validation found 0 missing cells and 0 duplicate rows. All sales and units were positive. Gross Profit matched Sales minus Cost for the supplied rows.

### 4. Methodology
#### 4.1 Profitability calculations
- Gross Margin (%) = Gross Profit / Sales × 100
- Profit per Unit = Gross Profit / Units
- Revenue Contribution = Product Sales / Total Sales × 100
- Profit Contribution = Product Profit / Total Profit × 100
- Margin Volatility = standard deviation of monthly product gross margin

#### 4.2 Product classification
The project does not supply a numerical high-sales or low-margin threshold. For reproducibility:
- High Sales = product sales at or above the median product sales (597.50)
- Low Margin = product gross margin below the median product margin (62.31%)

#### 4.3 Division analysis
Sales, cost, units, gross profit, gross margin and profit per unit were aggregated by division.

#### 4.4 Pareto analysis
Products were ranked by revenue and gross profit. Cumulative contribution was used to identify the number of products required to reach 80% of revenue and 80% of profit.

#### 4.5 Cost diagnostics
Product-level cost was compared with sales. High-sales/low-margin products were treated as exploratory risk signals rather than automatic recommendations for discontinuation.

### 5. Results

#### 5.1 Overall profitability
| Metric | Result |
|---|---:|
| Rows/orders | 10,194 |
| Unique products | 15 |
| Total sales | 141,783.63 |
| Total gross profit | 93,442.80 |
| Overall gross margin | 65.91% |

#### 5.2 Product leaderboard
| Product | Sales | Gross Profit | Gross Margin | Profit / Unit |
|---|---:|---:|---:|---:|
| Wonka Bar -Scrumdiddlyumptious | 27,874.80 | 19,357.50 | 69.44% | 2.50 |
| Wonka Bar - Triple Dazzle Caramel | 28,485.00 | 18,610.20 | 65.33% | 2.45 |
| Wonka Bar - Milk Chocolate | 26,867.75 | 17,443.37 | 64.92% | 2.11 |
| Wonka Bar - Nutty Crunch Surprise | 23,574.95 | 16,819.95 | 71.35% | 2.49 |
| Wonka Bar - Fudge Mallows | 24,890.40 | 16,593.60 | 66.67% | 2.40 |
| Lickable Wallpaper | 7,860.00 | 3,930.00 | 50.00% | 10.00 |
| Wonka Gum | 597.50 | 310.70 | 52.00% | 0.65 |
| Everlasting Gobstopper | 130.00 | 104.00 | 80.00% | 8.00 |
| Kazookles | 1,205.75 | 92.75 | 7.69% | 0.25 |
| Hair Toffee | 76.50 | 59.50 | 77.78% | 3.50 |

The five leading products by total gross profit are all in the Chocolate division. The largest total profit contribution is from Wonka Bar -Scrumdiddlyumptious (19,357.50).

#### 5.3 Division performance
| Division | Sales | Gross Profit | Gross Margin | Profit / Unit | Revenue Contribution | Profit Contribution |
|---|---:|---:|---:|---:|---:|---:|
| Chocolate | 131,692.90 | 88,824.62 | 67.45% | 2.38 | 92.88% | 95.06% |
| Other | 9,663.25 | 4,333.45 | 44.84% | 3.49 | 6.82% | 4.64% |
| Sugar | 427.48 | 284.73 | 66.61% | 2.08 | 0.30% | 0.30% |

Chocolate accounts for 92.88% of revenue and 95.06% of gross profit in the supplied data.

#### 5.4 High-sales / low-margin diagnostics
| Product | Sales | Gross Profit | Gross Margin | Profit / Unit |
|---|---:|---:|---:|---:|
| Lickable Wallpaper | 7,860.00 | 3,930.00 | 50.00% | 10.00 |
| Kazookles | 1,205.75 | 92.75 | 7.69% | 0.25 |
| Wonka Gum | 597.50 | 310.70 | 52.00% | 0.65 |

These 3 products are margin-review candidates under the documented rules; the classification is not a recommendation to discontinue them.

#### 5.5 Profit concentration
The top five revenue products contribute **92.88% of revenue**, while the top five profit products contribute **95.06% of profit**.

Only **5 of 15 products** are needed to reach 80% of revenue and **5 of 15 products** are needed to reach 80% of profit.

#### 5.6 Margin volatility
The standard deviation of monthly gross margin is **0 percentage points for all observed products**. The product-level unit economics therefore appear stable across the available months, leaving little variation for this KPI to distinguish products.

#### 5.7 Cost structure
The product-level Pearson correlation between cost and sales is approximately **0.991**. This indicates a strong positive linear relationship in the aggregated product data, but correlation does not establish a causal relationship.

### 6. Discussion
The profitability profile is highly concentrated in Chocolate products. This division generates nearly all recorded sales and profit, while the Other division has a lower gross margin.

The high-sales/low-margin diagnostic identifies Lickable Wallpaper, Kazookles and Wonka Gum as products requiring margin review under the project's median-based rule. Kazookles has the lowest observed gross margin among these candidates at 7.69%.

At the same time, some products have higher margins but contribute little revenue or total profit. Therefore, margin percentage and absolute profit contribution should be interpreted together.

The strong Pareto concentration means a small set of products drives most of the financial output. This can increase portfolio dependency on those products.

### 7. Recommendations
1. Monitor high-sales/low-margin products as a dedicated margin-review group.
2. Review pricing, discounting and cost structure before changing product strategy.
3. Track the major Chocolate products separately because of their large contribution to total revenue and profit.
4. Use gross margin percentage together with gross profit and profit per unit.
5. Investigate supplier costs and pricing for low-margin products.
6. Maintain monthly price/cost history in future data collection to make margin volatility more informative.
7. Validate any pricing or cost intervention with additional demand and operational data.

### 8. Limitations
- The dataset covers a single calendar year.
- The project brief does not prescribe a numerical high-sales/low-margin threshold, so median-based rules were documented for reproducibility.
- Revenue and cost units are not explicitly identified as a currency in the provided file, so the report uses dataset units.
- Margin volatility is zero in the observed product-level data.
- Factory/product mapping comes from the project instructions and is not a field directly observed in the CSV.
- The analysis is descriptive and does not establish causality.

### 9. Conclusion
The analysis provides a structured view of product profitability for Nassau Candy Distributor. Total sales were **141,783.63**, total gross profit was **93,442.80**, and overall gross margin was **65.91%**.

Profitability is strongly concentrated: the top five products account for **95.06% of profit**, and the top five revenue products account for **92.88% of revenue**. The Chocolate division dominates the portfolio, while three high-sales/low-margin products form an exploratory margin-risk group under the documented rules.

These findings can support pricing, cost and portfolio review, but any operational decision should be validated with additional commercial and market context.

### Scope note
The supplied project page contains a conclusion mentioning shipping-route efficiency, while the project title, problem statement, dataset fields and KPIs are focused on product profitability and margin performance. This report therefore follows the profitability-focused scope.

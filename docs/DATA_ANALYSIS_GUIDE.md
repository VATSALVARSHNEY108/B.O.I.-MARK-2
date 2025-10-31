# 📊 Data Analysis Features Guide

## Complete Data Analysis Toolkit with 100+ Features

Your AI Desktop Automation Controller now includes a comprehensive data analysis suite with over 100 powerful features across 10 categories. Transform, analyze, visualize, and gain insights from your data using natural language commands!

---

## 🗂️ Feature Categories

1. **Data Import/Export** - Load and save data in multiple formats
2. **Data Cleaning** - Handle missing values, duplicates, and outliers
3. **Data Analysis** - Statistical summaries and correlations
4. **Data Visualization** - Charts, heatmaps, and dashboards
5. **Data Transformation** - Pivot tables, aggregations, and merging
6. **Machine Learning** - Regression, classification, and clustering
7. **Text Analytics** - Sentiment analysis and word frequency
8. **Time Series** - Trend analysis and forecasting
9. **Statistical Tests** - T-tests, ANOVA, and chi-square
10. **Data Quality** - Quality assessment and completeness checks

---

## 📥 1. Data Import/Export

### Import CSV
Load data from CSV files into the analysis system.

**Commands:**
```
✅ "Import CSV file sales_data.csv"
✅ "Load data from customers.csv"
✅ "Import sales_data.csv as sales"
```

**Features:**
- Automatically detects column types
- Shows data preview
- Stores data for further analysis

### Import JSON
Load data from JSON files.

**Commands:**
```
✅ "Import JSON file users.json"
✅ "Load data from api_response.json"
✅ "Import users.json as user_data"
```

### Import Excel
Load data from Excel spreadsheets.

**Commands:**
```
✅ "Import Excel file report.xlsx"
✅ "Load data from sales.xlsx sheet Sales"
✅ "Import report.xlsx from Sheet1"
```

### Export Data
Save your analyzed data in various formats.

**Commands:**
```
✅ "Export data to output.csv"
✅ "Save data as results.json"
✅ "Export sales data to final_report.csv"
```

### Convert Format
Convert data between CSV, JSON, and Excel formats.

**Commands:**
```
✅ "Convert data.csv to data.json"
✅ "Convert report.xlsx to report.csv"
✅ "Change format from JSON to Excel"
```

---

## 🧹 2. Data Cleaning

### Handle Missing Values
Deal with missing data using various strategies.

**Commands:**
```
✅ "Handle missing values by dropping rows"
✅ "Fill missing values with mean"
✅ "Replace missing values in age column with median"
✅ "Fill missing values with forward fill"
```

**Strategies:**
- `drop` - Remove rows with missing values
- `mean` - Fill with column average (numeric only)
- `median` - Fill with column median (numeric only)
- `mode` - Fill with most common value
- `forward` - Forward fill from previous values

### Remove Duplicates
Eliminate duplicate rows from your dataset.

**Commands:**
```
✅ "Remove duplicate rows"
✅ "Delete duplicates from data"
✅ "Remove duplicates based on email column"
```

### Validate Data
Check data quality and identify issues.

**Commands:**
```
✅ "Validate data quality"
✅ "Check data for issues"
✅ "Run data validation"
```

**What it checks:**
- Missing values
- Duplicate rows
- Low variance columns
- Data type consistency

### Convert Data Types
Change column data types for proper analysis.

**Commands:**
```
✅ "Convert age column to integer"
✅ "Change price to float"
✅ "Convert date column to datetime"
✅ "Make category column categorical"
```

**Supported types:**
- `int` - Integer numbers
- `float` - Decimal numbers
- `string` - Text data
- `datetime` - Date and time
- `category` - Categorical data

### Detect Outliers
Find unusual values in your data.

**Commands:**
```
✅ "Detect outliers in price column"
✅ "Find outliers in sales using IQR method"
✅ "Check for outliers in age column using Z-score"
```

**Methods:**
- `iqr` - Interquartile Range method (default)
- `zscore` - Z-score method (3 standard deviations)

---

## 📈 3. Data Analysis

### Statistical Summary
Get comprehensive statistics about your data.

**Commands:**
```
✅ "Show statistical summary"
✅ "Generate statistics for data"
✅ "Give me data summary"
```

**Includes:**
- Mean, median, standard deviation
- Min, max, quartiles
- Data types and unique values
- Missing value counts

### Correlation Analysis
Analyze relationships between numeric columns.

**Commands:**
```
✅ "Analyze correlations"
✅ "Show correlation matrix"
✅ "Find correlations using Spearman method"
```

**Methods:**
- `pearson` - Linear correlation (default)
- `spearman` - Rank correlation
- `kendall` - Kendall's tau

**Output:**
- Correlation matrix
- Strong correlations (>0.7)
- Correlation strength interpretation

### Data Profiling
Comprehensive data profile with quality metrics.

**Commands:**
```
✅ "Profile my data"
✅ "Generate data profile"
✅ "Show data profiling report"
```

**Includes:**
- Overview (rows, columns, memory usage)
- Column-by-column analysis
- Missing value percentages
- Completeness score

### Distribution Analysis
Analyze the distribution of specific columns.

**Commands:**
```
✅ "Analyze distribution of age column"
✅ "Show distribution for salary"
✅ "Check price distribution"
```

**For numeric columns:**
- Mean, median, mode
- Standard deviation
- Skewness and kurtosis
- Quantiles (25%, 50%, 75%)

**For categorical columns:**
- Unique value count
- Most common values
- Value frequency

### Trend Analysis
Analyze trends over time.

**Commands:**
```
✅ "Analyze trend in sales over time"
✅ "Show trend for date and revenue columns"
✅ "Analyze time series trend"
```

**Provides:**
- Overall trend direction
- Start vs end values
- Total change and percent change
- Average and volatility

---

## 📊 4. Data Visualization

### Create Charts
Generate various types of charts.

**Commands:**
```
✅ "Create bar chart for category and sales"
✅ "Make line chart of date vs revenue"
✅ "Generate scatter plot for age and income"
✅ "Create histogram of prices"
✅ "Make pie chart for categories"
```

**Chart types:**
- `bar` - Bar chart
- `line` - Line chart
- `scatter` - Scatter plot
- `histogram` - Histogram (distribution)
- `pie` - Pie chart

### Create Heatmap
Visualize correlations with a heatmap.

**Commands:**
```
✅ "Create correlation heatmap"
✅ "Generate heatmap"
✅ "Show heatmap of correlations"
```

**Features:**
- Color-coded correlation matrix
- Annotated values
- Easy to spot strong correlations

### Create Dashboard
Generate comprehensive dashboard with multiple visualizations.

**Commands:**
```
✅ "Create data dashboard"
✅ "Generate dashboard"
✅ "Make visual dashboard"
```

**Includes:**
- Distribution plot
- Scatter plot
- Box plot comparison
- Correlation matrix

---

## 🔄 5. Data Transformation

### Create Pivot Table
Summarize data with pivot tables.

**Commands:**
```
✅ "Create pivot table with region as index, product as columns, and sales as values"
✅ "Make pivot table for category by month showing average revenue"
✅ "Generate pivot table"
```

**Aggregation functions:**
- `mean` - Average (default)
- `sum` - Total
- `count` - Count
- `min` - Minimum
- `max` - Maximum

### Aggregate Data
Group and aggregate data.

**Commands:**
```
✅ "Aggregate data by category"
✅ "Group by region and calculate sum of sales"
✅ "Aggregate sales by product"
```

### Calculate Column
Create new calculated columns.

**Commands:**
```
✅ "Calculate total as price * quantity"
✅ "Create profit column as revenue - cost"
✅ "Add margin column as profit / revenue"
```

**Uses pandas expression syntax:**
- Basic math: `+`, `-`, `*`, `/`
- Example: `"price * quantity + tax"`

### Merge Datasets
Combine two datasets.

**Commands:**
```
✅ "Merge customers and orders on customer_id"
✅ "Join sales and products datasets on product_id"
✅ "Left join data1 and data2 on id"
```

**Join types:**
- `inner` - Only matching rows (default)
- `left` - All from left, matching from right
- `right` - All from right, matching from left
- `outer` - All rows from both

### Split Column
Split text columns into multiple columns.

**Commands:**
```
✅ "Split full_name by space into first_name and last_name"
✅ "Divide address column by comma"
✅ "Split column by delimiter"
```

---

## 🤖 6. Machine Learning

### Linear Regression
Predict numeric values using linear regression.

**Commands:**
```
✅ "Run linear regression on price using age and mileage"
✅ "Predict salary from experience and education"
✅ "Linear regression with target sales"
```

**Provides:**
- R² score (model accuracy)
- Mean squared error (MSE)
- Coefficients for each feature
- Feature importance ranking

### Advanced Regression
Use regularized regression models.

**Commands:**
```
✅ "Run Ridge regression on price using features"
✅ "Use Lasso regression for feature selection"
✅ "Apply ElasticNet regression"
```

**Models:**
- `ridge` - Ridge regression (L2 regularization)
- `lasso` - Lasso regression (L1 regularization)
- `elasticnet` - Elastic Net (L1 + L2)

### Classification
Predict categories using classification models.

**Commands:**
```
✅ "Classify customer type using age and income"
✅ "Run random forest classification"
✅ "Predict category using decision tree"
```

**Models:**
- `logistic` - Logistic regression
- `random_forest` - Random Forest
- `decision_tree` - Decision Tree

**Output:**
- Accuracy score
- Test size
- Predicted classes

### Ensemble Methods
Use powerful ensemble learning.

**Commands:**
```
✅ "Run ensemble classification on target"
✅ "Use ensemble methods for regression"
✅ "Compare Random Forest and Gradient Boosting"
```

**Compares:**
- Random Forest
- Gradient Boosting
- Recommends best model

### Clustering
Group similar data points.

**Commands:**
```
✅ "Cluster customers into 3 groups using age and income"
✅ "Run K-means clustering on features"
✅ "Use DBSCAN clustering"
```

**Methods:**
- `kmeans` - K-Means clustering (default)
- `dbscan` - Density-based clustering
- `hierarchical` - Hierarchical clustering

**Provides:**
- Cluster assignments
- Silhouette score (quality)
- Cluster sizes

### Feature Selection
Select most important features.

**Commands:**
```
✅ "Select top 5 features for predicting price"
✅ "Find best features for classification"
✅ "Feature selection for target column"
```

**Output:**
- Selected features
- Feature scores
- Ranked feature importance

### Cross Validation
Validate model performance.

**Commands:**
```
✅ "Run 5-fold cross validation"
✅ "Validate model with cross validation"
✅ "Cross validate prediction model"
```

**Provides:**
- Individual fold scores
- Mean score
- Standard deviation
- Scoring metric used

---

## 📝 7. Text Analytics

### Text Mining
Extract insights from text.

**Commands:**
```
✅ "Analyze this text: [your text]"
✅ "Mine text for insights"
✅ "Extract information from text"
```

**Provides:**
- Total word count
- Unique words
- Most common words (top 10)
- Vocabulary richness score

### Sentiment Analysis
Analyze emotional tone of text.

**Commands:**
```
✅ "Analyze sentiment of this review: [text]"
✅ "Check sentiment: [text]"
✅ "Is this text positive or negative: [text]"
```

**Output:**
- Sentiment (positive/negative/neutral)
- Sentiment score
- Positive/negative word counts

### Word Frequency
Analyze word frequency in text columns.

**Commands:**
```
✅ "Analyze word frequency in reviews column"
✅ "Show top 20 words in comments"
✅ "Get word frequency for text data"
```

**Provides:**
- Total words
- Unique words
- Top N most common words

---

## ⏰ 8. Time Series Analysis

### Trend Decomposition
Break down time series into components.

**Commands:**
```
✅ "Decompose time series for sales over time"
✅ "Break down trend for monthly revenue"
✅ "Decompose date and value columns"
```

**Components:**
- Trend
- Seasonality
- Residual

### Seasonality Analysis
Identify seasonal patterns.

**Commands:**
```
✅ "Analyze seasonality in sales data"
✅ "Find seasonal patterns by month"
✅ "Check for seasonal trends"
```

**Analyzes:**
- Monthly patterns
- Day of week patterns
- Quarterly trends
- Strongest/weakest periods

### Time Series Forecast
Predict future values.

**Commands:**
```
✅ "Forecast next 10 periods for sales"
✅ "Predict future revenue for 12 months"
✅ "Generate forecast for time series"
```

**Provides:**
- Forecast values
- Forecast trend direction
- Last actual value for comparison

### Moving Averages
Calculate moving averages.

**Commands:**
```
✅ "Calculate 7-day moving average for sales"
✅ "Compute moving average with window 30"
✅ "Add moving average to price column"
```

**Calculates:**
- Simple Moving Average (MA)
- Exponential Moving Average (EMA)

---

## 🔬 9. Statistical Tests

### T-Test
Compare means of two groups.

**Commands:**
```
✅ "Run t-test between group1 and group2 columns"
✅ "Compare means using t-test"
✅ "Test significance of age differences"
```

**Provides:**
- T-statistic
- P-value
- Significance (p < 0.05)
- Mean values for both groups

### Chi-Square Test
Test independence of categorical variables.

**Commands:**
```
✅ "Run chi-square test on gender and preference"
✅ "Test independence of category and outcome"
✅ "Chi-square for two categorical columns"
```

**Provides:**
- Chi-square statistic
- P-value
- Degrees of freedom
- Independence interpretation

### ANOVA Test
Compare means across multiple groups.

**Commands:**
```
✅ "Run ANOVA on region and sales"
✅ "Test group differences using ANOVA"
✅ "ANOVA for category and value"
```

**Provides:**
- F-statistic
- P-value
- Number of groups tested
- Significance interpretation

### Normality Test
Test if data follows normal distribution.

**Commands:**
```
✅ "Test normality of age column"
✅ "Check if sales are normally distributed"
✅ "Run Shapiro-Wilk test"
```

**Provides:**
- Test statistic
- P-value
- Normality conclusion
- Sample size used

---

## ✅ 10. Data Quality

### Quality Assessment
Comprehensive data quality evaluation.

**Commands:**
```
✅ "Assess data quality"
✅ "Check overall data quality"
✅ "Generate quality report"
```

**Metrics:**
- Quality score (0-100%)
- Completeness percentage
- Missing cells count
- Duplicate rows count
- Quality grade (Excellent/Good/Fair/Poor)
- List of issues found

### Completeness Check
Check data completeness by column.

**Commands:**
```
✅ "Check data completeness"
✅ "Show completeness by column"
✅ "Assess data coverage"
```

**Provides:**
- Overall completeness %
- Completeness by column
- List of incomplete columns

---

## 💡 Usage Tips

### Data Workflow Best Practices

1. **Import Data**
   ```
   "Import CSV file sales_2024.csv"
   ```

2. **Clean Data**
   ```
   "Validate data quality"
   "Handle missing values with mean"
   "Remove duplicate rows"
   ```

3. **Explore Data**
   ```
   "Show statistical summary"
   "Create correlation heatmap"
   "Profile my data"
   ```

4. **Visualize**
   ```
   "Create dashboard"
   "Make bar chart for sales by region"
   ```

5. **Analyze**
   ```
   "Run linear regression on sales"
   "Cluster customers into 4 groups"
   "Forecast next 12 months"
   ```

6. **Export Results**
   ```
   "Export data to analyzed_results.csv"
   ```

### Common Use Cases

**Business Analytics:**
```
✅ "Import sales_data.csv"
✅ "Show statistical summary"
✅ "Analyze trend in revenue over time"
✅ "Create pivot table by region and product"
✅ "Forecast next quarter sales"
```

**Customer Segmentation:**
```
✅ "Import customers.csv"
✅ "Cluster customers into 5 groups using age and spending"
✅ "Create dashboard"
✅ "Export results to segments.csv"
```

**Quality Control:**
```
✅ "Import product_data.csv"
✅ "Detect outliers in defect_rate column"
✅ "Run ANOVA on factory and quality"
✅ "Create control charts"
```

**Predictive Modeling:**
```
✅ "Import training_data.csv"
✅ "Select top 10 features for target"
✅ "Run ensemble classification"
✅ "Validate with cross validation"
```

---

## 📁 Data Storage

All imported datasets are stored in the `data_analysis_files/` directory:
- Datasets are saved as CSV files
- Charts and visualizations are saved as PNG images
- Multiple datasets can be loaded simultaneously with different names

**Managing Multiple Datasets:**
```
✅ "Import sales.csv as sales_data"
✅ "Import customers.csv as customer_data"
✅ "Merge sales_data and customer_data on customer_id"
```

---

## 🎯 Quick Reference

### Most Used Commands

**Data Loading:**
- `"Import CSV file [filename]"`
- `"Import Excel file [filename]"`

**Data Cleaning:**
- `"Handle missing values"`
- `"Remove duplicates"`
- `"Detect outliers in [column]"`

**Analysis:**
- `"Show statistical summary"`
- `"Analyze correlations"`
- `"Profile data"`

**Visualization:**
- `"Create dashboard"`
- `"Create bar chart for [x] and [y]"`
- `"Create heatmap"`

**Machine Learning:**
- `"Run linear regression on [target] using [features]"`
- `"Cluster into [n] groups"`
- `"Forecast next [n] periods"`

---

## 🚀 Advanced Features

### Chaining Operations
You can perform multiple operations in sequence:

```
1. "Import sales_data.csv"
2. "Handle missing values with mean"
3. "Remove duplicates"
4. "Create correlation heatmap"
5. "Run clustering with 3 groups"
6. "Export to final_analysis.csv"
```

### Custom Analysis Pipelines
Combine different analysis types:

```
1. Import and clean data
2. Exploratory analysis (profiling, correlations)
3. Visualization (charts, dashboard)
4. Predictive modeling (regression, classification)
5. Time series forecasting
6. Export results
```

---

## 📞 Need Help?

If you encounter issues:
1. Check that your data file exists and path is correct
2. Ensure column names match exactly
3. For ML features, ensure you have numeric data
4. For time series, ensure datetime format is recognized

**Common Issues:**
- **"Dataset not found"**: Import the data first
- **"Column not found"**: Check column name spelling
- **"No numeric columns"**: Convert data types or check your data
- **"Not enough data points"**: Some operations require minimum data

---

## ✨ Summary

You now have access to a professional-grade data analysis toolkit with:
- ✅ 100+ data analysis features
- ✅ 10 comprehensive categories
- ✅ Natural language interface
- ✅ Automatic visualization
- ✅ Machine learning capabilities
- ✅ Statistical testing
- ✅ Quality assessment
- ✅ Time series forecasting
- ✅ Text analytics
- ✅ Export in multiple formats

**Transform your data into insights with simple commands!** 📊✨

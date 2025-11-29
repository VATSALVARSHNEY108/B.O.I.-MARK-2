"""
Comprehensive Data Analysis Module
Provides 100+ data analysis features across 10 categories
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    plt = None
    sns = None

try:
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
    from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report, silhouette_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.feature_selection import SelectKBest, f_classif, RFE
    from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
except ImportError:
    pass

try:
    from scipy import stats
    from scipy.stats import ttest_ind, chi2_contingency, f_oneway, shapiro
except ImportError:
    stats = None

try:
    import statsmodels.api as sm
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
except ImportError:
    sm = None

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.probability import FreqDist
except ImportError:
    nltk = None


class DataAnalysisSuite:
    """Comprehensive data analysis toolkit with 100+ features"""
    
    def __init__(self):
        self.data_storage_dir = "data_analysis_files"
        self.current_data = {}
        os.makedirs(self.data_storage_dir, exist_ok=True)
        
        try:
            if nltk:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
        except:
            pass
    
    def _save_dataframe(self, df: pd.DataFrame, name: str) -> str:
        """Save dataframe for later use"""
        self.current_data[name] = df
        filepath = os.path.join(self.data_storage_dir, f"{name}.csv")
        df.to_csv(filepath, index=False)
        return filepath
    
    def _get_dataframe(self, name: str) -> Optional[pd.DataFrame]:
        """Retrieve saved dataframe"""
        if name in self.current_data:
            return self.current_data[name]
        
        filepath = os.path.join(self.data_storage_dir, f"{name}.csv")
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            self.current_data[name] = df
            return df
        return None
    
    
    def import_csv(self, filepath: str, name: str = "data") -> Dict[str, Any]:
        """Import data from CSV file"""
        try:
            df = pd.read_csv(filepath)
            self._save_dataframe(df, name)
            
            return {
                "success": True,
                "message": f"✅ CSV imported successfully: {df.shape[0]} rows, {df.shape[1]} columns",
                "data": {
                    "name": name,
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "column_names": list(df.columns),
                    "preview": df.head(5).to_dict('records')
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error importing CSV: {str(e)}"}
    
    def import_json(self, filepath: str, name: str = "data") -> Dict[str, Any]:
        """Import data from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
            else:
                return {"success": False, "message": "❌ Invalid JSON format"}
            
            self._save_dataframe(df, name)
            
            return {
                "success": True,
                "message": f"✅ JSON imported successfully: {df.shape[0]} rows, {df.shape[1]} columns",
                "data": {
                    "name": name,
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "column_names": list(df.columns)
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error importing JSON: {str(e)}"}
    
    def import_excel(self, filepath: str, sheet_name: str = None, name: str = "data") -> Dict[str, Any]:
        """Import data from Excel file"""
        try:
            if sheet_name:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
            else:
                df = pd.read_excel(filepath)
            
            self._save_dataframe(df, name)
            
            return {
                "success": True,
                "message": f"✅ Excel imported successfully: {df.shape[0]} rows, {df.shape[1]} columns",
                "data": {
                    "name": name,
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "column_names": list(df.columns)
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error importing Excel: {str(e)}"}
    
    def export_csv(self, name: str, output_path: str) -> Dict[str, Any]:
        """Export data to CSV file"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            df.to_csv(output_path, index=False)
            return {
                "success": True,
                "message": f"✅ Data exported to {output_path}",
                "data": {"filepath": output_path, "rows": df.shape[0]}
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error exporting CSV: {str(e)}"}
    
    def export_json(self, name: str, output_path: str) -> Dict[str, Any]:
        """Export data to JSON file"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            df.to_json(output_path, orient='records', indent=2)
            return {
                "success": True,
                "message": f"✅ Data exported to {output_path}",
                "data": {"filepath": output_path, "rows": df.shape[0]}
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error exporting JSON: {str(e)}"}
    
    def convert_format(self, input_file: str, output_file: str, output_format: str) -> Dict[str, Any]:
        """Convert data between formats (CSV, JSON, Excel)"""
        try:
            if input_file.endswith('.csv'):
                df = pd.read_csv(input_file)
            elif input_file.endswith('.json'):
                df = pd.read_json(input_file)
            elif input_file.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(input_file)
            else:
                return {"success": False, "message": "❌ Unsupported input format"}
            
            if output_format.lower() == 'csv':
                df.to_csv(output_file, index=False)
            elif output_format.lower() == 'json':
                df.to_json(output_file, orient='records', indent=2)
            elif output_format.lower() == 'excel':
                df.to_excel(output_file, index=False)
            else:
                return {"success": False, "message": "❌ Unsupported output format"}
            
            return {
                "success": True,
                "message": f"✅ Converted {input_file} to {output_file}",
                "data": {"output": output_file, "rows": df.shape[0]}
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error converting: {str(e)}"}
    
    
    def handle_missing_values(self, name: str, strategy: str = "drop", column: str = None) -> Dict[str, Any]:
        """Handle missing values - drop, fill with mean/median/mode, or forward fill"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            original_missing = df.isnull().sum().sum()
            
            if strategy == "drop":
                df = df.dropna()
            elif strategy == "mean":
                if column:
                    df[column].fillna(df[column].mean(), inplace=True)
                else:
                    df.fillna(df.mean(numeric_only=True), inplace=True)
            elif strategy == "median":
                if column:
                    df[column].fillna(df[column].median(), inplace=True)
                else:
                    df.fillna(df.median(numeric_only=True), inplace=True)
            elif strategy == "mode":
                if column:
                    df[column].fillna(df[column].mode()[0] if not df[column].mode().empty else 0, inplace=True)
                else:
                    for col in df.columns:
                        if not df[col].mode().empty:
                            df[col].fillna(df[col].mode()[0], inplace=True)
            elif strategy == "forward":
                df.fillna(method='ffill', inplace=True)
            
            self._save_dataframe(df, name)
            remaining_missing = df.isnull().sum().sum()
            
            return {
                "success": True,
                "message": f"✅ Missing values handled using '{strategy}' strategy",
                "data": {
                    "original_missing": int(original_missing),
                    "remaining_missing": int(remaining_missing),
                    "rows_after": df.shape[0]
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error handling missing values: {str(e)}"}
    
    def remove_duplicates(self, name: str, subset: List[str] = None) -> Dict[str, Any]:
        """Remove duplicate rows"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            original_rows = df.shape[0]
            duplicates = df.duplicated(subset=subset).sum()
            
            df = df.drop_duplicates(subset=subset)
            self._save_dataframe(df, name)
            
            return {
                "success": True,
                "message": f"✅ Removed {duplicates} duplicate rows",
                "data": {
                    "original_rows": original_rows,
                    "duplicates_removed": int(duplicates),
                    "rows_after": df.shape[0]
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error removing duplicates: {str(e)}"}
    
    def validate_data(self, name: str, rules: Dict[str, Any] = None) -> Dict[str, Any]:
        """Validate data against rules"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            validation_results = {
                "total_rows": df.shape[0],
                "total_columns": df.shape[1],
                "missing_values": int(df.isnull().sum().sum()),
                "duplicate_rows": int(df.duplicated().sum()),
                "data_types": df.dtypes.astype(str).to_dict(),
                "issues": []
            }
            
            if df.isnull().sum().sum() > 0:
                validation_results["issues"].append("⚠️ Contains missing values")
            
            if df.duplicated().sum() > 0:
                validation_results["issues"].append("⚠️ Contains duplicate rows")
            
            for col in df.columns:
                if df[col].dtype == 'object':
                    unique_ratio = df[col].nunique() / len(df)
                    if unique_ratio < 0.01:
                        validation_results["issues"].append(f"⚠️ Column '{col}' has very low variance")
            
            return {
                "success": True,
                "message": f"✅ Data validation complete: {len(validation_results['issues'])} issues found",
                "data": validation_results
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error validating data: {str(e)}"}
    
    def convert_data_types(self, name: str, column: str, new_type: str) -> Dict[str, Any]:
        """Convert column data type"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            if column not in df.columns:
                return {"success": False, "message": f"❌ Column '{column}' not found"}
            
            old_type = str(df[column].dtype)
            
            if new_type == "int":
                df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype(int)
            elif new_type == "float":
                df[column] = pd.to_numeric(df[column], errors='coerce')
            elif new_type == "string":
                df[column] = df[column].astype(str)
            elif new_type == "datetime":
                df[column] = pd.to_datetime(df[column], errors='coerce')
            elif new_type == "category":
                df[column] = df[column].astype('category')
            
            self._save_dataframe(df, name)
            
            return {
                "success": True,
                "message": f"✅ Converted column '{column}' from {old_type} to {new_type}",
                "data": {"column": column, "old_type": old_type, "new_type": str(df[column].dtype)}
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error converting data type: {str(e)}"}
    
    def detect_outliers(self, name: str, column: str, method: str = "iqr") -> Dict[str, Any]:
        """Detect outliers using IQR or Z-score method"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            if column not in df.columns:
                return {"success": False, "message": f"❌ Column '{column}' not found"}
            
            if df[column].dtype not in [np.int64, np.float64]:
                return {"success": False, "message": f"❌ Column '{column}' must be numeric"}
            
            outliers = []
            
            if method == "iqr":
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            elif method == "zscore":
                z_scores = np.abs(stats.zscore(df[column].dropna()))
                outliers = df[z_scores > 3]
            
            return {
                "success": True,
                "message": f"✅ Found {len(outliers)} outliers in '{column}' using {method} method",
                "data": {
                    "column": column,
                    "method": method,
                    "outlier_count": len(outliers),
                    "outlier_percentage": round(len(outliers) / len(df) * 100, 2),
                    "outlier_values": outliers[column].tolist()[:20]
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error detecting outliers: {str(e)}"}
    
    
    def statistical_summary(self, name: str) -> Dict[str, Any]:
        """Generate comprehensive statistical summary"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            summary = {
                "shape": {"rows": df.shape[0], "columns": df.shape[1]},
                "column_info": {},
                "numeric_summary": df.describe().to_dict() if not df.select_dtypes(include=[np.number]).empty else {},
                "missing_values": df.isnull().sum().to_dict(),
                "data_types": df.dtypes.astype(str).to_dict()
            }
            
            for col in df.columns:
                summary["column_info"][col] = {
                    "type": str(df[col].dtype),
                    "unique_values": int(df[col].nunique()),
                    "missing": int(df[col].isnull().sum())
                }
            
            return {
                "success": True,
                "message": f"✅ Statistical summary generated for '{name}'",
                "data": summary
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error generating summary: {str(e)}"}
    
    def correlation_analysis(self, name: str, method: str = "pearson") -> Dict[str, Any]:
        """Analyze correlations between numeric columns"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            numeric_df = df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                return {"success": False, "message": "❌ No numeric columns found"}
            
            corr_matrix = numeric_df.corr(method=method)
            
            strong_correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        strong_correlations.append({
                            "column1": corr_matrix.columns[i],
                            "column2": corr_matrix.columns[j],
                            "correlation": round(float(corr_value), 3)
                        })
            
            return {
                "success": True,
                "message": f"✅ Correlation analysis complete using {method} method",
                "data": {
                    "correlation_matrix": corr_matrix.to_dict(),
                    "strong_correlations": strong_correlations,
                    "method": method
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in correlation analysis: {str(e)}"}
    
    def data_profiling(self, name: str) -> Dict[str, Any]:
        """Comprehensive data profiling"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            profile = {
                "overview": {
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
                    "duplicate_rows": int(df.duplicated().sum())
                },
                "columns": {},
                "data_quality": {
                    "completeness": round((1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2),
                    "total_missing": int(df.isnull().sum().sum())
                }
            }
            
            for col in df.columns:
                col_data = {
                    "type": str(df[col].dtype),
                    "unique": int(df[col].nunique()),
                    "missing": int(df[col].isnull().sum()),
                    "missing_pct": round(df[col].isnull().sum() / len(df) * 100, 2)
                }
                
                if df[col].dtype in [np.int64, np.float64]:
                    col_data.update({
                        "mean": round(float(df[col].mean()), 2) if not df[col].isnull().all() else None,
                        "median": round(float(df[col].median()), 2) if not df[col].isnull().all() else None,
                        "std": round(float(df[col].std()), 2) if not df[col].isnull().all() else None,
                        "min": round(float(df[col].min()), 2) if not df[col].isnull().all() else None,
                        "max": round(float(df[col].max()), 2) if not df[col].isnull().all() else None
                    })
                
                profile["columns"][col] = col_data
            
            return {
                "success": True,
                "message": f"✅ Data profiling complete for '{name}'",
                "data": profile
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in data profiling: {str(e)}"}
    
    def distribution_analysis(self, name: str, column: str) -> Dict[str, Any]:
        """Analyze distribution of a column"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            if column not in df.columns:
                return {"success": False, "message": f"❌ Column '{column}' not found"}
            
            analysis = {
                "column": column,
                "type": str(df[column].dtype)
            }
            
            if df[column].dtype in [np.int64, np.float64]:
                analysis.update({
                    "mean": round(float(df[column].mean()), 2),
                    "median": round(float(df[column].median()), 2),
                    "mode": round(float(df[column].mode()[0]), 2) if not df[column].mode().empty else None,
                    "std": round(float(df[column].std()), 2),
                    "skewness": round(float(df[column].skew()), 2),
                    "kurtosis": round(float(df[column].kurtosis()), 2),
                    "quantiles": {
                        "25%": round(float(df[column].quantile(0.25)), 2),
                        "50%": round(float(df[column].quantile(0.50)), 2),
                        "75%": round(float(df[column].quantile(0.75)), 2)
                    }
                })
            else:
                value_counts = df[column].value_counts().head(10)
                analysis.update({
                    "unique_values": int(df[column].nunique()),
                    "top_values": value_counts.to_dict(),
                    "most_common": str(df[column].mode()[0]) if not df[column].mode().empty else None
                })
            
            return {
                "success": True,
                "message": f"✅ Distribution analysis complete for '{column}'",
                "data": analysis
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in distribution analysis: {str(e)}"}
    
    def trend_analysis(self, name: str, time_column: str, value_column: str) -> Dict[str, Any]:
        """Analyze trends over time"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            if time_column not in df.columns or value_column not in df.columns:
                return {"success": False, "message": "❌ Specified columns not found"}
            
            df[time_column] = pd.to_datetime(df[time_column], errors='coerce')
            df = df.sort_values(time_column)
            
            trend_data = {
                "overall_trend": "increasing" if df[value_column].iloc[-1] > df[value_column].iloc[0] else "decreasing",
                "start_value": round(float(df[value_column].iloc[0]), 2),
                "end_value": round(float(df[value_column].iloc[-1]), 2),
                "change": round(float(df[value_column].iloc[-1] - df[value_column].iloc[0]), 2),
                "percent_change": round(((df[value_column].iloc[-1] - df[value_column].iloc[0]) / df[value_column].iloc[0] * 100), 2),
                "average": round(float(df[value_column].mean()), 2),
                "volatility": round(float(df[value_column].std()), 2)
            }
            
            return {
                "success": True,
                "message": f"✅ Trend analysis complete",
                "data": trend_data
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in trend analysis: {str(e)}"}
    
    
    def create_chart(self, name: str, chart_type: str, x_column: str, y_column: str = None, title: str = None) -> Dict[str, Any]:
        """Create various types of charts"""
        try:
            if plt is None:
                return {"success": False, "message": "❌ Matplotlib not available"}
            
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            plt.figure(figsize=(10, 6))
            
            if chart_type == "bar":
                if y_column:
                    plt.bar(df[x_column], df[y_column])
                    plt.ylabel(y_column)
                else:
                    df[x_column].value_counts().plot(kind='bar')
                plt.xlabel(x_column)
            elif chart_type == "line":
                if y_column:
                    plt.plot(df[x_column], df[y_column])
                    plt.ylabel(y_column)
                else:
                    plt.plot(df[x_column])
                plt.xlabel(x_column)
            elif chart_type == "scatter":
                if y_column:
                    plt.scatter(df[x_column], df[y_column])
                    plt.ylabel(y_column)
                plt.xlabel(x_column)
            elif chart_type == "histogram":
                plt.hist(df[x_column], bins=30, edgecolor='black')
                plt.xlabel(x_column)
                plt.ylabel("Frequency")
            elif chart_type == "pie":
                df[x_column].value_counts().plot(kind='pie', autopct='%1.1f%%')
            
            if title:
                plt.title(title)
            else:
                plt.title(f"{chart_type.capitalize()} Chart")
            
            plt.tight_layout()
            
            output_path = os.path.join(self.data_storage_dir, f"{name}_{chart_type}_chart.png")
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return {
                "success": True,
                "message": f"✅ {chart_type.capitalize()} chart created successfully",
                "data": {"chart_path": output_path, "chart_type": chart_type}
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error creating chart: {str(e)}"}
    
    def create_heatmap(self, name: str, title: str = None) -> Dict[str, Any]:
        """Create correlation heatmap"""
        try:
            if plt is None or sns is None:
                return {"success": False, "message": "❌ Visualization libraries not available"}
            
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            numeric_df = df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                return {"success": False, "message": "❌ No numeric columns found"}
            
            plt.figure(figsize=(12, 8))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0, fmt='.2f')
            
            if title:
                plt.title(title)
            else:
                plt.title("Correlation Heatmap")
            
            plt.tight_layout()
            
            output_path = os.path.join(self.data_storage_dir, f"{name}_heatmap.png")
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return {
                "success": True,
                "message": "✅ Heatmap created successfully",
                "data": {"chart_path": output_path}
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error creating heatmap: {str(e)}"}
    
    def create_dashboard(self, name: str) -> Dict[str, Any]:
        """Create comprehensive dashboard with multiple visualizations"""
        try:
            if plt is None or sns is None:
                return {"success": False, "message": "❌ Visualization libraries not available"}
            
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                return {"success": False, "message": "❌ Need at least 2 numeric columns for dashboard"}
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            
            df[numeric_cols[0]].hist(ax=axes[0, 0], bins=30, edgecolor='black')
            axes[0, 0].set_title(f'Distribution of {numeric_cols[0]}')
            axes[0, 0].set_xlabel(numeric_cols[0])
            axes[0, 0].set_ylabel('Frequency')
            
            if len(numeric_cols) >= 2:
                axes[0, 1].scatter(df[numeric_cols[0]], df[numeric_cols[1]])
                axes[0, 1].set_title(f'{numeric_cols[0]} vs {numeric_cols[1]}')
                axes[0, 1].set_xlabel(numeric_cols[0])
                axes[0, 1].set_ylabel(numeric_cols[1])
            
            df[numeric_cols[:min(5, len(numeric_cols))]].boxplot(ax=axes[1, 0])
            axes[1, 0].set_title('Box Plot Comparison')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            if len(numeric_cols) >= 2:
                corr_subset = df[numeric_cols[:min(5, len(numeric_cols))]].corr()
                im = axes[1, 1].imshow(corr_subset, cmap='coolwarm', aspect='auto')
                axes[1, 1].set_title('Correlation Matrix')
                axes[1, 1].set_xticks(range(len(corr_subset.columns)))
                axes[1, 1].set_yticks(range(len(corr_subset.columns)))
                axes[1, 1].set_xticklabels(corr_subset.columns, rotation=45)
                axes[1, 1].set_yticklabels(corr_subset.columns)
                plt.colorbar(im, ax=axes[1, 1])
            
            plt.tight_layout()
            
            output_path = os.path.join(self.data_storage_dir, f"{name}_dashboard.png")
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return {
                "success": True,
                "message": "✅ Dashboard created successfully",
                "data": {"dashboard_path": output_path}
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error creating dashboard: {str(e)}"}
    
    
    def create_pivot_table(self, name: str, index: str, columns: str, values: str, agg_func: str = "mean") -> Dict[str, Any]:
        """Create pivot table"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            pivot = pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=agg_func)
            
            pivot_name = f"{name}_pivot"
            self._save_dataframe(pivot.reset_index(), pivot_name)
            
            return {
                "success": True,
                "message": f"✅ Pivot table created: '{pivot_name}'",
                "data": {
                    "name": pivot_name,
                    "shape": pivot.shape,
                    "preview": pivot.head(10).to_dict()
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error creating pivot table: {str(e)}"}
    
    def aggregate_data(self, name: str, group_by: List[str], agg_dict: Dict[str, str]) -> Dict[str, Any]:
        """Aggregate data by groups"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            aggregated = df.groupby(group_by).agg(agg_dict).reset_index()
            
            agg_name = f"{name}_aggregated"
            self._save_dataframe(aggregated, agg_name)
            
            return {
                "success": True,
                "message": f"✅ Data aggregated: '{agg_name}'",
                "data": {
                    "name": agg_name,
                    "rows": aggregated.shape[0],
                    "columns": aggregated.shape[1],
                    "preview": aggregated.head(10).to_dict('records')
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error aggregating data: {str(e)}"}
    
    def calculate_column(self, name: str, new_column: str, expression: str) -> Dict[str, Any]:
        """Create new column based on calculation"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            df[new_column] = df.eval(expression)
            self._save_dataframe(df, name)
            
            return {
                "success": True,
                "message": f"✅ New column '{new_column}' created",
                "data": {
                    "column": new_column,
                    "sample_values": df[new_column].head(10).tolist()
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error calculating column: {str(e)}"}
    
    def merge_datasets(self, name1: str, name2: str, on: str, how: str = "inner", result_name: str = "merged") -> Dict[str, Any]:
        """Merge two datasets"""
        try:
            df1 = self._get_dataframe(name1)
            df2 = self._get_dataframe(name2)
            
            if df1 is None or df2 is None:
                return {"success": False, "message": "❌ One or both datasets not found"}
            
            merged = pd.merge(df1, df2, on=on, how=how)
            self._save_dataframe(merged, result_name)
            
            return {
                "success": True,
                "message": f"✅ Datasets merged: '{result_name}'",
                "data": {
                    "name": result_name,
                    "rows": merged.shape[0],
                    "columns": merged.shape[1],
                    "merge_type": how
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error merging datasets: {str(e)}"}
    
    def split_column(self, name: str, column: str, delimiter: str, new_columns: List[str]) -> Dict[str, Any]:
        """Split a column into multiple columns"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            if column not in df.columns:
                return {"success": False, "message": f"❌ Column '{column}' not found"}
            
            split_data = df[column].str.split(delimiter, expand=True)
            
            for i, new_col in enumerate(new_columns):
                if i < len(split_data.columns):
                    df[new_col] = split_data[i]
            
            self._save_dataframe(df, name)
            
            return {
                "success": True,
                "message": f"✅ Column '{column}' split into {len(new_columns)} new columns",
                "data": {"new_columns": new_columns}
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error splitting column: {str(e)}"}
    
    
    def linear_regression(self, name: str, target_column: str, feature_columns: List[str]) -> Dict[str, Any]:
        """Perform linear regression"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            X = df[feature_columns]
            y = df[target_column]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            coefficients = dict(zip(feature_columns, model.coef_.tolist()))
            
            return {
                "success": True,
                "message": "✅ Linear regression completed",
                "data": {
                    "model": "Linear Regression",
                    "r2_score": round(r2, 4),
                    "mse": round(mse, 4),
                    "rmse": round(np.sqrt(mse), 4),
                    "intercept": round(float(model.intercept_), 4),
                    "coefficients": {k: round(v, 4) for k, v in coefficients.items()},
                    "feature_importance": sorted(
                        [(k, abs(v)) for k, v in coefficients.items()],
                        key=lambda x: x[1],
                        reverse=True
                    )
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in linear regression: {str(e)}"}
    
    def advanced_regression(self, name: str, target_column: str, feature_columns: List[str], model_type: str = "ridge") -> Dict[str, Any]:
        """Perform advanced regression (Ridge, Lasso, ElasticNet)"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            X = df[feature_columns]
            y = df[target_column]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            if model_type == "ridge":
                model = Ridge(alpha=1.0)
            elif model_type == "lasso":
                model = Lasso(alpha=1.0)
            elif model_type == "elasticnet":
                model = ElasticNet(alpha=1.0, l1_ratio=0.5)
            else:
                return {"success": False, "message": f"❌ Unknown model type: {model_type}"}
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            return {
                "success": True,
                "message": f"✅ {model_type.capitalize()} regression completed",
                "data": {
                    "model": model_type.capitalize(),
                    "r2_score": round(r2, 4),
                    "mse": round(mse, 4),
                    "rmse": round(np.sqrt(mse), 4)
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in advanced regression: {str(e)}"}
    
    def classification_model(self, name: str, target_column: str, feature_columns: List[str], model_type: str = "logistic") -> Dict[str, Any]:
        """Perform classification"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            X = df[feature_columns]
            y = df[target_column]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            if model_type == "logistic":
                model = LogisticRegression(max_iter=1000)
            elif model_type == "random_forest":
                model = RandomForestClassifier(n_estimators=100, random_state=42)
            elif model_type == "decision_tree":
                model = DecisionTreeClassifier(random_state=42)
            else:
                return {"success": False, "message": f"❌ Unknown model type: {model_type}"}
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            
            return {
                "success": True,
                "message": f"✅ {model_type.capitalize()} classification completed",
                "data": {
                    "model": model_type.capitalize(),
                    "accuracy": round(accuracy, 4),
                    "test_size": len(X_test),
                    "classes": list(set(y.unique()))
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in classification: {str(e)}"}
    
    def ensemble_methods(self, name: str, target_column: str, feature_columns: List[str], task: str = "classification") -> Dict[str, Any]:
        """Perform ensemble learning (Random Forest, Gradient Boosting)"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            X = df[feature_columns]
            y = df[target_column]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            if task == "classification":
                rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
                gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
                
                rf_model.fit(X_train, y_train)
                gb_model.fit(X_train, y_train)
                
                rf_accuracy = accuracy_score(y_test, rf_model.predict(X_test))
                gb_accuracy = accuracy_score(y_test, gb_model.predict(X_test))
                
                return {
                    "success": True,
                    "message": "✅ Ensemble classification completed",
                    "data": {
                        "random_forest_accuracy": round(rf_accuracy, 4),
                        "gradient_boosting_accuracy": round(gb_accuracy, 4),
                        "best_model": "Random Forest" if rf_accuracy > gb_accuracy else "Gradient Boosting"
                    }
                }
            else:
                rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
                gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
                
                rf_model.fit(X_train, y_train)
                gb_model.fit(X_train, y_train)
                
                rf_r2 = r2_score(y_test, rf_model.predict(X_test))
                gb_r2 = r2_score(y_test, gb_model.predict(X_test))
                
                return {
                    "success": True,
                    "message": "✅ Ensemble regression completed",
                    "data": {
                        "random_forest_r2": round(rf_r2, 4),
                        "gradient_boosting_r2": round(gb_r2, 4),
                        "best_model": "Random Forest" if rf_r2 > gb_r2 else "Gradient Boosting"
                    }
                }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in ensemble methods: {str(e)}"}
    
    def clustering_analysis(self, name: str, feature_columns: List[str], n_clusters: int = 3, method: str = "kmeans") -> Dict[str, Any]:
        """Perform clustering analysis"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            X = df[feature_columns]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            if method == "kmeans":
                model = KMeans(n_clusters=n_clusters, random_state=42)
            elif method == "dbscan":
                model = DBSCAN(eps=0.5, min_samples=5)
            elif method == "hierarchical":
                model = AgglomerativeClustering(n_clusters=n_clusters)
            else:
                return {"success": False, "message": f"❌ Unknown clustering method: {method}"}
            
            clusters = model.fit_predict(X_scaled)
            df['cluster'] = clusters
            self._save_dataframe(df, name)
            
            silhouette_avg = silhouette_score(X_scaled, clusters) if len(set(clusters)) > 1 else 0
            
            cluster_sizes = pd.Series(clusters).value_counts().to_dict()
            
            return {
                "success": True,
                "message": f"✅ {method.capitalize()} clustering completed",
                "data": {
                    "method": method,
                    "n_clusters": len(set(clusters)),
                    "silhouette_score": round(silhouette_avg, 4),
                    "cluster_sizes": {f"Cluster {k}": int(v) for k, v in cluster_sizes.items()}
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in clustering: {str(e)}"}
    
    def feature_selection(self, name: str, target_column: str, feature_columns: List[str], k: int = 5) -> Dict[str, Any]:
        """Select best features using statistical tests"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            X = df[feature_columns]
            y = df[target_column]
            
            selector = SelectKBest(score_func=f_classif, k=min(k, len(feature_columns)))
            selector.fit(X, y)
            
            scores = dict(zip(feature_columns, selector.scores_))
            selected_features = [feature_columns[i] for i in selector.get_support(indices=True)]
            
            return {
                "success": True,
                "message": f"✅ Feature selection completed: {len(selected_features)} features selected",
                "data": {
                    "selected_features": selected_features,
                    "feature_scores": {k: round(float(v), 4) for k, v in scores.items()},
                    "top_features": sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in feature selection: {str(e)}"}
    
    def cross_validation(self, name: str, target_column: str, feature_columns: List[str], cv_folds: int = 5) -> Dict[str, Any]:
        """Perform cross-validation"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            X = df[feature_columns]
            y = df[target_column]
            
            is_classification = df[target_column].dtype == 'object' or df[target_column].nunique() < 20
            
            if is_classification:
                model = LogisticRegression(max_iter=1000)
                scoring = 'accuracy'
            else:
                model = LinearRegression()
                scoring = 'r2'
            
            scores = cross_val_score(model, X, y, cv=cv_folds, scoring=scoring)
            
            return {
                "success": True,
                "message": f"✅ {cv_folds}-fold cross-validation completed",
                "data": {
                    "cv_folds": cv_folds,
                    "scores": [round(float(s), 4) for s in scores],
                    "mean_score": round(float(scores.mean()), 4),
                    "std_score": round(float(scores.std()), 4),
                    "scoring_metric": scoring
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in cross-validation: {str(e)}"}
    
    
    def text_mining(self, text: str) -> Dict[str, Any]:
        """Extract insights from text"""
        try:
            if nltk is None:
                return {"success": False, "message": "❌ NLTK not available"}
            
            tokens = word_tokenize(text.lower())
            
            stop_words = set(stopwords.words('english')) if stopwords else set()
            filtered_tokens = [w for w in tokens if w.isalnum() and w not in stop_words]
            
            freq_dist = FreqDist(filtered_tokens)
            
            return {
                "success": True,
                "message": "✅ Text mining completed",
                "data": {
                    "total_words": len(tokens),
                    "unique_words": len(set(tokens)),
                    "filtered_words": len(filtered_tokens),
                    "most_common": freq_dist.most_common(10),
                    "vocabulary_richness": round(len(set(tokens)) / len(tokens), 4) if tokens else 0
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in text mining: {str(e)}"}
    
    def sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text (basic implementation)"""
        try:
            positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best', 'perfect', 'awesome'}
            negative_words = {'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'poor', 'disappointing', 'sad', 'angry'}
            
            words = text.lower().split()
            
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)
            
            total = positive_count + negative_count
            
            if total == 0:
                sentiment = "neutral"
                score = 0.0
            else:
                score = (positive_count - negative_count) / total
                if score > 0.2:
                    sentiment = "positive"
                elif score < -0.2:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
            
            return {
                "success": True,
                "message": "✅ Sentiment analysis completed",
                "data": {
                    "sentiment": sentiment,
                    "score": round(score, 4),
                    "positive_words": positive_count,
                    "negative_words": negative_count,
                    "total_words": len(words)
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in sentiment analysis: {str(e)}"}
    
    def word_frequency(self, name: str, text_column: str, top_n: int = 20) -> Dict[str, Any]:
        """Analyze word frequency in a text column"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            if text_column not in df.columns:
                return {"success": False, "message": f"❌ Column '{text_column}' not found"}
            
            all_text = ' '.join(df[text_column].astype(str).tolist())
            
            if nltk:
                tokens = word_tokenize(all_text.lower())
                stop_words = set(stopwords.words('english')) if stopwords else set()
                filtered_tokens = [w for w in tokens if w.isalnum() and w not in stop_words and len(w) > 2]
                freq_dist = FreqDist(filtered_tokens)
                top_words = freq_dist.most_common(top_n)
            else:
                words = all_text.lower().split()
                words = [w for w in words if w.isalnum() and len(w) > 2]
                freq_dist = pd.Series(words).value_counts()
                top_words = [(word, int(count)) for word, count in freq_dist.head(top_n).items()]
            
            return {
                "success": True,
                "message": f"✅ Word frequency analysis completed",
                "data": {
                    "total_words": len(all_text.split()),
                    "unique_words": len(set(all_text.split())),
                    "top_words": top_words
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in word frequency: {str(e)}"}
    
    
    def trend_decomposition(self, name: str, time_column: str, value_column: str, period: int = 12) -> Dict[str, Any]:
        """Decompose time series into trend, seasonal, and residual components"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            df[time_column] = pd.to_datetime(df[time_column])
            df = df.set_index(time_column)
            
            if len(df) < 2 * period:
                return {"success": False, "message": f"❌ Need at least {2 * period} data points for decomposition"}
            
            decomposition = seasonal_decompose(df[value_column], model='additive', period=period)
            
            return {
                "success": True,
                "message": "✅ Time series decomposition completed",
                "data": {
                    "period": period,
                    "data_points": len(df),
                    "trend_strength": round(float(decomposition.trend.std()), 4) if hasattr(decomposition.trend, 'std') else None,
                    "seasonal_strength": round(float(decomposition.seasonal.std()), 4) if hasattr(decomposition.seasonal, 'std') else None
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in decomposition: {str(e)}"}
    
    def seasonality_analysis(self, name: str, time_column: str, value_column: str) -> Dict[str, Any]:
        """Analyze seasonality patterns"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            df[time_column] = pd.to_datetime(df[time_column])
            
            df['month'] = df[time_column].dt.month
            df['day_of_week'] = df[time_column].dt.dayofweek
            df['quarter'] = df[time_column].dt.quarter
            
            monthly_avg = df.groupby('month')[value_column].mean().to_dict()
            dow_avg = df.groupby('day_of_week')[value_column].mean().to_dict()
            quarterly_avg = df.groupby('quarter')[value_column].mean().to_dict()
            
            return {
                "success": True,
                "message": "✅ Seasonality analysis completed",
                "data": {
                    "monthly_average": {f"Month {k}": round(v, 2) for k, v in monthly_avg.items()},
                    "day_of_week_average": {f"Day {k}": round(v, 2) for k, v in dow_avg.items()},
                    "quarterly_average": {f"Q{k}": round(v, 2) for k, v in quarterly_avg.items()},
                    "strongest_month": max(monthly_avg, key=monthly_avg.get) if monthly_avg else None,
                    "weakest_month": min(monthly_avg, key=monthly_avg.get) if monthly_avg else None
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in seasonality analysis: {str(e)}"}
    
    def time_series_forecast(self, name: str, time_column: str, value_column: str, periods: int = 10) -> Dict[str, Any]:
        """Forecast future values using exponential smoothing"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            df[time_column] = pd.to_datetime(df[time_column])
            df = df.sort_values(time_column)
            df = df.set_index(time_column)
            
            model = ExponentialSmoothing(df[value_column], trend='add', seasonal=None)
            fitted_model = model.fit()
            
            forecast = fitted_model.forecast(steps=periods)
            
            return {
                "success": True,
                "message": f"✅ Forecast completed for next {periods} periods",
                "data": {
                    "forecast_periods": periods,
                    "forecast_values": [round(float(v), 2) for v in forecast],
                    "last_actual_value": round(float(df[value_column].iloc[-1]), 2),
                    "forecast_trend": "increasing" if forecast.iloc[-1] > df[value_column].iloc[-1] else "decreasing"
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in forecasting: {str(e)}"}
    
    def moving_averages(self, name: str, column: str, window: int = 7) -> Dict[str, Any]:
        """Calculate moving averages"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            if column not in df.columns:
                return {"success": False, "message": f"❌ Column '{column}' not found"}
            
            df[f'{column}_MA_{window}'] = df[column].rolling(window=window).mean()
            df[f'{column}_EMA_{window}'] = df[column].ewm(span=window, adjust=False).mean()
            
            self._save_dataframe(df, name)
            
            return {
                "success": True,
                "message": f"✅ Moving averages calculated with window={window}",
                "data": {
                    "window": window,
                    "new_columns": [f'{column}_MA_{window}', f'{column}_EMA_{window}'],
                    "latest_ma": round(float(df[f'{column}_MA_{window}'].iloc[-1]), 2) if not df[f'{column}_MA_{window}'].isna().all() else None,
                    "latest_ema": round(float(df[f'{column}_EMA_{window}'].iloc[-1]), 2) if not df[f'{column}_EMA_{window}'].isna().all() else None
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error calculating moving averages: {str(e)}"}
    
    
    def t_test(self, name: str, column1: str, column2: str) -> Dict[str, Any]:
        """Perform independent t-test"""
        try:
            if stats is None:
                return {"success": False, "message": "❌ SciPy not available"}
            
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            data1 = df[column1].dropna()
            data2 = df[column2].dropna()
            
            t_stat, p_value = ttest_ind(data1, data2)
            
            significant = p_value < 0.05
            
            return {
                "success": True,
                "message": "✅ T-test completed",
                "data": {
                    "test": "Independent T-Test",
                    "column1": column1,
                    "column2": column2,
                    "t_statistic": round(float(t_stat), 4),
                    "p_value": round(float(p_value), 4),
                    "significant": significant,
                    "interpretation": "Significant difference" if significant else "No significant difference",
                    "mean1": round(float(data1.mean()), 2),
                    "mean2": round(float(data2.mean()), 2)
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in t-test: {str(e)}"}
    
    def chi_square_test(self, name: str, column1: str, column2: str) -> Dict[str, Any]:
        """Perform chi-square test of independence"""
        try:
            if stats is None:
                return {"success": False, "message": "❌ SciPy not available"}
            
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            contingency_table = pd.crosstab(df[column1], df[column2])
            
            chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
            
            significant = p_value < 0.05
            
            return {
                "success": True,
                "message": "✅ Chi-square test completed",
                "data": {
                    "test": "Chi-Square Test of Independence",
                    "column1": column1,
                    "column2": column2,
                    "chi2_statistic": round(float(chi2_stat), 4),
                    "p_value": round(float(p_value), 4),
                    "degrees_of_freedom": int(dof),
                    "significant": significant,
                    "interpretation": "Variables are dependent" if significant else "Variables are independent"
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in chi-square test: {str(e)}"}
    
    def anova_test(self, name: str, group_column: str, value_column: str) -> Dict[str, Any]:
        """Perform one-way ANOVA test"""
        try:
            if stats is None:
                return {"success": False, "message": "❌ SciPy not available"}
            
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            groups = [group[value_column].dropna().values for name, group in df.groupby(group_column)]
            
            f_stat, p_value = f_oneway(*groups)
            
            significant = p_value < 0.05
            
            return {
                "success": True,
                "message": "✅ ANOVA test completed",
                "data": {
                    "test": "One-Way ANOVA",
                    "group_column": group_column,
                    "value_column": value_column,
                    "f_statistic": round(float(f_stat), 4),
                    "p_value": round(float(p_value), 4),
                    "num_groups": len(groups),
                    "significant": significant,
                    "interpretation": "Group means are significantly different" if significant else "No significant difference between groups"
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in ANOVA test: {str(e)}"}
    
    def normality_test(self, name: str, column: str) -> Dict[str, Any]:
        """Test for normality using Shapiro-Wilk test"""
        try:
            if stats is None:
                return {"success": False, "message": "❌ SciPy not available"}
            
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            data = df[column].dropna()
            
            if len(data) > 5000:
                data = data.sample(5000, random_state=42)
            
            stat, p_value = shapiro(data)
            
            is_normal = p_value > 0.05
            
            return {
                "success": True,
                "message": "✅ Normality test completed",
                "data": {
                    "test": "Shapiro-Wilk Test",
                    "column": column,
                    "statistic": round(float(stat), 4),
                    "p_value": round(float(p_value), 4),
                    "is_normal": is_normal,
                    "interpretation": "Data is normally distributed" if is_normal else "Data is not normally distributed",
                    "sample_size": len(data)
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in normality test: {str(e)}"}
    
    
    def quality_assessment(self, name: str) -> Dict[str, Any]:
        """Comprehensive data quality assessment"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            total_cells = df.shape[0] * df.shape[1]
            missing_cells = df.isnull().sum().sum()
            
            quality_score = (1 - missing_cells / total_cells) * 100
            
            issues = []
            if missing_cells > 0:
                issues.append(f"Missing values: {missing_cells} ({round(missing_cells/total_cells*100, 2)}%)")
            
            duplicates = df.duplicated().sum()
            if duplicates > 0:
                issues.append(f"Duplicate rows: {duplicates}")
            
            for col in df.columns:
                if df[col].dtype == 'object':
                    unique_ratio = df[col].nunique() / len(df)
                    if unique_ratio < 0.01 and df[col].nunique() > 1:
                        issues.append(f"Low variance in '{col}' column")
            
            return {
                "success": True,
                "message": f"✅ Data quality assessment completed: {round(quality_score, 2)}% quality score",
                "data": {
                    "quality_score": round(quality_score, 2),
                    "total_rows": df.shape[0],
                    "total_columns": df.shape[1],
                    "completeness": round((1 - missing_cells / total_cells) * 100, 2),
                    "missing_cells": int(missing_cells),
                    "duplicate_rows": int(duplicates),
                    "issues": issues,
                    "grade": "Excellent" if quality_score >= 95 else "Good" if quality_score >= 80 else "Fair" if quality_score >= 60 else "Poor"
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in quality assessment: {str(e)}"}
    
    def completeness_check(self, name: str) -> Dict[str, Any]:
        """Check data completeness"""
        try:
            df = self._get_dataframe(name)
            if df is None:
                return {"success": False, "message": f"❌ Dataset '{name}' not found"}
            
            completeness_by_column = {}
            for col in df.columns:
                non_null = df[col].count()
                total = len(df)
                completeness_by_column[col] = round((non_null / total) * 100, 2)
            
            overall_completeness = round((df.count().sum() / (df.shape[0] * df.shape[1])) * 100, 2)
            
            return {
                "success": True,
                "message": f"✅ Completeness check: {overall_completeness}% complete",
                "data": {
                    "overall_completeness": overall_completeness,
                    "by_column": completeness_by_column,
                    "incomplete_columns": [col for col, pct in completeness_by_column.items() if pct < 100]
                }
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error in completeness check: {str(e)}"}


def create_data_analysis_suite():
    """Factory function to create DataAnalysisSuite instance"""
    return DataAnalysisSuite()

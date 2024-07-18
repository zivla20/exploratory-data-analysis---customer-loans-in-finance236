from scipy.stats import boxcox

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Plotter:
    """A class to visualise insights from the data."""
    
    def __init__(self, df):
        """Initialise Plotter class with a DataFrame"""
        self.df = df

    def plot_null_values(self):
        """Plot missing values in DataFrame"""
        null_counts = self.df.isnull().sum()
        plt.figure(figsize=(12, 6))
        sns.barplot(x=null_counts.index, y=null_counts.values)
        plt.xticks(rotation=45)
        plt.title('Number of Null Values in Each Column')
        plt.xlabel('Columns')
        plt.ylabel('Number of Null Values')
        plt.show()

    def plot_distribution(self, columns):
        """Plot distribution of given columns in DataFrame"""
        for column in columns:
            plt.figure(figsize=(10,6))
            sns.histplot(self.df[column], kde=True)
            plt.title(f'Distribution of {column}')
            plt.show()

    def plot_skewness(self, column):
        """Plot the skewness of a given column."""
        plt.figure(figsize = (12,6))
        sns.histplot(self.df[column].dropna(), kde = True)
        plt.title(f'Skewness of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()
    
    def plot_outliers(self, columns):
        """Plot boxplots for given columns to visualize outliers."""
        for column in columns:
            plt.figure(figsize=(10,6))
            sns.boxplot(x=self.df[column])
            plt.title(f"Boxplot of {column}")
            plt.xlabel(column)
            plt.show

    def plot_correlation_matrix(self):
        """Plot the correlation matrix for the DataFrame."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        plt.figure(figsize=(12,10))
        sns.heatmap(corr_matrix, annot = True, fmt='.2f', cmap = 'coolwarm', vmin=-1, vmax =1)
        plt.title('Correlation Matrix')
        plt.show()

    def plot_recovery_rate(self, total_recovery_amount, total_funded_amount):
        """
        Plot recovery rate as a percentage of loans recovered against total funding.

        Args:
        - total_recovery_amount (float): Total amount recovered from loans.
        - total_funded_amount (float): Total amount funded by investors.
        """
        # Calculate recovery rate
        recovery_rate = (total_recovery_amount / total_funded_amount) * 100

        # Calculate remaining funded amount
        remaining_funded_amount = total_funded_amount - total_recovery_amount

        # Create a DataFrame for pie chart
        data = {
            'Category': ['Recovered Amount', 'Remaining Funded Amount'],
            'Amount': [total_recovery_amount, remaining_funded_amount]
        }
        df_pie = pd.DataFrame(data)

        # Plotting the recovery rate as a pie chart
        plt.figure(figsize=(8, 5))
        plt.pie(df_pie['Amount'], labels=df_pie['Category'], autopct='%1.1f%%', startangle=90,
                colors=['#ff9999', '#66b3ff'])
        plt.title('Recovery Rate: Percentage of loans recovered against investor funding')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

    def plot_recovery_rate_over_time(self, monthly_data):
        """
        Plot recovery rate over time using a line chart.
        
        Args:
        - monthly_data (DataFrame): DataFrame with columns ['date', 'recovery_rate']
        """
        plt.figure(figsize=(10, 6))
        plt.plot(monthly_data['date'], monthly_data['recovery_rate'], marker='o', linestyle='-', color='b')
        plt.title('Recovery Rate Over Time')
        plt.xlabel('Date')
        plt.ylabel('Recovery Rate (%)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_predicted_recovery(self, projected_recovery_percentage_6_months):
        """
        Plot predicted recovery percentage up to 6 months into the future.

        Args:
        - projected_recovery_percentage_6_months (float): Projected recovery percentage.
        """
        months = range(1, 7)  # Assuming projection is for up to 6 months
        
        plt.figure(figsize=(8, 5))
        plt.plot(months, [projected_recovery_percentage_6_months] * len(months), marker='o', linestyle='-', color='g')
        plt.title('Predicted Recovery Percentage Up to 6 Months')
        plt.xlabel('Months')
        plt.ylabel('Recovery Percentage (%)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_recovery_breakdown(self, total_recovery_amount, total_funded_amount):
        """
        Plot a breakdown of recovered amount versus funded amount.
        
        Args:
        - total_recovery_amount (float): Total amount recovered from loans.
        - total_funded_amount (float): Total amount funded by investors.
        """
        labels = ['Recovered Amount', 'Remaining Funded Amount']
        sizes = [total_recovery_amount, total_funded_amount - total_recovery_amount]
        colors = ['#ff9999','#66b3ff']
        
        plt.figure(figsize=(8, 6))
        plt.bar(labels, sizes, color=colors)
        plt.title('Breakdown of Recovered Amount vs. Remaining Funded Amount')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.show()


class DataFrameTransform:
    """A class to perform EDA transformations on the data."""

    def __init__(self, df):
        """Initialise DataFrameTransform class with a DataFrame."""
        self.df = df

    def check_nulls(self):
        """Determine the amount of NULLS in each column"""
        nulls = self.df.isnull().sum()
        null_percent = (nulls/len(self.df))*100
        null_df = pd.DataFrame({'null_count': nulls, 'null_percent':null_percent})
        return null_df
    
    def drop_columns(self, threshold = 50):
        """Drop columns with missing data above a given threshold"""
        null_df = self.check_nulls()
        cols_to_drop = null_df[null_df['null_percent']>threshold].index
        self.df.drop(columns = cols_to_drop, inplace = True)
        return self.df

    def impute_numerical_nulls(self):
        """Impute missing values in numerical columns. Decide whether to impute with median or mean."""
        for column in self.df.select_dtypes(include=['number']).columns:
            if self.df[column].isnull().sum() > 0:
                skewness = self.df[column].skew()
                if abs(skewness) > 1: #Using 1 as threshold for skewness
                    self.df[column] = self.df[column].fillna(self.df[column].median())
                else:
                    self.df[column] = self.df[column].fillna(self.df[column].mean())
        return self.df

    def impute_categorical_nulls(self):
        """Impute missing values in categorical columns using the most frequent value (mode)."""
        for column in self.df.select_dtypes(include=['object', 'category']).columns:
            if self.df[column].isnull().sum() > 0:
                mode_value = self.df[column].mode()[0]
                self.df[column] = self.df[column].fillna(mode_value)
                print(f"Imputing {column} with mode ({mode_value})")
        return self.df

    def impute_nulls(self):
        """Impute missing values in both numerical and categorical columns."""
        self.impute_numerical_nulls()
        self.impute_categorical_nulls()
        return self.df

    def calculate_skewness(self, threshold = 0):
        """Calculate skewness of the DataFrame columns and return columns with skewness above threshold."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        skewed_columns = numeric_df.skew().abs()
        return skewed_columns[skewed_columns > threshold].index.tolist()

    def _calculate_skewness(self, series):
        """Helper method to apply a transformation to a pandas series."""
        return series.skew()
    
    def _transform_column(self, series, method):
        """Helper method to apply a transformation to a pandas series."""
        if method == 'log':
            return np.log1p(series)
        elif method == 'sqrt':
            return np.sqrt(series)
        elif method == 'boxcox':
            return boxcox(series+1)[0]
    
    def transform_skewed_columns(self, columns, methods = ['log', 'sqrt', 'boxcox']):
        """Automatically apply the best transformation to reduce skewness of the given columns."""
        best_transformations = {}
        
        for column in columns:
            best_method = None
            best_skewness = np.inf

            for method in methods:
                try:
                    transformed_series = self._transform_column(self.df[column], method)
                    skewness = self._calculate_skewness(transformed_series)

                    if skewness < best_skewness:
                        best_skewness = skewness
                        best_method = method
                except Exception as e:
                    print(f"Could not apply {method} transformation on {column}: {e}")

            if best_method:
                self.df[column] = self._transform_column(self.df[column], best_method)
                best_transformations[column] = best_method

        return best_transformations

    def identify_outliers(self, threshold=1.5):
        """Identify outliers using the IQR method."""
        outliers = {}
        for column in self.df.select_dtypes(include=['number']).columns:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers[column] = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)].index.tolist()
        return outliers  

    def handle_outliers(self, columns, method='remove', threshold=1.5):
        """Handle outliers in specified columns using the chosen method."""
        for column in columns:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            if method == 'remove':
                self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
            elif method == 'transform':
                self.df.loc[self.df[column] < lower_bound, column] = lower_bound
                self.df.loc[self.df[column] > upper_bound, column] = upper_bound
        return self.df

    def decide_outlier_handling(self, columns, skewness_threshold=1):
        """Decide whether to remove or transform outliers based on skewness and impact on summary statistics."""
        for column in columns:
            skewness_before = self.df[column].skew()
            mean_before = self.df[column].mean()
            median_before = self.df[column].median()

            # Try removing outliers
            df_removed = self.handle_outliers([column], method='remove').copy()
            skewness_removed = df_removed[column].skew()
            mean_removed = df_removed[column].mean()
            median_removed = df_removed[column].median()

            # Try transforming outliers
            df_transformed = self.handle_outliers([column], method='transform').copy()
            skewness_transformed = df_transformed[column].skew()
            mean_transformed = df_transformed[column].mean()
            median_transformed = df_transformed[column].median()

        if abs(skewness_removed) < abs(skewness_transformed) and abs(mean_removed - median_removed) < abs(mean_transformed - median_transformed):
            self.df = df_removed
            print(f"Removing outliers for column {column}")
        else:
            self.df = df_transformed
            print(f"Transforming outliers for column {column}")

        return self.df          
    
    def remove_highly_correlated_columns(self, threshold = 0.9):
        """Identify and remove highly correlated columns."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column]>threshold)]
        self.df.drop(columns = to_drop, inplace = True)
        return to_drop

    def calculate_recovery_rate(self):
        # Ensure 'funded_amount' and 'recoveries' columns are present and numeric
        try:
            total_funded_amount = self.df['out_prncp_inv'].astype(float).sum()
            total_recovery_amount = self.df['total_payment'].sum() + self.df['total_rec_int'].sum() + self.df['total_rec_late_fee'].sum()
        except KeyError as e:
            print(f"Column error: {e}")
            return None
        except ValueError as e:
            print(f"Value error: {e}")
            return None

        recovery_rate = (total_recovery_amount / total_funded_amount) * 100
        return recovery_rate, total_funded_amount, total_recovery_amount

    def calculate_projected_recovery_6_months(self):
        # Ensure 'last_payment_date' and 'recoveries' columns are present and numeric
        try:
            # Convert 'last_payment_date' to datetime
            self.df['last_payment_date'] = pd.to_datetime(self.df['last_payment_date'], errors='coerce')

            # Calculate the current date
            current_date = pd.Timestamp.now()

            # Calculate months since last payment using a valid method
            self.df['months_since_last_payment'] = self.df['last_payment_date'].apply(lambda x: (current_date.year - x.year) * 12 + current_date.month - x.month)

            # Calculate projected recovery rates for next 6 months
            projected_recovery_6_months = self.df[self.df['months_since_last_payment'] <= 6]['recoveries'].astype(float).sum()
            total_recoverable_amount = self.df['total_payment'].astype(float).sum() + self.df['recoveries'].astype(float).sum()
        except KeyError as e:
            print(f"Column error: {e}")
            return None
        except ValueError as e:
            print(f"Value error: {e}")
            return None

        projected_recovery_percentage_6_months = (projected_recovery_6_months / total_recoverable_amount) * 100
        return projected_recovery_percentage_6_months, total_recoverable_amount, projected_recovery_6_months

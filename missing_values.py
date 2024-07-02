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
        
    

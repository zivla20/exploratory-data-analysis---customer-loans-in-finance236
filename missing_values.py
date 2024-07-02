import pandas as pd 
import numpy as numpy
import matplotlib.pyplot as plt
import seaborn as sns

class Plotter:
    """A class to visualise insights from the data."""
    
    def __init__(self, df):
        """Initialise Plotter class with a DataFrame """
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

    def impute_columns(self):
        """Impute missing values in columns. Decide whether to impute with median or mean."""
        for column in self.df.columns:
            if self.df[column].isnull().sum() > 0:
                if strategy == 'mean':
                    self.df[column].fillna(self.df[column].mean, inplace = True)
                elif strategy == 'median':
                    self.df[column].fillna(self.df[column].median(), inplace = True)
        return self.df

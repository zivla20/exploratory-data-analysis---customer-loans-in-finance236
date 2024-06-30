import pandas as py 

class DataFrameInfo:

    """Initialise the class"""
    def __init__(self, df):
        self.df = df

    def describe_columns(self):
        """Prints out a description of all the columns."""
        print("DataFrame Description: \n")
        print(self.df.info())

    def statistical_summary(self):
        """Return a statistical summary of the DataFrame."""
        print("Statistical Summary: \n")
        return self.df.describe(include = 'all')

    def get_median(self):
        """Returns the median of all numeric columns"""
        return self.df.median

    def get_standard_deviation(self):
        """Returns the standard deviation of all numeric columns."""
        numeric_cols = self.df.select_dtypes(include=['number'])
        return numeric_cols.std()

    def get_mean(self):
        """Returns the mean of all numeric columns."""
        numeric_cols = self.df.select_dtypes(include=['number'])
        return numeric_cols.mean()

    def count_distinct_values(self):
        """Counts distinct values in each column"""
        return self.df.nunique()

    def get_shape(self):
        """Returns shape of DataFrame"""
        return self.df.shape

    def count_null_values(self):
        """Returns a count of NULL values in each column."""
        return self.df.isnull().sum()

    def count_null_values_percentage(self):
        """Returns the percentage of NULL values in each column."""
        return (self.df.isnull().sum() / len(self.df)) * 100
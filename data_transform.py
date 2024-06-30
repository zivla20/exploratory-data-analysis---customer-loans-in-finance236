import pandas as pd
from pandas.api.types import CategoricalDtype

class DataTransform:

    def __init__(self, dataframe):
        self.df = dataframe

    def convert_to_numeric(self, column_name):
        """Converts a columns to numeric, setting errors as NaN."""
        self.df[column_name] = pd.to_numeric(self.df[column_name], errors = 'coerce')
        return self.df
    
    def convert_to_datetime(self, column_names, precision='D'):
        """Converts columns to datetime with specified precision."""
        for column_name in column_names:
            self.df[column_name] = pd.to_datetime(self.df[column_name], errors='coerce')
            if precision == 'D':
                self.df[column_name] = self.df[column_name].dt.floor('D')
            elif precision == 'M':
                self.df[column_name] = self.df[column_name].dt.to_period('M')
        return self.df
    
    def convert_to_category(self, column_name):
        """Converts a columns to categorical type."""
        self.df[column_name] = self.df[column_name].astype(CategoricalDtype())
        return self.df

    def remove_symbols(self, column_name, symbols):
        """Removes specified symbols from a column using regex."""
        self.df[column_name] = self.df[column_name].replace(symbols, '', regex = True)
        return self.df

from sqlalchemy import create_engine
import pandas as pd
import yaml

def load_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials


class RDSDatabaseConnector():
    def __init__(self, credentials):
        self.host = credentials['RDS_HOST']
        self.password = credentials['RDS_PASSWORD']
        self.user = credentials['RDS_USER']
        self.database = credentials['RDS_DATABASE']
        self.port = credentials['RDS_PORT']
        self.engine = None

    def init_engine(self):
        connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_engine(connection_string)
        print("Database engine initialised.")

    def fetch_data(self, query):
        if self.engine is None:
            self.init_engine()
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def fetch_loan_payments(self):
        query = "SELECT * FROM loan_payments"
        return self.fetch_data(query)
    

def save_to_csv(df, file_path):
        df.to_csv(file_path, index = False)
        print(f"Data saved to {file_path}")

def load_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    print(f"Data Shape: {df.shape}")
    print(f"Data Sample: {df.head()}")
    print(f"Data Columns: {df.columns.tolist()}")
    return

if __name__ == "__main__":
    credentials = load_credentials("credentials.yaml")
    rds_connector = RDSDatabaseConnector(credentials)
    loan_payments_df = rds_connector.fetch_loan_payments()
    save_to_csv(loan_payments_df, "loan_payments.csv")

if __name__ == "__main__":
    file_path = "loan_payments.csv"
    loan_payments_df = load_data_from_csv(file_path)
# Project Title
Exploratory Data Analysis - Customer Loans in Finance

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

## Description
This project involves performing exploratory data analysis (EDA) on customer loan payment data stored in an AWS RDS database. The aim of the project is to extract, transform, and analyze the data to gain insights into loan payment behaviors and patterns.

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
   ``'bash
   git clone https://github.com/zivla20/exploratory-data-analysis---customer-loans-in-finance236.git
   ```
   
2. Navigate to the project directory
    ```bash
    cd exploratory-data-analysis---customer-loans-in-finance236
    ```
3. Install the required dependencies:
    ```bash
    pip install pandas sqlalchemy pyyaml boto3 psycopg2
    ```
## Usage

1. Run python db_utils.py to connect to the RDS database, fetch data, and save it locally as loan_payments.csv.

2. Use python explore_data.py to load loan_payments.csv, perform EDA, and generate visualizations

## File Structure
The project structure is as follows:
```bash
├── README.md
├── db_utils.py         # Script for database connection and data extraction
├── explore_data.py     # Script for exploratory data analysis and visualization
├── credentials.yaml    # YAML file containing RDS database credentials
├── loan_payments.csv   # CSV file storing extracted data from RDS
├── requirements.txt    # List of Python dependencies
└── .gitignore          # Git ignore file
```

## License
This project is licensed under the MIT License.


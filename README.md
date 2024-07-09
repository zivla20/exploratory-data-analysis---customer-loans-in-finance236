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

### Objectives:
- Extract data from AWS RDS database using Python and SQLAlchemy.
- Clean and preprocess data to ensure quality and reliability.
- Perform EDA to understand relationships and distributions within the dataset.
- Visualize key insights using matplotlib and seaborn.
- Document findings and insights in Jupyter notebooks for easy comprehension and future reference.

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/zivla20/exploratory-data-analysis---customer-loans-in-finance236.git
   ```
   
2. Navigate to the project directory
    ```bash
    cd exploratory-data-analysis---customer-loans-in-finance236
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage Instructions

1. Ensure you have Python installed on your machine.
2. Set up the database credentials in `credentials.yaml` (not included in the repository).
3. Run the Jupyter notebooks (`analysis.ipynb`, `data_cleaning.ipynb`) to execute the data analysis and EDA steps.
4. Refer to the notebooks for detailed explanations, visualizations, and insights derived from the data.


## File Structure
The project structure is as follows:
```bash
├── data/
│ ├── loan_payments.csv # Processed data file
├── notebooks/
│ ├── analysis.ipynb # Jupyter notebook for data analysis
│ ├── data_cleaning.ipynb # Jupyter notebook for data cleaning and preprocessing
├── src/
│ ├── db_utils.py # Python script for database utilities
│ ├── data_transform.py # Class for data transformation methods
│ ├── plotter.py # Class for visualization methods
│ ├── dataframe_info.py # Class for DataFrame information methods
├── credentials.yaml # Database credentials (ignored in git)
├── README.md # Project README file
├── requirements.txt # Python dependencies
```

## License
This project is licensed under the MIT License.


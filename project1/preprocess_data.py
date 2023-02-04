#!/usr/bin/env python3

import pandas as pd
import re

def columns_to_drop(path) -> list[str]:
    """Retrieves a list of columns from .txt file to drop from dataframe """
    with open(path, "r") as fin:
        return list(map(lambda x: x.strip("\n"), fin.readlines()))

def get_salary_estimate(salary_estimate:str) -> tuple[int, int]:
    """
    Converts a string salary range into a tuple of integers scaled into the appropriate range 
    Example: "$86K-$143K (Glassdoor est.)" -> (86000, 143000)
    """
    min_max = re.findall(r"\d+",salary_estimate)
    return tuple(map(lambda x: int(x)*1000, min_max))
    
def insert_min_salaries_col(df) -> pd.DataFrame:
    """"""
    min_salaries = list(map(lambda x: min(get_salary_estimate(x)), df["Salary Estimate"]))
    df["min_salary"] = min_salaries
    return df
    
def insert_max_salaries_col(df) -> pd.DataFrame:
    """"""
    max_salaries = list(map(lambda x: max(get_salary_estimate(x)), df["Salary Estimate"]))
    df["max_salary"] = max_salaries
    return df
    



def main():
    df = pd.read_csv("data/raw/data_scientist_salary.csv")
    df.set_index("index", inplace=True)
    insert_min_salaries_col(df)
    insert_max_salaries_col(df)
    df.drop(columns=columns_to_drop("columns_to_drop.txt"), inplace=True)
    assert not df.isnull().values.any() # check for null




    
    
    
    #df.to_csv("data/processed/data_scientist_salary_processed.tsv")
if __name__ == "__main__":
    main()
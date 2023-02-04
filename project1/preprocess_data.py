#!/usr/bin/env python3

import pandas as pd
import re

def columns_to_drop(path) -> list[str]:
    """Retrieves a list of columns from .txt file to drop from dataframe """
    with open(path, "r") as fin:
        return list(map(lambda x: x.strip("\n"), fin.readlines()))


def reformat_cols(df) -> pd.DataFrame:
    """Renames certain columns and converts all to lowercase (in place)"""
    names = {
        "Job Title":"job_title",
        "Company Name":"comp_name",
        "Lower Salary":"lower_salary_est",
        "Upper Salary":"upper_salary_est",
        "Avg Salary(K)":"avg_reported_salary",
        "Job Location":"job_location", 
    }
    df.rename(columns=names,inplace=True)
    df.columns = df.columns.str.lower()
    return df
    
    



def main():
    df = pd.read_csv("data/raw/data_scientist_salary.csv")
    df.drop(columns=columns_to_drop("columns_to_drop.txt"), inplace=True)
    df.set_index("index", inplace=True)
    reformat_cols(df)

    
    
    

    
    print(df.columns)

    
    
    assert not df.isnull().values.any() # check for null
    #df.to_csv("data/processed/data_scientist_salary_processed.csv", sep=",")
if __name__ == "__main__":
    main()
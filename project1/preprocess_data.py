#!/usr/bin/env python3

import pandas as pd
import re

def columns_to_drop(path) -> list[str]:
    """Retrieves a list of columns from .txt file to drop from dataframe """
    with open(path, "r") as fin:
        return list(map(lambda x: x.strip("\n"), fin.readlines()))

def get_salary_estimate(salary_estimate:str) -> tuple[int, int]:
    """Converts a string salary range into a tuple """
    min_max = re.findall(r"\d+",salary_estimate)
    return tuple(map(lambda x: int(x)*1000, min_max))
    
    



def main():
    df = pd.read_csv("data/raw/data_scientist_salary.csv")
    df = df.drop(columns=columns_to_drop("columns_to_drop.txt"))
    print()
    test = "$56K-$91K (Glassdoor est.)"
    print(get_salary_estimate(test))
    
    
    
    
    #df.to_csv("data/processed/data_scientist_salary_processed.csv")
if __name__ == "__main__":
    main()
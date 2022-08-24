import pandas as pd

def add_records(olympics):
    return olympics.append(pd.Series({2021: 'Tokyo', 2024: 'Paris', 2028: 'Los Angeles'}))
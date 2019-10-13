import os
import numpy as np
import pandas as pd



def process_data():
    pd.set_option('display.max_columns', None)
    filedir = os.path.join("data", "shfe")
    filename = os.path.join(filedir, "2018price.xls")
    dataframe = pd.read_excel(filename, sheet_name=0, header=2)
    dataframe = dataframe.drop(range(dataframe.shape[0] - 5, dataframe.shape[0]), axis=0)
    columns = dataframe.columns.tolist()
    dataframe = dataframe.drop(columns[-1], axis=1)
    dataframe[columns[0]] = dataframe[columns[0]].ffill()
    print(dataframe.head(15))
    print(dataframe.shape)


if __name__ == "__main__":
    process_data()
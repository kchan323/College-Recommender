import os
import pandas as pd
import numpy as np

# Convert CSV to dataframe for training and testing data.


def get_dataframes_from_files(pathTr, pathTe, debugging=False):
    dfTr = pd.read_csv(pathTr, sep=',', header=None, encoding='unicode_escape')
    dfTe = pd.read_csv(pathTe, sep=',', header=None, encoding='unicode_escape')
    if debugging:
        print("DATAFRAMES FROM CSV")
        print("Training DataFrame:")
        print(dfTr)
        print("Testing DataFrame:")
        print(dfTe)
        print()
    return dfTr, dfTe

# Filter dataframes. Drop the rows where at least one element is missing.


def filter_dataframes(dfTr, dfTe, debugging=False):
    dfTr = dfTr.dropna()
    dfTe = dfTe.dropna()
    if debugging:
        print("FILTER DATAFRAMES")
        print("Training DataFrame:")
        print(dfTr)
        print("Testing DataFrame:")
        print(dfTe)
        print("Shapes:")
        print("Training DataFrame shape: " + str(dfTr.shape))
        print("Testing DataFrame shape: " + str(dfTe.shape))
        print()
    return dfTr, dfTe

# Convert numerical values from string to float.


def update_column_types(data):
    # Loop through all data entries.
    for row in range(len(data)):
        for col in range(len(data[row])):
            try:
                # Update name where applicable.
                if type(data[row][col]) == str:
                    data[row][col] = data[row][col].replace("&amp;", "and")
                # Update numerical data to float where applicable.
                data[row][col] = float(data[row][col])
            except ValueError:
                # Keep data that cannot be converted to float.
                pass
    return data

# Convert dataframes to numpy arrays.


def get_data_from_dataframes(dfTr, dfTe, debugging=False):
    # Convert dataframes to numpy, then convert types to float where needed.
    dataTr = update_column_types(pd.DataFrame(dfTr).to_numpy()[1:])
    dataTe = update_column_types(pd.DataFrame(dfTe).to_numpy()[1:])
    if debugging:
        print("INITIAL DATA")
        print("Training Data:")
        print(dataTr)
        print("Testing Data:")
        print(dataTe)
        print()
    return dataTr, dataTe

# Use helper functions from above to convert files directly to data lists.


def get_standardized_data_from_files(pathTr, pathTe, debugging=False):
    # Get dataframes from training and testing files.
    dfTr, dfTe = get_dataframes_from_files(pathTr, pathTe, debugging)
    # Update dataframes to remove missing values.
    dfTr, dfTe = filter_dataframes(dfTr, dfTe, debugging)
    # Get numpy array equivalent of data from dataframes.
    dataTr, dataTe = get_data_from_dataframes(dfTr, dfTe, debugging)

    return dataTr, dataTe


# Toggle debugging to print out helpful information.
debugging = True

dataTr, dataTe = get_standardized_data_from_files(
    "/content/ForbesAmericasTopColleges2019.csv", "/content/ForbesAmericasTopColleges2019.csv", debugging)

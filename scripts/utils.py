import sys
import os
import pandas as pd
import numpy as np


# Grab variable dictionary
def read_variable_dict(dict_fp):
    """
    Creates a mapping of the survey question column names to updated dabase
    names based on the REC variable dictionary.

    :param dict_fp (string): Path to the variable dictionary working directory.
    :return (dictionary): Map of survey questions to variable names.
    """
    variable_dict = {}  # Store dictionary mapping question to variable

    if getattr(sys, "frozen", False):
        # When running as an executable with PyInstaller
        base_path = sys._MEIPASS
    else:
        # When running the script in development mode
        base_path = os.path.abspath(os.path.dirname(__file__))

    vardict = os.path.join(base_path, str(dict_fp))

    # Get question-variable mapping
    with open(vardict, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            question, variable = line.split(",")
            if i == 0:
                question = question.strip("\ufeff")

            # Map question to updated variable name
            variable_dict[question] = variable

    return variable_dict


# Grab survey monkey variable map
def get_sm_headers(filepath, export=True):
    ext = filepath.split(".")[-1]
    if ext == "xlsx":
        df = pd.read_excel(filepath, header=None)
    else:
        df = pd.read_csv(filepath, header=None)

    outpath = "scripts/sm_headers.csv"

    # Grab file headers
    headers = df.iloc[:2, :]

    # Replace filler columns (those that describe the response)
    headers = headers.map(
        lambda x: np.nan if str(x).lower().find("response") >= 0 else x
    )

    headers.loc[2, :] = headers.loc[0, :]
    headers = headers.loc[1:, :].reset_index(drop=True)
    headers = headers.ffill().drop_duplicates().loc[1, :].reset_index(drop=True)
    headers = headers.map(lambda x: x.split("https")[0])

    # Export
    if export:
        headers.to_csv(outpath, index=False, header=False)
    return headers

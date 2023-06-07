import pandas as pd
import os
import sys

VARIABLE_DICTIONARY = "forefront_database_dictionary.csv"


def read_variable_dict():
    """
    Creates a mapping of the survey question column names to updated dabase
    names based on the REC variable dictionary.

    :param fullpath (string): Path to application working directory.
    :return (dictionary): Map of survey questions to variable names.
    """
    variable_dict = {}  # Store dictionary mapping question to variable

    if getattr(sys, "frozen", False):
        # When running as an executable with PyInstaller
        base_path = sys._MEIPASS
    else:
        # When running the script in development mode
        base_path = os.path.abspath(os.path.dirname(__file__))

    vardict = os.path.join(base_path, VARIABLE_DICTIONARY)

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


def clean_REC_df(fullpath, filename):
    """
    Changes the database column names and ordering, from survey questions to
    variables.

    :param fullpath (string): Path to application working directory.
    :param filename (string): File name for uncleaned database.
    :return (dataframe): Pandas dataframe of cleaned database.
    """
    REC_df = pd.read_excel(os.path.join(fullpath, filename))

    # Get REC variable dictionary
    variable_dict = read_variable_dict()

    # Subset uncleand database
    rec = REC_df[list(variable_dict.keys())]

    # Change description row to variable name row
    rec.iloc[0] = list(variable_dict.values())

    # Fix column names
    new_cols = list(rec.iloc[0, :])
    rec = rec.drop([0])
    rec.columns = new_cols

    return rec

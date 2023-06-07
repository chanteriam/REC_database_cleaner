import pandas as pd
import sys

VARIABLE_DICTIONARY = "forefront_database_dictionary.csv"


def read_variable_dict():
    """
    Creates a mapping of the survey question column names to updated dabase 
    names based on the REC variable dictionary.

    :return (dictionary): Map of survey questions to variable names.
    """
    variable_dict = {}  # Store dictionary mapping question to variable

    # Get question-variable mapping
    with open(VARIABLE_DICTIONARY, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            question, variable = line.split(",")
            if i == 0:
                question = question.strip("\ufeff")

            # Map question to updated variable name
            variable_dict[question] = variable

    return variable_dict


def clean_REC_df(filepath):
    """
    Changes the database column names and ordering, from survey questions to
    variables.

    :param filepath (string): File path for uncleaned database.
    :return (dataframe): Pandas dataframe of cleaned database.
    """
    REC_df = pd.read_excel(filepath)

    # Get REC variable dictionary
    variable_dict = read_variable_dict()

    # Subset uncleand database
    rec = REC_df[list(variable_dict.keys())]

    # Change description row to variable name row
    rec.iloc[0] = list(variable_dict.values())

    # Fix column names
    new_cols = list(rec.iloc[0, :])

    rec.columns = new_cols
    return rec


def main(filepath):
    """
    Generates and exports a cleaned Forefront Racial Equity Map database with 
    updated variable names and column orders. Cleaned database exported to the
    "output/" directory.

    :param filepath (string): File path for the uncleaned database.
    """
    rec = clean_REC_df(filepath)

    # Get cleaned database output file name
    filepath = filepath.split("/")[1].split(".xlsx")  # get extension
    new_filepath = "output/" + filepath[0] + "_cleaned.xlsx"

    # Export cleaned database to xlsx
    rec.to_excel(new_filepath, index=False)

if __name__ == '__main__':

    # Get database file path
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
    else:
        # MANUALLY CHANGE ME
        filepath = (
            "Racial+Equity+Collective+of+Illinois+Mapping+Survey_March+1,+2023_10.22.xlsx"
        )
        
    # Ensure correct path
    if "input/" not in filepath:
        filepath = "input/" + filepath

    # Clean and export database
    main(filepath)
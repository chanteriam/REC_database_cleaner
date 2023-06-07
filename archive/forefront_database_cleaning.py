import pandas as pd


def read_variable_dict(filepath):
    variable_dict = {}  # dictionary mapping question to variable

    # get question-variable mapping
    with open(filepath, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            question, variable = line.split(",")
            if i == 0:
                question = question.strip("\ufeff")
            variable_dict[question] = variable

    return variable_dict


def main(filepath):
    REC_df = pd.read_excel(filepath)

    # get variable dictionary
    variable_dict = read_variable_dict("forefront_database_dictionary.csv")

    # subset database
    rec = REC_df[list(variable_dict.keys())]

    # change description row to variable name row
    rec.iloc[0] = list(variable_dict.values())

    filepath = filepath.split(".")  # get extension
    new_filepath = filepath[0] + "_cleaned." + filepath[1]

    rec.to_excel(new_filepath)

import pandas as pd
import numpy as np
import os
import sys

from scripts.constants import (
    VARIABLE_DICT_MAP,
    SM_COL_MAP,
    SM_COLS_FP,
    bool_cols,
    output_cols,
    other_org_cols,
    years_operational_map,
    bipoc_staff_perc_map,
    other_cols,
)
from scripts.utils import get_sm_headers


class Cleaner:
    """
    Implements parent Cleaner class for cleaning Forefront REC map survey data.

    params:
        fullpath (string): path to the application working directory.
        filename (string): filename of data to clean.
    """

    def __init__(self, fullpath, filename, variable_dict):
        ext = filename.split(".")[-1]
        self.filepath = os.path.join(fullpath, filename)
        if ext == "xlsx":
            self.data = pd.read_excel(self.filepath)
        else:
            self.data = pd.read_csv(self.filepath)

        self.variable_dict = variable_dict
        self.cleaned = None

    def remove_test(self):
        """
        Removes test data from the cleaned df, identified by any cells
        containing "test".
        """
        self.cleaned = self.cleaned.loc[
            ~(
                self.cleaned.apply(
                    lambda row: row.astype(str).str.contains("test", case=False).any(),
                    axis=1,
                )
            ),
            :,
        ]

    def clean_data(self):
        pass

    def fill_zip(self, zip):
        """
        Ensures that zip codes are 5 characters long
        """
        if str(zip) == "nan":
            return ""

        if len(str(zip)) < 5:
            new_zip = "0" * (5 - len(str(zip))) + str(zip)
            return new_zip

        return str(zip)


class QualtricsCleaner(Cleaner):
    """
    Implements Cleaner class for Qualtrics survey data.
    """

    def clean_data(self):
        """
        Cleans inputted qualtrics data.
        """
        # Subset uncleand database
        rec = self.data[list(self.variable_dict.keys())]

        # Change description row to variable name row
        rec.iloc[0] = list(self.variable_dict.values())

        # Fix column names
        new_cols = list(rec.iloc[0, :])
        rec = rec.drop([0])
        rec.columns = new_cols

        # Change yes/no response cols to true/false
        for col in bool_cols:
            rec.loc[rec.loc[:, col] == "Yes", col] = True
            rec.loc[rec.loc[:, col] == "No", col] = False
            rec.loc[rec.loc[:, col].isna(), col] = ""

        # Clean "other organization" emails
        for col in other_org_cols:
            rec.loc[
                (rec.loc[:, col].isna())
                | ~(rec.loc[:, col].str.contains("@", na=False)),
                col,
            ] = ""

        # ensure zipcodes are 5 charactes
        rec.loc[:, "Mailing Zip/Postal Code"] = rec.loc[
            :, "Mailing Zip/Postal Code"
        ].apply(lambda x: self.fill_zip(x))

        self.cleaned = rec


class SMCleaner(Cleaner):
    """
    Implements Cleaner class for Survey Monkey (SM) data.
    """

    def __init__(self, fullpath, filename, variable_dict):
        super().__init__(fullpath, filename, variable_dict)

        # assert file
        correct_cols = pd.read_csv(SM_COLS_FP)
        assert list(self.data.columns) == list(
            correct_cols.columns
        ), "PLEASE ENSURE THAT YOU ARE DOWNLOADING SURVEY MONKEY DATA USING CONDENSED COLUMNS"

    def clean_data(self):
        """
        Cleans inputted survey monkey data.
        """

        # check if headers file exists
        if not os.path.isfile("scripts/sm_headers.csv"):
            heads = get_sm_headers(self.filepath)
        else:
            heads = pd.read_csv("scripts/sm_headers.csv", header=None)[0]

        # grab relevant rows and rename cols to match derived headers
        df = self.data.iloc[1:, :].reset_index(drop=True)
        df.columns = list(heads)

        # grab columns that don't need pre-processing
        accurate_cols = self.variable_dict.loc[
            self.variable_dict.loc[:, "type"] == "column", ["heads", "mapped"]
        ]
        acc_col_idx = list(accurate_cols.index)

        # Redefine Service Region cols - from yes/no to service region names
        df.iloc[:, SM_COL_MAP["Service Region"]] = df.iloc[
            :, SM_COL_MAP["Service Region"]
        ].apply(lambda x: self.rename_cols(x))

        # Ensure years have a space around the hiphens
        df.iloc[:, SM_COL_MAP["Years Operational"]] = df.iloc[
            :, SM_COL_MAP["Years Operational"]
        ].replace(years_operational_map)

        # Fix Staff and Leadership percentages
        df.iloc[:, SM_COL_MAP["BIPOC Staff Percentages"]] = df.iloc[
            :, SM_COL_MAP["BIPOC Staff Percentages"]
        ].replace(bipoc_staff_perc_map)

        # Ensire Equity Topics "Other (please specify)" is just "Other"
        df.iloc[:, other_cols] = df.iloc[:, other_cols].applymap(
            lambda x: x if str(x) == "nan" else "Other"
        )

        rec = df.iloc[:, acc_col_idx]
        rec.columns = list(accurate_cols.loc[:, "mapped"])

        # Define new, condenced columns
        for col, idxs in SM_COL_MAP.items():
            rec.loc[:, col] = df.iloc[:, idxs].apply(
                lambda x: self.concat_row(x), axis=1
            )

        # Change yes/no response cols to true/false
        for col in bool_cols:
            rec.loc[rec.loc[:, col] == "Yes", col] = True
            rec.loc[rec.loc[:, col] == "No", col] = False
            rec.loc[rec.loc[:, col].isna(), col] = ""

        # Clean "other organization" emails
        for col in other_org_cols:
            rec.loc[
                (rec.loc[:, col].isna())
                | ~(rec.loc[:, col].str.contains("@", na=False)),
                col,
            ] = ""

        # ensure zipcodes are 5 charactes
        rec.loc[:, "Mailing Zip/Postal Code"] = rec.loc[
            :, "Mailing Zip/Postal Code"
        ].apply(lambda x: self.fill_zip(x))

        # Add missing columns
        rec.loc[:, "Completed Survey"] = True
        rec.loc[rec.loc[:, "Consent"] == "", "Completed Survey"] = False
        rec.loc[:, "Email"] = rec.loc[:, "REC Respondent Email"]
        rec.loc[:, "Organization: Account Name"] = rec.loc[
            :, "REC Invited Organization"
        ]

        self.cleaned = rec.loc[:, output_cols]

    def rename_cols(self, col):
        """
        Renames service area column values from 'Yes'/'No' to the specific service area.

        params:
            cols (Series): column to rename.

        returns (Series): altered column.
        """
        new_col = col.apply(
            lambda x: list(
                self.variable_dict.loc[
                    self.variable_dict.loc[:, "heads"].str.contains(col.name.strip()),
                    "mapped",
                ]
            )[0]
            if x == "Yes"
            else ""
        )
        return new_col

    def concat_row(self, row):
        """
        Concatenates row data into a single value.

        params:
            row (DataFrame): row data to concatenate.

        returns (string): concatenated row data.
        """
        vals = list(row)

        # remove null values
        clean_vals = [val for val in vals if str(val) != "nan" and val != ""]

        return ";".join(clean_vals)


def main(fullpath, filename, source):
    """
    Coordinates REC map data cleaning.

    params:
        fullpath (string): path to the application working directory.
        filename (string): filename of data to clean.
        source (string): data source (qualtrics or survey monkey).
        test (bool): if we're in the testing environment
    """

    if source.lower() == "qualtrics":
        cleaner = QualtricsCleaner(
            fullpath, filename, VARIABLE_DICT_MAP[source.lower()]
        )
    else:
        cleaner = SMCleaner(fullpath, filename, VARIABLE_DICT_MAP[source.lower()])

    # Clean input data
    cleaner.clean_data()

    # Remove any test or filler data
    cleaner.remove_test()

    return cleaner.cleaned

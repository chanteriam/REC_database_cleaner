from scripts.utils import read_variable_dict
import pandas as pd

# Qualtrics variable dictionary
var_dict_fp_q = "qualtrics_database_dictionary.csv"
VARIABLE_DICTIONARY_Q = read_variable_dict(var_dict_fp_q)

# Survey monkey variable dictionary
var_dict_fp_s = "scripts/sm_database_dictionary.csv"
VARIABLE_DICTIONARY_S = pd.read_csv(var_dict_fp_s, header=0, encoding="latin-1")

VARIABLE_DICT_MAP = {
    "qualtrics": VARIABLE_DICTIONARY_Q,
    "survey monkey": VARIABLE_DICTIONARY_S,
}

SM_COLS_FP = "scripts/sm_cols.csv"

# Survey Monkey constants
SM_COL_MAP = {
    "Service Region": [28, 53, 98],
    "Service Region - Northern IL": [i for i in range(29, 53)],
    "Service Region - Central IL": [i for i in range(54, 98)],
    "Service Region - Southern IL": [i for i in range(99, 133)],
    "Type": [133, 134],
    "Type of Racial Equity Work": [135, 261],
    "Program 1 Equity Topics": [i for i in range(139, 159)],
    "Program 2 Equity Topics": [i for i in range(164, 184)],
    "Program 3 Equity Topics": [i for i in range(189, 209)],
    "Program 4 Equity Topics": [i for i in range(214, 234)],
    "Program 5 Equity Topics": [i for i in range(239, 259)],
    "Policy 1 Equity Topics": [i for i in range(265, 285)],
    "Policy 2 Equity Topics": [i for i in range(290, 310)],
    "Policy 3 Equity Topics": [i for i in range(315, 335)],
    "Policy 4 Equity Topics": [i for i in range(340, 360)],
    "Policy 5 Equity Topics": [i for i in range(365, 385)],
    "Years Operational": [160, 185, 210, 235, 260, 286, 311, 336, 361, 386],
    "BIPOC Staff Percentages": [389, 392],
}

years_operational_map = {"1-4 years": "1 - 4 years", "5-9 years": "5 - 9 years"}
bipoc_staff_perc_map = {
    "25%-50%": "25% to 50%",
    "51%-75%": "51% to 75%",
    "76%-100%": "76% to 100%",
}

output_cols = [
    "REC Invited Organization",
    "REC Respondent Email",
    "Completed Survey",
    "Screener: Racial Equity Work",
    "Screener: Type of Equity Work",
    "Screener: Work in IL",
    "Organization: Account Name",
    "Organization: Acronym",
    "Organization: Main Website",
    "Email",
    "Organization: Main Phone Number",
    "Mailing Address Line 1",
    "Mailing Address Line 2",
    "Mailing City",
    "Mailing State/Province",
    "Mailing Zip/Postal Code",
    "Service Areas",
    "Service Region",
    "Service Region - Northern IL",
    "Service Region - Central IL",
    "Service Region - Southern IL",
    "Type",
    "Type of Racial Equity Work",
    "More than One Program",
    "Program 1 Name",
    "Program 1 Industry Area",
    "Program 1 Equity Topics",
    "Program 1 Description",
    "Program 1 Years Operational",
    "Program 2 Name",
    "Program 2 Industry Area",
    "Program 2 Equity Topics",
    "Program 2 Description",
    "Program 2 Years Operational",
    "Program 3 Name",
    "Program 3 Industry Area",
    "Program 3 Equity Topics",
    "Program 3 Description",
    "Program 3 Years Operational",
    "Program 4 Name",
    "Program 4 Industry Area",
    "Program 4 Equity Topics",
    "Program 4 Description",
    "Program 4 Years Operational",
    "Program 5 Name",
    "Program 5 Industry Area",
    "Program 5 Equity Topics",
    "Program 5 Description",
    "Program 5 Years Operational",
    "More than One Policy",
    "Policy 1 Name",
    "Policy 1 Industry Area",
    "Policy 1 Equity Topics",
    "Policy 1 Description",
    "Policy 1 Years Operational",
    "Policy 2 Name",
    "Policy 2 Industry Area",
    "Policy 2 Equity Topics",
    "Policy 2 Description",
    "Policy 2 Years Operational",
    "Policy 3 Name",
    "Policy 3 Industry Area",
    "Policy 3 Equity Topics",
    "Policy 3 Description",
    "Policy 3 Years Operational",
    "Policy 4 Name",
    "Policy 4 Industry Area",
    "Policy 4 Equity Topics",
    "Policy 4 Description",
    "Policy 4 Years Operational",
    "Policy 5 Name",
    "Policy 5 Industry Area",
    "Policy 5 Equity Topics",
    "Policy 5 Description",
    "Policy 5 Years Operational",
    "Racial Equity Challenge",
    "BIPOC Staff: Senior Leader",
    "BIPOC Staff: Leadership Percentage",
    "BIPOC Staff: Majority",
    "Organization: Staff Size Range",
    "BIPOC Staff: Percentage",
    "Consent",
    "Racial Equity Contact: Name",
    "Racial Equity Contact: Phone",
    "Racial Equity Contact: Email",
    "Other Organization 1 Name",
    "Other Organization 2 Name",
    "Other Organization 3 Name",
    "Other Organization 1 Email",
    "Other Organization 2 Email",
    "Other Organization 3 Email",
]

bool_cols = [
    "Screener: Racial Equity Work",
    "Screener: Work in IL",
    "More than One Program",
    "More than One Policy",
    "Consent",
    "BIPOC Staff: Senior Leader",
    "BIPOC Staff: Majority",
]

other_org_cols = [
    "Other Organization 1 Email",
    "Other Organization 2 Email",
    "Other Organization 3 Email",
]

other_cols = [158, 183, 208, 233, 258, 284, 309, 334, 359, 384]

def count_by_value(column):
    # get unique values
    unique_values = list(column.unique())
    counts = {}

    # get count of actual values
    for value in unique_values:
        # get count of null values
        if str(value) == "nan":
            counts[value] = counts.get(value, 0) + len(column.isnull())
            continue

        counts[value] = column[column == value].count()

    # get count of null values

    return counts


def summarize(database, cols):
    descriptives = {}

    database[cols].apply(lambda x: descriptives.update({x.name: count_by_value(x[1:])}))

    return descriptives


def main():
    pass


cols_count_by_value = [
    "Q2",
    "Q3",
    "Q4",
    "Q9",
    "Q10",
    "Q11",
    "Q12",
    "Q13",
    "Q14",
    "Q15",
    "Q16",
]

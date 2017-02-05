import pandas 
import csv
def csv_read(csvfile):
    '''
    Takes csv in the form of the training dataset and returns as list of lists
    representing each row.
    Parameters
    ----------
    csvfile: directory of csv file

    Returns
    -------
    dataset: dataset including header as list of lists
    '''
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        dataset = list(reader)
    return dataset


def urls_from_csv(dataset, column=None, header=1):
    '''
    Takes csv in the form of the training dataset and returns list of URLs
    Parameters
    ----------
    csv: path to csv file containing urls
    column: integer number (0 indexed) or name of column with urls
            if not given, function will try to find column with urls
    header: used to index beginning of rows
            defaults to 1, assumes header present

    Returns
    -------
    urls: a list of URLs
    '''
    # if a column is given
    if column:
        # check whether it is a valid integer
        if isinstance(column, int) and column < len(dataset[0]):
            # take urls from that column
            urls = [line[column] for line in dataset[header:]]
        # if a column name is given, check header also selected and is present
        elif isinstance(column, str) and header == 1 and column in dataset[0]:
            # find the column index containing the string
            column = dataset[0].index(column)
            urls = [line[column] for line in dataset[header:]]
        elif isinstance(column, str) and header == 0:
            raise ValueError("Invalid use of column name."
                             "No header present in dataset.")
        elif isinstance(column, str) and column not in dataset[0]:
            raise ValueError("Invalid column name."
                             "Column name specified not in dataset."
                             "Please use a valid column name.")
        else:
            raise ValueError("Column index not in range of dataset."
                             "Please choose a valid column index.")
    # if no column specified, try to find by looking for
    elif column is None:
        first_row = dataset[header]
        index = [i for i, s in enumerate(first_row) if 'http' in s]
        urls = [line[index] for line in dataset[header:]]
    else:
        raise ValueError("Can't find any URLs!")

    return urls

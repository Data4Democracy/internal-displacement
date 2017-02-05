import csv


def csv_read(csvfile):
    """
    Takes csv in the form of the training dataset and returns as list of lists
    representing each row.
    Parameters
    ----------
    csvfile: directory of csv file

    Returns
    -------
    dataset: dataset including header as list of lists
    """
    f =open(csvfile, 'r')
    reader = csv.reader(f)
    dataset = list(reader)
    f.close()
    return dataset


def urls_from_csv(dataset, url_column="URL", label_column=None, header=1):
    """
    Takes csv in the form of the training dataset and returns list of URLs
    Parameters
    ----------
    csv: path to csv file containing urls
    column: integer number (0 indexed) or name of column with urls
            if not given, function will try to find column with urls
    label_column: integer number (0 indexed) or name of column with labels.
            if not given, function will assume there are no labels
    header: used to index beginning of rows
            defaults to 1, assumes header present

    Returns
    -------
    a list of URLs
    OR
    a list of (url,label) tuples
    """

    # if an url_column is given
    if url_column:
        # check whether it is a valid integer
        if isinstance(url_column, int) and url_column < len(dataset[0]):
            # take urls from that url_columns
            urls = [line[url_column] for line in dataset[header:]]
        # if a column name is given, check header also selected and is present
        elif isinstance(url_column, str) and header == 1 and url_column in dataset[0]:
            # find the column index containing the string
            url_columns = dataset[0].index(url_column)
            urls = [line[url_columns] for line in dataset[header:]]
        elif isinstance(url_columns, str) and header == 0:
            raise ValueError("Invalid use of url_column name."
                             "No header present in dataset.")
        elif isinstance(url_columns, str) and url_column not in dataset[0]:
            raise ValueError("Invalid url_url_columns name."
                             "Column name specified not in dataset."
                             "Please use a valid column name.")
        else:
            raise ValueError("Column index not in range of dataset."
                             "Please choose a valid column index.")
    # if no url_column specified, try to find by looking for
    elif url_column is None:
        print(header)
        first_row = dataset[header]
        print(first_row)
        index = [i for i, s in enumerate(first_row) if 'http' in s]
        urls = [line[index] for line in dataset[header:]]
    else:
        raise ValueError("Can't find any URLs!")


    # If a label column is provided:
    if label_column:
        if isinstance(label_column, int) and label_column < len(dataset[0]):
            # take labels from that column
            urls = [line[column] for line in dataset[header:]]
        # if a column name is given, check header also selected and is present
        elif isinstance(label_column, str) and header == 1 and label_column in dataset[0]:
            # find the column index containing the string
            label_column = dataset[0].index(label_column)
            labels = [line[label_column] for line in dataset[header:]]
        elif isinstance(label_column, str) and header == 0:
            raise ValueError("Invalid use of label_column name."
                             "No header present in dataset.")
        elif isinstance(label_column, str) and column not in dataset[0]:
            raise ValueError("Invalid label_column name."
                             "Column name specified not in dataset."
                             "Please use a valid label_column name.")
        else:
            raise ValueError("label_column index not in range of dataset."
                             "Please choose a valid label_column index.")

        return list(zip(urls, labels))
    else:
        return urls



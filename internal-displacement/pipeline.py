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

def csv2dict(csvfile):
    '''
    Takes csv in the form of the training dataset and returns as list of
    ordered dictionaries each representing a row.
    Parameters
    ----------
    csvfile: directory of csv file

    Returns
    -------
    dataset: dataset including header as list of ordered dictionaries
    '''
    with open(csvfile, 'r') as f:
        reader = csv.DictReader(f)
        dataset = [line for line in reader]
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


def sample_urls(urls, size=0.25, random=True):
        '''
        Return a subsample of URLs. Helpful function if you don't want to 
        scrape a large number of URLs from a dataset.
        Parameters
        ----------
        size: float or int, default 0.25.
            If float, should be between 0.0 and 1.0 and is
            the size of the subsample of return. If int, represents
            the absolute size of the sample to return.

        random: boolean, default True
            Whether or not to generate a random or direct subsample.

        Returns
        -------
        urls_sample: subsample of urls as Pandas Series
        '''
        if isinstance(size, int) and size <= len(urls):
            sample_size = size
        elif isinstance(size, int) and size > len(urls):
            raise ValueError("Sample size cannot be larger than the"
                             " number of urls.")
        elif isinstance(size, float) and size >= 0.0 and size <= 1.0:
            sample_size = int(size * len(urls))
        else:
            raise ValueError("Invalid sample size."
                             " Please specify required sample size as"
                             " a float between 0.0 and 1.0 or as an integer.")

        if isinstance(random, bool):
            randomize = random
        else:
            raise ValueError("Invalid value for random."
                             " Please specify True or False.")

        if randomize:
            return np.random.choice(urls, sample_size)
        else:
            return urls[:sample_size]
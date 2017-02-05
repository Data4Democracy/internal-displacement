"""
A pipeline to facilitate the extraction and storage of data from URLS.
Purpose:
    - Ensure articles are only ever scraped once.
    - Facilitate ingestion of articles (which may or may not be labeled with a category)
    - Facilitate export of articles into
        - A pandas dataframe
        - A file
        - A database
"""
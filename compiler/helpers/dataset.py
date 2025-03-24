import csv, logging
import pandas as pd
from config import dataset
from config import TC1_COL, TC2_COL, TC3_COL, PROCES_COL, PROCESSTAP_COL, LT_COL, OI_COL, PI_COL, DT_COL


# Helper function to check if a row is empty
def checkRowEmpty(row):
    columns_to_check = [TC1_COL, TC2_COL, TC3_COL, PROCES_COL, PROCESSTAP_COL, LT_COL, OI_COL, PI_COL, DT_COL]
    return any(index >= len(row) or row[index] in ("", None) for index in columns_to_check)

# Parse the dataset file from a XLSX file to a list.
def parseDatasetFile(datasetFile):
    global dataset
    try:
        # Open the dataset and parse it to a list
        df = pd.read_excel(datasetFile)
        csvData = df.to_csv(index=False, sep=';')
        reader = csv.reader(csvData.splitlines(), delimiter=';', quotechar='|')
        dataset.extend(list(reader)[1:])
        
        # Remove empty rows, this is done to prevent errors when reading the dataset
        for row in dataset[1:]:
            if checkRowEmpty(row): 
                dataset.remove(row)
                logging.info(f"Removed empty row: {row}")

    except FileNotFoundError as e:
        logging.error(f"Dataset file {datasetFile} not found")
        raise
    except Exception as e:
        logging.error(f"An error occurred while reading the dataset file: {str(e)}")
        raise

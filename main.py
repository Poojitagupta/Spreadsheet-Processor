from SpreadsheetDataProcessor import SpreadsheetDataProcessor

processor = SpreadsheetDataProcessor()
while True:
    choice = input("Do you want to process the data of your spreadsheet? (Y/N)").strip().lower()
    if choice == 'y':
        processor.process_spreadsheet()
    else:
        break
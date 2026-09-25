from SpreadsheetDataProcessor import SpreadsheetDataProcessor

while True: 
    processor = SpreadsheetDataProcessor()
    x = processor.process_spreadsheet()
    if not x:
        break
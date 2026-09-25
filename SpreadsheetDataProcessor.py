import csv
from Converter import convert_datetime, convert_date, convert_boolean
from helper.get_data_type import get_data_type
from helper.get_field_name import get_field_name
from helper.handle_invalid_data import handle_invalid_data

class SpreadsheetDataProcessor:
    converter = {"1" : str, "2" : int, "3" : float, "4" : convert_date, "5" : convert_datetime, "6" : convert_boolean }
    def __init__(self):
        self.f = None
        self.fields = []             #List to store the field names
        self.records = []            #List of dictionaries to store each row with the field name
        self.summary = {}            #Dictionary of dictionary to store the total and average of numeric fields
        self.filtered_result = []    #List of dictionary to store filtered result
        self.report = []             #List of list to store the report in which each list denotes a row in csv file


    def __load_spreadsheet(self):
        while True:
            path = input("Enter the path of the spreadsheet file : ")
            path = path.strip()
            if not path.endswith(".csv"):
                print("Please enter a csv file")
                continue
            try:
                self.f = open(path, 'r', newline = '', encoding = "utf-8")
                return
            except FileNotFoundError:
                print("File not found")
            except PermissionError:
                print("Don't have the permission to access the file")
            except OSError as e:
                print("OS error : ", e)

    def __read_records(self):
        rows = []
        reader = csv.reader(self.f)
        try:
            self.fields = next(reader)
        except StopIteration:
            print("The file is empty")
            self.f.close()
            return False
        for row in reader:
            rows.append(row)

        if len(rows) == 0:
            print("The file doesn't contain any data")
            self.f.close()
            return False
        self.f.close()

        for i, row in enumerate(rows):
            if len(row) != len(self.fields):
                print(f"Skipping row number {i} with incorrect number of fields")
                continue
            record = {}
            for i in range(len(self.fields)):
                record[self.fields[i]] = row[i]
            self.records.append(record)  
        return True

    def __validate_data(self, field_name, data_type):
        missing = []
        invalid = []
        converter = self.converter[data_type]

        for i, record in enumerate(self.records):
            value = record[field_name]
            if value == "":
                missing.append(i)
                continue
            try:
                record[field_name] = converter(value)
            except ValueError:
                invalid.append(i)

        return missing, invalid

    def __calculate_summary(self):
        
        field_name = get_field_name(self.fields)
        data_type = get_data_type(field_name, SpreadsheetDataProcessor.converter)
        if data_type is None:
            return
        if data_type not in ("2", "3"):
            print("Summary can only be calculated for numeric fields")
            return

        missing, invalid = self.__validate_data(field_name, data_type)
        print(f"Missing values : {len(missing)}")
        print(f"Invalid values : {len(invalid)}")
        ignored_rows, self.records = handle_invalid_data(SpreadsheetDataProcessor.converter, data_type, field_name, missing, invalid, self.records)

        if ignored_rows is None:
            print("Calculation is cancelled")
            return
        
        total = 0
        cnt = 0
        for i in range(len(self.records)):
            if i in ignored_rows:
                continue
            else:
                total += self.records[i][field_name]
                cnt += 1
        try:
            self.summary[field_name] = {"Total" : total, "Average" : total/cnt}
        except ZeroDivisionError:
            self.summary[field_name] = {"Total" : total, "Average" : 0}
        print("Calculated summary")

    def __filter_records(self):
        field_name = get_field_name(self.fields)
        data_type = get_data_type(field_name, SpreadsheetDataProcessor.converter)
        if data_type is None:
            return
        missing, invalid = self.__validate_data(field_name, data_type)
        print(f"Missing values : {len(missing)}")
        print(f"Invalid values : {len(invalid)}")
        ignored_rows, self.records = handle_invalid_data(SpreadsheetDataProcessor.converter, data_type, field_name, missing, invalid, self.records)

        if ignored_rows is None:
            return

        filtered_record = []
        for i in range(5):
            value = input("Enter the value for filteration : ")
            try:
                value = self.converter[data_type](value)
                break

            except ValueError:
                print(f"Selected field for filteration is {field_name}, provide the value of correct data type")
            if i == 3:
                print("This is your last chance otherwise the feature will terminate!")
            if i == 4:
                print("Terminating filter process...")
                return

        for i, record in enumerate(self.records):
            if i in ignored_rows:
                continue
            if data_type == "1":
                if record[field_name].lower() == value.lower():
                    filtered_record.append(record)
            else:
                if record[field_name] == value:
                    filtered_record.append(record)
        filter_info = {
            "field": field_name,
            "value": value,
            "records": filtered_record
        }

        self.filtered_result.append(filter_info)
        print("Fileteration done")

    def __create_report(self):
        self.report = []
        self.report.append(["SUMMARY"])
        self.report.append(["Total Records", len(self.records)])
        self.report.append([])
        if len(self.summary) > 0:
            self.report.append(["Field", "Total", "Average"])
            for field, values in self.summary.items():
                self.report.append([field, values["Total"], values["Average"]])

        self.report.append([])        

        if len(self.filtered_result) > 0:
            self.report.append(["FILTERED RECORDS"])
            for info in self.filtered_result:
                self.report.append(["Filter Field", info["field"]])
                self.report.append(["Filter Value", info["value"]])
                if info["records"]:
                    self.report.append(self.fields)
                    for record in info["records"]:
                        self.report.append([record[field] for field in self.fields])
                else:
                    self.report.append(["No matching records found"])
                    self.report.append([])

        print("Report created")

    def __save_spreadsheet(self):
        while True:
            path = input("Enter the path where the report should be saved : ")
            path = path.strip()
            if not path.endswith(".csv"):
                print("Please enter a csv file")
                continue
            try:
                with open(path, 'w', newline = '') as f:
                    writer = csv.writer(f)
                    writer.writerows(self.report)
                    print("Report saved")
                return
            except FileNotFoundError:
                print("File not found")
            except PermissionError:
                print("Don't have the permission to access the file")
            except OSError as e:
                print("OS error : ", e)

    def process_spreadsheet(self):
        self.__load_spreadsheet()
        if not self.__read_records():
            return
        choice = 1
        while choice:
            try:
                choice = int(input("Press\n1 for Calculate summary\n2 for Filter records\n3 for Create report\n4 for again\n5 Exit\n"))
            except ValueError:
                print("Please enter from 1 to 5")
                continue
            if choice == 1:
                self.__calculate_summary()
            elif choice == 2:
                self.__filter_records()
            elif choice == 3:
                self.__create_report()
                self.__save_spreadsheet()
            elif choice == 4:
                return True
            elif choice == 5:
                break
            else:
                print("Please enter from 1 to 5")
        return False
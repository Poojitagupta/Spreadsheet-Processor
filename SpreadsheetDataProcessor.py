import csv
from Converter import convert_datetime, convert_date, convert_boolean

class SpreadsheetDataProcessor:
    converter = {"int" : int, "float" : float, "string" : str, "date" : convert_date, "datetime" : convert_datetime, "boolean" : convert_boolean }
    def __init__(self):
        self.f = None
        self.fields = []             #List to store the field names
        self.records = []            #List of dictionaries to store each row with the field name
        self.field_type = {}         #Dictionary to store field name with the data type of that field
        self.missing = []            #List of dictionary to store row number and field name of missing values
        self.invalid_type = []       #List of dictionary to store row number and field name of invalid data type of data
        self.summary = {}            #List of dictionary to store the total and average of numeric fields
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
                self.f = open(path, 'r', newline = '')  
                return
            except FileNotFoundError:
                print("File not found")
            except Exception as e:
                print(e)
                print("Enter a valid path")

    def __read_records(self):
        rows = []
        reader = csv.reader(self.f)
        try:
            self.fields = next(reader)
        except:
            print("The file is empty")
            return False
        for row in reader:
            rows.append(row)

        if len(rows) == 0:
            print("The file doesn't contain any data")
            return False
        self.f.close()
        

        for field in self.fields:
            while True:
                data_type = input(f"Enter the data type of {field} column (string/int/float/date/datetime/boolean): ").strip().lower()
                if data_type in SpreadsheetDataProcessor.converter:
                    self.field_type[field] = data_type
                    break
                else:
                    print("Enter from the given options only")

        for row in rows:
            if len(row) != len(self.fields):
                continue
            record = {}
            for i in range(len(self.fields)):
                record[self.fields[i]] = row[i]
            self.records.append(record)  
        return True

    def __validate_data(self):
        for i in range(len(self.records)):
            for key, value in self.records[i].items():
                if value == "":
                    self.missing.append((i, key))
                    continue

                try:
                    self.records[i][key] = SpreadsheetDataProcessor.converter[self.field_type[key]](self.records[i][key])

                except ValueError:
                    self.invalid_type.append((i, key))

    def __calculate_summary(self):
        while True:
            field_name = input("Enter the field for which you want to calculate average and total : ").strip()
            if field_name not in self.fields:
                print("Please enter correct field name")
            elif self.field_type[field_name] not in ("int", "float"):
                print("Please enter the field which have numeric values")
            else:
                break

        total = 0
        cnt = 0
        for i in range(len(self.records)):
            if ((i, field_name) in self.invalid_type) or ((i, field_name) in self.missing):
                continue
            else:
                total += self.records[i][field_name]
                cnt += 1
        try:
            self.summary[field_name] = {"Total" : total, "Average" : total/cnt}
        except ZeroDivisionError:
            self.summary[field_name] = {"Total" : total, "Average" : 0}
        except Exception as e:
            print(e)
        print("Calculated summary")

    def __filter_records(self):
        while True:
            field_name = input("Enter the field name for filteration : ").strip()
            if field_name not in self.fields:
                print("Enter correct field name")
            else:
                break

        filtered_record = []
        while True:
            value = input("Enter the value for filteration : ")
            try:
                value = self.converter[self.field_type[field_name]](value)
                break

            except ValueError:
                print(f"Selected field for filteration is {field_name} and its data type is {self.field_type[field_name]} so provide the value of correct data type")

        for record in self.records:
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
        self.report.append(["VALIDATION"])
        self.report.append(["Missing Values", len(self.missing)])
        self.report.append(["Invalid Values", len(self.invalid_type)])
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
            except:
                print("Enter a valid path")

    def process_spreadsheet(self):
        self.__load_spreadsheet()
        if not self.__read_records():
            return
        self.__validate_data()
        choice = 1
        while choice:
            try:
                choice = int(input("Press\n1 for Calculate summary\n2 for Filter records\n3 for Create report\n4 for Exit\n"))
            except ValueError:
                print("Please enter from 1 to 4")
                continue
            if choice == 1:
                self.__calculate_summary()
            elif choice == 2:
                self.__filter_records()
            elif choice == 3:
                self.__create_report()
                self.__save_spreadsheet()
            elif choice == 4:
                break
            else:
                print("Please enter from 1 to 4")
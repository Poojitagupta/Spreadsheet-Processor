def handle_invalid_data(converter, data_type, field_name, missing, invalid, records):
    problematic_rows = set(invalid + missing)
    if invalid or missing:
        choice = input("What do you want to do?\n1. Ignore these rows\n2. Replace the invalid/missing values only for calculation purpose\n3. Cancel calculation\nEnter your choice: ").strip()
        if choice == "1":
            return problematic_rows, records
        if choice == "3":
            print("Calculation cancelled.")
            return None, records
        elif choice == "2":
            problematic_rows = set(missing + invalid)
            while True:
                replacement = input(f"Enter the replacement value for {field_name}: ").strip()
                try:
                    replacement = converter[data_type](replacement)
                    break
                except ValueError:
                    print("Invalid value for the selected data type.")
                    print("Please enter a valid value.")
                
            for row in problematic_rows:
                records[row][field_name] = replacement
                
            return set(), records
        else:
            print("Invalid choice.")
            return None, records
    return set(), records
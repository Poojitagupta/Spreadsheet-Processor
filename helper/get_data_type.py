def get_data_type(field, converter):
    print(f"Enter the following for data type of {field} : ")
    print("1. string\n2. int\n3. float\n4. date\n5. datetime\n6. boolean")
    for i in range(5):
        data_type = input(f"Enter the data type of {field} : ").strip()
        if data_type in converter:
            return data_type
        if i == 3:
            print("This is your last chance, enter the correct choice otherwise the application will terminate!")
        elif i == 4:
            print("Terminating the application...")
            return None
        else:
            print("Enter from the given options only")
    return None
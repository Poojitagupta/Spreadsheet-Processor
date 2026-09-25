from helper.search import search

def get_field_name(fields):
    while True:
        #we can also add the loop based limiting logic here
        field_name = input("Enter the field name : ").strip()
        matched_columns = search(field_name, fields)
        if len(matched_columns) == 0:
            print("No matches found")
        else:
            break
        
    while True:
        #we can also add the loop based limiting logic here
        print(matched_columns)
        choice = input("Enter the number for the filed name which is required : ")
        if not choice.isdigit():
            print("Please enter from the displayed numbers : ")
        elif int(choice) > len(matched_columns) or int(choice) < 1:
            print("Please enter from the displayed numbers : ")
        else:
            field_name = matched_columns[int(choice)]
            break
    return field_name
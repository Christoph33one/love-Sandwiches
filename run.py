import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# first funtion to get sales data from the user as a string

def get_sales_data():
    """
    get sales figures from the user.
    run a while loop to collect a vaild string of data from the user
    via the terminal, which must be a string of 6 numbers
    by commas.the loop will repeatedly request data, until it is valid.
    """
    while True:
        print("please enter sales data from last market")
        print("data should be six numbers, separated be commas.")
        print("example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:") 

        sales_data = data_str.split(",")  
        # split(",") seperate values in the list.

        if validate_data(sales_data):
            print("Data is valid")
            break # stops loop if no Errors. (print(True))

    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into intergers.
    Raises ValueError if string cannot be converted into intergers,
    or if there are not 6 values.
    """
# try statement lets you test for Errors in a blocl of code, 
# Here an if statement is added.
    try: 
        [int(value) for value in values] # validates data into intergers
        if len(values) != 6: # if list length is not equal to 6.
            raise ValueError( # raises custom Error message.
                f"Exactly 6 values requried, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again./n")
        return False
    
    return True

# This is how to refactor code!

# def update_sales_worksheet(data):
#     """
#     Update worksheet, this adds a new row with the list of data provided.
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales") # adding data to the google sheets sales sheet.
#     sales_worksheet.append_row(data) # append adds more to list

# def update_surplus_worksheet(data): #dffdgfghgfhjhgjhgjgh
#     """
#     Update surplus worksheet, this adds a new row with the list of data provided.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus") # adding data to the google sales sheet.
#     surplus_worksheet.append_row(data) # append adds more to list
#     print("Updated surplus worksheet successfully,\n")

def update_worksheet(data, worksheet):
    """
    Recieves a list of intergers to be inserted into a worksheet
    Update the relevent worksheet with the data provided. 
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

    
def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calcutate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - positive surplus indicates waste
    - negative surplus indicates exta is made when stock is sold
    """
    print("Calculating_surplus_date...\n")
    stock = SHEET.worksheet("stock").get_all_values() # to get values from stock data in google sheets
    stock_row = stock[-1]
    
    surplus_data = [] # calculating the surplus data by using the sales and stock data.
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales # return data as int and not a string(default)
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():  
    """
    Collects collumns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data 
    as a list of lists. 
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1, 7): # removes 0 from the list of 6. now list is 1 to 6.
        column = sales.col_values(ind)
        columns.append(column[-5:]) # [] slicing from list to list, use :
   
    return columns

def calculate_stock_data(data):
    """
    Calculate the avaerage stock for eacj item type, adding 10%.
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    
    for columnn in data: # using a For loop to calculate the average from each column of data
        int_column = [int(num) for num in columnn] # coverting colums data into numbers (intergers)
        average= sum(int_column) / len(int_column) # divide int_column by its own lenght to get an average.
        stock_num = average * 1.1 # adding 10% to stock. Because additional stock results in better sales. 
        new_stock_data.append(round(stock_num)) # append is to add an extra piece of data.

    return(new_stock_data)


def main():
    """
    Run all program functions
    """
    # calls first function to get sales data from the terminal.
    data = get_sales_data()
    sales_data = [int(num) for num in data] # change from a string into an interger (int)
    update_worksheet(sales_data, "sales")
    # calling function and passing the sales_data variable .
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    

print("Welcome to love sandwiches data automation")
main()


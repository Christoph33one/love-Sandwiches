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

def update_sales_worksheet(data):
    """
    Update worksheet, this adds a new row with the list of data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales") # adding data to the google sheets sales sheet.
    sales_worksheet.append_row(data) # append adds more to list
    
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
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def main():
    """
    Run all program functions
    """
    # calls first function to get sales data from the terminal.
    data = get_sales_data()
    sales_data = [int(num) for num in data] # change from a string into an interger (int)
    update_sales_worksheet(sales_data)
    # calling function and passing the sales_data variable .
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

print("Welcome to love sandwiches data automation")
main()


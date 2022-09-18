import gspread
from google.oauth2.service_account import Credentials

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
    get sales figures from the user
    """
    while True:
        print("please enter sales data from last market")
        print("data should be six numbers, seperated be commas.")
        print("example: 10,20,30,40,50,60\n")

    # data_str function for data as a string. 
    # print data_str back to the termial to check its value. 
    # (always print functions to test it works!) 
        data_str = input("Enter your data here:") 

        sales_data = data_str.split(",")  # split(",") seperate values in the list.

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
        [int(value) for value in values]
        if len(values) != 6: # if list length is not equal to 6.
            raise ValueError( # raises custom Error message.
                f"Exactly 6 values requried, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again./n")
        return False

    return True

# calls first function to get sales data from the terminal.
data = get_sales_data()

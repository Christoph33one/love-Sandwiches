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

# first funtion to get sales data from the user
def get_sales_data():
    """
    get sales figures from the user
    """
    print("please enter sales data from last market")
    print("data should be six numbers, seperated be commas.")
    print("example: 10,20,30,40,50,60\n")

    # data_str function for data as a string. 
    # print data_str back to the termial to check its value. (always print fucntions to test it works!)
    data_str = input("Enter your data here:")
    print(f"The data provided id {data_str}")

# calls first function to get sales data from the terminal.
get_sales_data()

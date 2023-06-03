#if you don't have 'tkinter library' install it using this command
# ----> python -m tkinter
# ----> pip install --upgrade tkinter



import tkinter as tk
import pyodbc
from PIL import ImageTk, Image
import datetime


# Database connection details
server = 'FARAH\SQLEXPRESS'
database = 'BankSystem'
driver = 'SQL Server'
trusted_connection = 'yes'

# Create a connection string
conn_str = f'Driver={{{driver}}};Server={server};Database={database};Trusted_Connection={trusted_connection}'


# Main window
def show_main_window():
    window = tk.Tk()
    window.title("Bank System")
    window.geometry("800x600")  
    
    try:
        image = Image.open("img2.jpg")
        
        # Resize the image to your desired dimensions
        width = 1600
        height = 1000
        resized_image = image.resize((width, height), Image.ANTIALIAS)

        background_image = ImageTk.PhotoImage(resized_image)

        # Create a label with the image as the background
        background_label = tk.Label(window, image=background_image)
        background_label.image = background_image  # Keep a reference to the image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except IOError as e:
        print(f"Error loading image: {e}")
        
    authenticate_label = tk.Label(window, text="Authenticate as", font=("Arial", 50),bg= "pink")
    authenticate_label.pack()
    
    
    button_frame = tk.Frame(window, bg="white")
    button_frame.pack(pady=50)

    customer_button = tk.Button(window, text="Customer", command=show_customer_window, font=("Arial", 30),width= 9, bg = "pink")
    customer_button.pack()
    
    employee_button = tk.Button(window, text="Employee", command=show_Employee_window, font=("Arial", 30),width= 9, bg = "pink")
    employee_button.pack()
    
    admin_button = tk.Button(window, text="Admin", command=show_Admin_window, font=("Arial", 30), width= 9, bg = "pink")
    admin_button.pack() 

# Customer window
def show_customer_window():
    window = tk.Tk()
    window.title("Customer")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    
    word_label = tk.Label(window, text="Hello! Please sign up or sign in to continue.", font=("Arial", 30))
    word_label.pack()
    
    sign_up_button = tk.Button(window, text="Sign Up", command=show_sign_up_window, font=("Arial", 40),width= 9)
    sign_up_button.pack()

    sign_in_button = tk.Button(window, text="Sign In", command=show_sign_in_window, font=("Arial", 40),width= 9)
    sign_in_button.pack()
    

# Sign Up window
def show_sign_up_window():
    window = tk.Tk()
    window.title("Sign Up")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    entry_font = ("Arial", 12)
    Font = ("Arial",14)
    
    word_label = tk.Label(window, text="Fill out the following form to create a new account.", font=("Arial", 20))
    word_label.pack()
    
    name_label = tk.Label(window, text="Name:", font = Font,bg = "pink")
    name_label.pack()
    name_entry = tk.Entry(window,font=entry_font)
    name_entry.pack()

    password_label = tk.Label(window, text="Password:", font = Font,bg = "pink")
    password_label.pack()
    password_entry = tk.Entry(window, show="*",font=entry_font)
    password_entry.pack()

    phone_label = tk.Label(window, text="Phone:",font = Font,bg = "pink")
    phone_label.pack()
    phone_entry = tk.Entry(window,font=entry_font)
    phone_entry.pack()

    state_label = tk.Label(window, text="State:",font = Font,bg = "pink")
    state_label.pack()
    state_entry = tk.Entry(window,font=entry_font)
    state_entry.pack()

    zip_code_label = tk.Label(window, text="Zip Code:",font = Font,bg = "pink")
    zip_code_label.pack()
    zip_code_entry = tk.Entry(window, font=entry_font)
    zip_code_entry.pack()

    street_label = tk.Label(window, text="Street:",font = Font,bg = "pink")
    street_label.pack()
    street_entry = tk.Entry(window, font=entry_font)
    street_entry.pack()

    city_label = tk.Label(window, text="City:",font = Font,bg = "pink")
    city_label.pack()
    city_entry = tk.Entry(window, font=entry_font)
    city_entry.pack()

    submit_button = tk.Button(window, text="Submit", command=lambda: save_customer( name_entry.get(), password_entry.get(),
                                                                                   phone_entry.get(), state_entry.get(), zip_code_entry.get(),
                                                                                   street_entry.get(), city_entry.get()), font = Font,bg = "pink")
    submit_button.pack()
    
 # Connect to the database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Save customer details to the database
def save_customer(name, password, phone, state, zip_code, street, city):
    cursor.execute("INSERT INTO Customer VALUES ( ?, ?, ?, ?, ?, ?, ?)",
              (name, password, phone, state, zip_code, street, city))
    
    cursor.execute("SELECT SNN FROM Customer WHERE Name=?", (name,))
    customer_id = cursor.fetchone()[0]
    
    id_window = tk.Tk()
    id_window.title("Customer ID")
    
    id_label = tk.Label(id_window, text="Your ID is: " + str(customer_id), font=("Arial", 20))
    id_label.pack()
    
    show_customer_dashboard()
    

# Sign In window
def show_sign_in_window():
    window = tk.Tk()
    window.title("Sign In")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    entry_font = ("Arial", 12)
    Font = ("Arial",14)
    
    word_label = tk.Label(window, text="Please enter your login credentials to access your account.", font = Font)
    word_label.pack()
    
    snn_label = tk.Label(window, text="User ID:",font = Font,bg = "pink")
    snn_label.pack()
    snn_entry = tk.Entry(window,  font=entry_font)
    snn_entry.pack()

    password_label = tk.Label(window, text="Password:", font = Font,bg = "pink")
    password_label.pack()
    password_entry = tk.Entry(window, show="*", font=entry_font)
    password_entry.pack()

    sign_in_button = tk.Button(window, text="Sign In", command=lambda: authenticate_customer(snn_entry.get(), password_entry.get()), font = Font,bg = "pink")
    sign_in_button.pack()


# Authenticate customer from the database
def authenticate_customer(snn, password):
    cursor.execute("SELECT * FROM Customer WHERE SNN=? AND Password=?", (snn, password))
    if cursor.fetchone() is not None:
        show_customer_dashboard()
    else:
        window = tk.Tk()
        window.title("Error message")
        incorrect_label = tk.Label(window, text="Incorrect ID or password, please try again.")
        incorrect_label.pack()
        

# Customer dashboard
def show_customer_dashboard():
    window = tk.Toplevel()
    window.title("Customer Dashboard")
    window.geometry("800x600") 
    window.configure(bg = "#301934")

    # Bank selection
    bank_label = tk.Label(window, text="Bank Name:", bg = "pink",width=11)
    bank_label.pack()
    bank_options = get_bank_names()  # Get the list of available bank names from the database
    bank_var = tk.StringVar(window)
    bank_var.set(bank_options[0])  # Set the default bank option
    bank_dropdown = tk.OptionMenu(window, bank_var, *bank_options)
    bank_dropdown.pack()

    # Branch selection
    branch_label = tk.Label(window, text="Branch Name:",bg = "pink", width = 11)
    branch_label.pack()
    branch_options = get_branches()  # Get the list of available bank names from the database
    branch_var = tk.StringVar(window)
    branch_var.set(branch_options[0])  # Set the default bank option
    branch_dropdown = tk.OptionMenu(window, branch_var, *branch_options)
    branch_dropdown.pack()

     # Loans selection
    loan_label = tk.Label(window, text="View Loans list:",bg = "pink",width=11)
    loan_label.pack()
    loan_options = get_loan()  # Get the list of available bank names from the database
    loan_var = tk.StringVar(window)
    loan_var.set(loan_options[0])  # Set the default bank option
    loan_dropdown = tk.OptionMenu(window, loan_var, * loan_options)
    loan_dropdown.pack()
    
    word_label = tk.Label(window, text="To show you Balance please enter your id first.",bg = "pink")
    word_label.pack()
    
    balance_button = tk.Button(window, text="Show Balance", command=lambda: show_balance(snn_entry.get()))
    balance_button.pack()
   
    snn_label = tk.Label(window, text="User ID:",bg = "pink")
    snn_label.pack()
    snn_entry = tk.Entry(window)
    snn_entry.pack()
    
    
    request_button = tk.Button(window, text="Loan Request", command=lambda: show_request_loan())
    request_button.pack()

def show_request_loan():
    
    # Create GUI elements
    window = tk.Toplevel()
    window.title("Loan Request")
    
    customer_id_label = tk.Label(window, text="Customer ID:")
    customer_id_label.pack()
    customer_id_entry = tk.Entry(window)
    customer_id_entry.pack()

    loan_amount_label = tk.Label(window, text="Loan Amount:")
    loan_amount_label.pack()
    loan_amount_entry = tk.Entry(window)
    loan_amount_entry.pack()
    
    Type_loan_label = tk.Label(window, text="Loan Type:")
    Type_loan_label.pack()
    Type_loan_entry = tk.Entry(window)
    Type_loan_entry.pack()
    
    Type1_loan_label = tk.Label(window, text="Loan_No:")
    Type1_loan_label.pack()
    Type1_loan_entry = tk.Entry(window)
    Type1_loan_entry.pack()
    
    def submit_loan_request():
        customer_id = customer_id_entry.get()
        loan_amount = loan_amount_entry.get()
        Type_loan = Type_loan_entry.get()
        loan_No = Type1_loan_entry.get()
        authenticate_request( loan_amount, Type_loan,loan_No, customer_id)

    submit_button = tk.Button(window, text="Submit", command=submit_loan_request)
    submit_button.pack()
    
def authenticate_request( loan_amount, Type_loan,loan_No, customer_id):
    
     # Check user balance
    cursor.execute("SELECT Balance FROM Account WHERE SNN= ?", (customer_id,))
 
    row = cursor.fetchone()

        
    window = tk.Toplevel()
    window.title("Message")

    message_label = tk.Label(window)
    message_label.pack()
    message_label.config(text="Loan request submitted successfully!")
                
    cursor.execute("INSERT INTO Loan (Amount, Type,loan_No,SNN) VALUES (?, ?,?,?)", ( loan_amount, Type_loan,loan_No, customer_id))
    conn.commit()
    

# Get the list of available bank names from the database
def get_bank_names():
    cursor.execute("SELECT Name FROM Bank")
    return [row.Name for row in cursor.fetchall()]

def get_branches():
    cursor.execute("SELECT branch_name FROM Branch")
    return [row.branch_name for row in cursor.fetchall()]

def get_loan():
    cursor.execute("SELECT distinct Type FROM Loan")
    return [row.Type for row in cursor.fetchall()]

def show_balance(snn):
    window = tk.Toplevel()
    cursor.execute("SELECT Balance FROM Account WHERE SNN=?", (snn))
    balance = cursor.fetchone()
    if balance is not None:
        balance_label = tk.Label(window, text=f"Balance: {balance[0]}", font=("Arial", 18))
        balance_label.pack()
    else:
        balance_label = tk.Label(window, text="No balance found for the customer.")
        balance_label.pack()
        
#-----------------------------------------------------------------------------------------------
#--------------------------------Admin---------------------------------------------------------------
#-----------------------------------------------------------------------------------------------


# Admin window
def show_Admin_window():
    window = tk.Tk()
    window.title("Admin")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    
    word_label = tk.Label(window, text="Hello! Please sign in to continue.", font=("Arial", 30))
    word_label.pack()
    
    signIn_button = tk.Button(window, text="sgin in", command=show_Asign_in_window, font=("Arial", 40),width= 9)
    signIn_button.pack() 
    
 
   
# admin Sign In window
def show_Asign_in_window():
    window = tk.Tk()
    window.title("Sign In")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    entry_font = ("Arial", 12)
    Font = ("Arial",14)
    
    word_label = tk.Label(window, text="Please enter your login credentials to access your account.", font = Font)
    word_label.pack()
    
    id_label = tk.Label(window, text="ID:",font = Font,bg = "pink")
    id_label.pack()
    id_entry = tk.Entry(window,  font=entry_font)
    id_entry.pack()

    password_label = tk.Label(window, text="Password:", font = Font,bg = "pink")
    password_label.pack()
    password_entry = tk.Entry(window, show="*", font=entry_font)
    password_entry.pack()

    sign_in_button = tk.Button(window, text="Sign In", command=lambda: authenticate_Admin(id_entry.get(), password_entry.get()), font = Font,bg = "pink")
    sign_in_button.pack() 
    
# Authenticate customer from the database
def authenticate_Admin(id, password):
    cursor.execute("SELECT * FROM Admin WHERE AdminId=? AND password=?", (id, password))
    if cursor.fetchone() is not None:
        show_Admin_dashboard()
    else:
        window = tk.Tk()
        window.title("Error message")
        incorrect_label = tk.Label(window, text="Incorrect ID or password, please try again.")
        incorrect_label.pack()
               


# Admin dashboard
def show_Admin_dashboard():
    window = tk.Tk()
    window.title("Admin Dashboard")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    
    word_label = tk.Label(window, text="Hello! Please enter the operation you want to do.", font=("Arial", 30))
    word_label.pack()
    
    Add_Bank_button = tk.Button(window, text="Add Bank", command=show_Add_Bank_window, font=("Arial", 30), width = 30)
    Add_Bank_button.pack()

    sign_in_button = tk.Button(window, text="Add Branch", command=show_Add_Branch_window, font=("Arial", 30),width=30)
    sign_in_button.pack()
    
    sign_in_button = tk.Button(window, text="show Customer Details", command=show_Customer_Details, font=("Arial", 30),width = 30)
    sign_in_button.pack()
    
    sign_in_button = tk.Button(window, text="show loan list with customer and employee", command=show_Loan_With_Customer, font=("Arial", 20),width = 43)
    sign_in_button.pack()

    sign_in_button = tk.Button(window, text="Generate Rport", command=generate_Report, font=("Arial", 30),width = 30)
    sign_in_button.pack()


# Generate report with system information
def generate_Report():
    window = tk.Toplevel()
    window.title("System Report")


    cursor.execute("SELECT COUNT(*) FROM Employee")
    num_Employee = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Customer")
    num_Customer = cursor.fetchone()[0]
    
    num_Customer_with_loan = cursor.execute("SELECT COUNT(loan_No) from Loan , Customer where Customer.SNN = Loan.SNN")
    num_Customer_with_loan = cursor.fetchone()[0]
    
    num_OfBranch_eachBank = cursor.execute("SELECT COUNT(branch_No),Bank.Name from Bank , Branch  where Bank.Code = Branch.Code GROUP BY Bank.Name")
    result = cursor.fetchall()
    
    cursor.execute("SELECT Type, Amount, COUNT(*) AS num_loans FROM Loan GROUP BY Type, Amount")
    loan_data = cursor.fetchall()
    
    #new_information = "Some new information you want to display."

    # Create report text
    report_text = f"System Report\n\n"
    report_text += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report_text += f"Number of Employees: {num_Employee}\n"
    report_text += f"Number of Customers: {num_Customer}\n"
    report_text += f"Number of branch per Bank:\n\n"
    #report_text += f"New Information:\n{new_information}"

    for row in result:
        num_branches = row[0]
        bank_name = row[1]
        report_text += f"{bank_name}: {num_branches} branches\n"
        
    report_text += f"The number of customers who have loans: {num_Customer_with_loan}\n"    

    report_text += "Loan Information:\n"

    for loan in loan_data:
        loan_type = loan[0]
        loan_amount = loan[1]
        num_loans = loan[2]
        report_text += f"Type: {loan_type}, Amount: {loan_amount}, Number of Loans: {num_loans}\n"


    report_label = tk.Label(window, text=report_text, font=("Arial", 14))
    report_label.pack()


# Add Bank window
def show_Add_Bank_window():
    window = tk.Tk()
    window.title("Add Bank")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    entry_font = ("Arial", 12)
    Font = ("Arial",14)
    
    word_label = tk.Label(window, text="Fill out the following form to create a new Bank.", font=("Arial", 20))
    word_label.pack()
    
    code_label = tk.Label(window, text="Code:", font = Font,bg = "pink")
    code_label.pack()
    code_entry = tk.Entry(window,font=entry_font)
    code_entry.pack()

    name_label = tk.Label(window, text="Name:", font = Font,bg = "pink")
    name_label.pack()
    name_entry = tk.Entry(window,font=entry_font)
    name_entry.pack()
    
    zip_label = tk.Label(window, text="zip_code:", font = Font,bg = "pink")
    zip_label.pack()
    zip_entry = tk.Entry(window,font=entry_font)
    zip_entry.pack()
    
    state_label = tk.Label(window, text="State:", font = Font,bg = "pink")
    state_label.pack()
    state_entry = tk.Entry(window,font=entry_font)
    state_entry.pack()
    
    city_label = tk.Label(window, text="Coty:", font = Font,bg = "pink")
    city_label.pack()
    city_entry = tk.Entry(window,font=entry_font)
    city_entry.pack()
    
    street_label = tk.Label(window, text="Street:", font = Font,bg = "pink")
    street_label.pack()
    street_entry = tk.Entry(window,font=entry_font)
    street_entry.pack()


    submit_button = tk.Button(window, text="Submit", command=lambda: save_Add_Bank( code_entry.get(), name_entry.get(),
                                                                                   zip_entry.get(), state_entry.get(),
                                                                                   city_entry.get(),street_entry.get(),font = Font),bg = "pink")
    submit_button.pack()

 # Connect to the database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


# Add Branch window
def show_Add_Branch_window():
    window = tk.Tk()
    window.title("Add Branch")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    entry_font = ("Arial", 12)
    Font = ("Arial",14)
    
    word_label = tk.Label(window, text="Fill out the following form to create a new Branch.", font=("Arial", 20))
    word_label.pack()
    
    pNumber_label = tk.Label(window, text="branch Number:", font = Font,bg = "pink")
    pNumber_label.pack()
    pNumber_entry = tk.Entry(window,font=entry_font)
    pNumber_entry.pack()

    city_label = tk.Label(window, text="City:", font = Font,bg = "pink")
    city_label.pack()
    city_entry = tk.Entry(window,font=entry_font)
    city_entry.pack()
    
    state_label = tk.Label(window, text="state:", font = Font,bg = "pink")
    state_label.pack()
    state_entry = tk.Entry(window,font=entry_font)
    state_entry.pack()
    
    zip_label = tk.Label(window, text="Zip Code:", font = Font,bg = "pink")
    zip_label.pack()
    zip_entry = tk.Entry(window,font=entry_font)
    zip_entry.pack()
    
    street_label = tk.Label(window, text="Street:", font = Font,bg = "pink")
    street_label.pack()
    street_entry = tk.Entry(window,font=entry_font)
    street_entry.pack()
    
    code_label = tk.Label(window, text="Code:", font = Font,bg = "pink")
    code_label.pack()
    code_entry = tk.Entry(window,font=entry_font)
    code_entry.pack()
    
    pName_label = tk.Label(window, text="Branch Name:", font = Font,bg = "pink")
    pName_label.pack()
    pName_entry = tk.Entry(window,font=entry_font)
    pName_entry.pack()
    
    submit_button = tk.Button(window, text="Submit", command=lambda: save_Add_Branch( pNumber_entry.get(), city_entry.get(),
                                                                                    state_entry.get(), zip_entry.get(),
                                                                                    street_entry.get(),code_entry.get(),
                                                                                    pName_entry.get(), font = Font),bg = "pink")
    submit_button.pack()

 # Connect to the database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()



# Save Bank details to the database
def save_Add_Bank(Code, Name, zip_code, state, city, street):
    cursor.execute("INSERT INTO Bank VALUES ( ?, ?, ?, ?, ?, ?)",
                (Code, Name, zip_code, state, city, street))
    conn.commit()
    conn.close()

# Save Branch details to the database
def save_Add_Branch(pNumber, city, state, zip_code, street, code, pName):
    cursor.execute("INSERT INTO Branch VALUES ( ?, ?, ?, ?, ?, ?, ?)",
                (pNumber, city,state, zip_code, street, code, pName))
    conn.commit()
    conn.close()


def show_Customer_Details():
    window = tk.Toplevel()
    cursor.execute("SELECT SNN, Name, Phone, State, Zip_Code, Street, City FROM Customer")
    details = cursor.fetchall()
    if details:
        for customer in details:
            customer_label = tk.Label(window, text=f"SNN: {customer[0]}, Name: {customer[1]}, Phone: {customer[2]}, State: {customer[3]}, Zip Code: {customer[4]}, Street: {customer[5]}, City: {customer[6]}",font = 16)
            customer_label.pack()
    else:
        no_details_label = tk.Label(window, text="No customer details found.")
        no_details_label.pack()
        

def show_Loan_With_Customer(): 
    window = tk.Toplevel()  
    cursor.execute("select Amount, Type, Customer.Name ,Employee.Name from Loan, Customer, Employee where Loan.SNN=Customer.SNN AND Loan.SNN = Employee.empid")
    details = cursor.fetchall()
    if details:
        for customer in details:
            customer_label = tk.Label(window, text=f"Amount: {customer[0]}, Type: {customer[1]},customer Name: {customer[2]}, Emplyee Name: {customer[3]}",font = 16)
            customer_label.pack()
    else:
        no_details_label = tk.Label(window, text="No customer details found.")
        no_details_label.pack()     


#--------------------------------------------------------------------------------------------------------
#-----------------------------------------------Employee-------------------------------------------------
#--------------------------------------------------------------------------------------------------------

# Employee window
def show_Employee_window():
    window = tk.Tk()
    window.title("Employee")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    
    
    word_label = tk.Label(window, text="Hello! Please sign up or sign in to continue.", font=("Arial", 30))
    word_label.pack()
    
    sign_up_button = tk.Button(window, text="Sign Up", command=show_Esign_up_window, font=("Arial", 40),width= 9)
    sign_up_button.pack()
    
    sign_in_button = tk.Button(window, text="sgin in", command=show_Esign_in_window, font=("Arial", 40),width= 9)
    sign_in_button.pack() 

    
# Sign Up window
def show_Esign_up_window():
    window = tk.Tk()
    window.title("Sign Up")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    entry_font = ("Arial", 12)
    Font = ("Arial",14)
    
    word_label = tk.Label(window, text="Fill out the following form to create a new account.", font=("Arial", 20))
    word_label.pack()
    
    name_label = tk.Label(window, text="Name:", font = Font,bg = "pink")
    name_label.pack()
    name_entry = tk.Entry(window,font=entry_font)
    name_entry.pack()

    password_label = tk.Label(window, text="Password:", font = Font,bg = "pink")
    password_label.pack()
    password_entry = tk.Entry(window, show="*",font=entry_font)
    password_entry.pack()

    phone_label = tk.Label(window, text="Phone:",font = Font,bg = "pink")
    phone_label.pack()
    phone_entry = tk.Entry(window,font=entry_font)
    phone_entry.pack()

    state_label = tk.Label(window, text="State:",font = Font,bg = "pink")
    state_label.pack()
    state_entry = tk.Entry(window,font=entry_font)
    state_entry.pack()

    zip_code_label = tk.Label(window, text="Zip Code:",font = Font,bg = "pink")
    zip_code_label.pack()
    zip_code_entry = tk.Entry(window, font=entry_font)
    zip_code_entry.pack()

    street_label = tk.Label(window, text="Street:",font = Font,bg = "pink")
    street_label.pack()
    street_entry = tk.Entry(window, font=entry_font)
    street_entry.pack()

    city_label = tk.Label(window, text="City:",font = Font,bg = "pink")
    city_label.pack()
    city_entry = tk.Entry(window, font=entry_font)
    city_entry.pack()

    submit_button = tk.Button(window, text="Submit", command=lambda: save_Employee( name_entry.get(), password_entry.get(),
                                                                                   phone_entry.get(), state_entry.get(), zip_code_entry.get(),
                                                                                   street_entry.get(), city_entry.get()), font = Font,bg = "pink")
    submit_button.pack()
    

    #window.mainloop()
    
 # Connect to the database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Save Employee details to the database
def save_Employee(name, password, phone, state, zip_code, street, city):
    cursor.execute("INSERT INTO Customer VALUES ( ?, ?, ?, ?, ?, ?, ?)",
              (name, password, phone, state, zip_code, street, city))
    conn.commit()
    conn.close()
    show_Employee_dashboard()




# Sign In window
def show_Esign_in_window():
    window = tk.Tk()
    window.title("Sign In")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    entry_font = ("Arial", 12)
    Font = ("Arial",14)
    
    word_label = tk.Label(window, text="Please enter your login credentials to access your account.", font = Font)
    word_label.pack()
    
    empId_label = tk.Label(window, text="Employee ID:",font = Font, bg = "pink")
    empId_label.pack()
    empId_entry = tk.Entry(window,  font=entry_font)
    empId_entry.pack()

    password_label = tk.Label(window, text="Password:", font = Font,bg = "pink")
    password_label.pack()
    password_entry = tk.Entry(window, show="*", font=entry_font)
    password_entry.pack()

    sign_in_button = tk.Button(window, text="Sign In", command=lambda: authenticate_Employee(empId_entry.get(), password_entry.get()), font = Font,bg = "pink")
    sign_in_button.pack()

# Authenticate customer from the database
def authenticate_Employee(empId, password):
    cursor.execute("SELECT * FROM Employee WHERE EmpId=? AND Password=?", (empId, password))
    if cursor.fetchone() is not None:
        show_Employee_dashboard()
    else:
        window = tk.Tk()
        window.title("Error message")
        incorrect_label = tk.Label(window, text="Incorrect ID or password, please try again.")
        incorrect_label.pack()


# Employee dashboard
def show_Employee_dashboard():
    window = tk.Tk()
    window.title("Employee Dashboard")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    
    word_label = tk.Label(window, text="Hello! Please enter the operation you want to do.", font=("Arial", 30))
    word_label.pack()
    
    Add_cust_button = tk.Button(window, text="Add Customer", command=show_Add_Customer_window, font=("Arial", 30),width = 22)
    Add_cust_button.pack()
    
    sign_in_button = tk.Button(window, text="show Loan List", command=show_Loans_List_Details, font=("Arial", 30),width = 22)
    sign_in_button.pack()
    
    
    update_button = tk.Button(window, text="Update User Data", command=show_Update_User_Data, font=("Arial", 30),width = 22)
    update_button.pack()

# Add Customer window
def show_Update_User_Data():
    window = tk.Tk()
    window.title("Update User Data")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    entry_font = ("Arial", 12)
    Font = ("Arial",14)
    
    word_label = tk.Label(window, text="Fill out the following form to update the user data.", font=("Arial", 20))
    word_label.pack()
    
    name_label = tk.Label(window, text="Name:", font = Font,bg = "pink")
    name_label.pack()
    name_entry = tk.Entry(window,font=entry_font)
    name_entry.pack()

    password_label = tk.Label(window, text="Password:", font = Font,bg = "pink")
    password_label.pack()
    password_entry = tk.Entry(window, show="*",font=entry_font)
    password_entry.pack()

    phone_label = tk.Label(window, text="Phone:",font = Font,bg = "pink")
    phone_label.pack()
    phone_entry = tk.Entry(window,font=entry_font)
    phone_entry.pack()

    state_label = tk.Label(window, text="State:",font = Font,bg = "pink")
    state_label.pack()
    state_entry = tk.Entry(window,font=entry_font)
    state_entry.pack()

    street_label = tk.Label(window, text="Street:",font = Font,bg = "pink")
    street_label.pack()
    street_entry = tk.Entry(window, font=entry_font)
    street_entry.pack()

    city_label = tk.Label(window, text="City:",font = Font,bg = "pink")
    city_label.pack()
    city_entry = tk.Entry(window, font=entry_font)
    city_entry.pack()

    submit_button = tk.Button(window, text="Submit", command=lambda: Update_User_data( name_entry.get(), password_entry.get(),
                                                                                   phone_entry.get(), state_entry.get(),
                                                                                   street_entry.get(), city_entry.get()), font = Font,bg = "pink")
    submit_button.pack()
    
 # Connect to the database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


# Save update customer details to the database
def Update_User_data(name, password, phone, state, street, city):
    cursor.execute("""
        UPDATE Customer
        SET Name = ?,
            Password = ?,
            Phone = ?,
            State = ?,
            Street = ?,
            City = ?
        """, (name, password, phone, state, street, city))
    conn.commit()
    conn.close()

# Add Customer window
def show_Add_Customer_window():
    window = tk.Tk()
    window.title("Add Customer")
    window.geometry("800x600") 
    window.configure(bg = "#301934")
    entry_font = ("Arial", 12)
    Font = ("Arial",14)
    
    word_label = tk.Label(window, text="Fill out the following form to create a new Customer.", font=("Arial", 20))
    word_label.pack()
    
    name_label = tk.Label(window, text="Name:", font = Font,bg = "pink")
    name_label.pack()
    name_entry = tk.Entry(window,font=entry_font)
    name_entry.pack()

    password_label = tk.Label(window, text="Password:", font = Font,bg = "pink")
    password_label.pack()
    password_entry = tk.Entry(window, show="*",font=entry_font)
    password_entry.pack()

    phone_label = tk.Label(window, text="Phone:",font = Font,bg = "pink")
    phone_label.pack()
    phone_entry = tk.Entry(window,font=entry_font)
    phone_entry.pack()

    state_label = tk.Label(window, text="State:",font = Font,bg = "pink")
    state_label.pack()
    state_entry = tk.Entry(window,font=entry_font)
    state_entry.pack()

    zip_code_label = tk.Label(window, text="Zip Code:",font = Font,bg = "pink")
    zip_code_label.pack()
    zip_code_entry = tk.Entry(window, font=entry_font)
    zip_code_entry.pack()

    street_label = tk.Label(window, text="Street:",font = Font,bg = "pink")
    street_label.pack()
    street_entry = tk.Entry(window, font=entry_font)
    street_entry.pack()

    city_label = tk.Label(window, text="City:",font = Font,bg = "pink")
    city_label.pack()
    city_entry = tk.Entry(window, font=entry_font)
    city_entry.pack()

    submit_button = tk.Button(window, text="Submit", command=lambda: save_customer( name_entry.get(), password_entry.get(),
                                                                                   phone_entry.get(), state_entry.get(), zip_code_entry.get(),
                                                                                   street_entry.get(), city_entry.get()), font = Font,bg = "pink")
    submit_button.pack()
    
 # Connect to the database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


def show_Loans_List_Details():
    window = tk.Toplevel()
    cursor.execute("SELECT Amount,Type , loan_No, branch_No from Loan")
    details = cursor.fetchall()
    if details:
        for loan in details:
            loan_label = tk.Label(window, text=f"Amount: {loan[0]}, Type: {loan[1]}, loan_No: {loan[2]}, branch_No: {loan[3]}", font = ("Aria", 16))
            loan_label.pack()
    else:
        no_details_label = tk.Label(window, text="No customer details found.")
        no_details_label.pack()


# Start the program
show_main_window()

tk.mainloop()
# Close the database connection
conn.close()

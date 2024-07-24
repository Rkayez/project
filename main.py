import pandas as pd  
import streamlit as st
import bankfunc as bank
import re
from bankfunc import Bank, BankAccount

csv_file = 'user_data.csv'

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'register' not in st.session_state:
    st.session_state.register = 0
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False
if 'jawnabehi' not in st.session_state:
    st.session_state.jawnabehi = False



def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        bank.operation.login(username, password)
        result = bank.operation.login(username, password)
        if result == 1:
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        elif result == -1:
            st.error("Invalid username or password")
        elif result == 0:
            st.error("Debugged")

def main_page():
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    st.sidebar.title("Dashboard")
    if 'balance' not in st.session_state:
        username = st.session_state.username
        bank = BankAccount(username)
        balance1 = bank.balance1(csv_file)
        bop = BankAccount(username, balance1)
        st.session_state.balance = bop.balance1(csv_file)
    page = st.sidebar.radio("Go to", ["Home", "Deposit", "Withdraw", "Transfer"])
    if page == "Home":
        username = st.session_state.username
        bank = BankAccount(username)
        balance1 = bank.balance1(csv_file)
        bop = BankAccount(username, balance1)
        st.session_state.balance = bop.balance1(csv_file)
        b = Bank(username)
        b.load_user_data()
        st.session_state.balance = bop.balance1(csv_file)
        st.title("GoMyBank")
        st.header(f"Current Balance: ${st.session_state.balance}")

    elif page == "Deposit":
        st.title("Deposit Funds")
        deposit_amount = st.number_input("Amount to deposit", min_value=1.0, step=10.0)
        if st.button("Deposit"):
            username = st.session_state.username
            df = pd.read_csv(csv_file) 
            if username in df['Username'].values:
                cash = df.loc[df['Username'] == username, 'Cash'].values[0]
                bop = BankAccount(username)
                csv = 'user_data.csv'
                balance = bop.balance1(csv)
                result = bop.deposit(deposit_amount, balance, cash)
                result
                if not result == -1:
                    st.success(f"${deposit_amount} deposited successfully!")
                    user = st.session_state.username
                    b = Bank(user)
                    b.load_user_data()
                    df = pd.read_csv(csv_file)

                    balance1, cash1 = result
        
                    if user in df['Username'].values:
                        df.loc[df['Username'] == user, 'Balance'] = balance1
                        df.to_csv(csv_file, index=False)
                        print(f"Balance for {user} updated to {balance1}.")
                    else:
                        print(f"Username {user} not found in the CSV file.")
                    if username in df['Username'].values:
                        df.loc[df['Username'] == user, 'Cash'] = cash1
                        df.to_csv(csv_file, index=False)
                        print(f"Cash balance for {user} updated to {cash1}.")
                    else:
                        print(f"Username {user} not found in the CSV file.")

                elif result == -1:
                    st.error(f"you don't have the following amount ${deposit_amount}.")
            else:
                return f"Username {username} not found in the CSV file."
            
    elif page == "Withdraw":
        st.title("Withdraw Funds")
        withdraw_amount = st.number_input("Amount to withdraw", min_value=1.0, step=10.0)
        if st.button("Withdraw"):
            username = st.session_state.username
            df = pd.read_csv(csv_file) 
            if username in df['Username'].values:
                cash = df.loc[df['Username'] == username, 'Cash'].values[0]
                bop = BankAccount(username)
                csv = 'user_data.csv'
                balance = bop.balance1(csv)
                result = bop.withdraw(withdraw_amount, balance, cash)
                if not result == -1:
                    st.success(f"${withdraw_amount} withdrawn successfully!")
                    user = st.session_state.username
                    b = Bank(user)
                    b.load_user_data()
                    df = pd.read_csv(csv_file)

                    balance1, cash1 = result
        
                    if user in df['Username'].values:
                        df.loc[df['Username'] == user, 'Balance'] = balance1
                        df.to_csv(csv_file, index=False)
                        print(f"Balance for {user} updated to {balance1}.")
                    else:
                        print(f"Username {user} not found in the CSV file.")
                    if username in df['Username'].values:
                        df.loc[df['Username'] == user, 'Cash'] = cash1
                        df.to_csv(csv_file, index=False)
                        print(f"Cash balance for {user} updated to {cash1}.")
                    else:
                        print(f"Username {user} not found in the CSV file.")

                elif result == -1:
                    st.error(f"you don't have the following amount ${withdraw_amount}.")
            else:
                return f"Username {username} not found in the CSV file."
        
    if page == "Transfer":
        st.title("Transfer Funds")
        ribreceiver = st.text_input("The RIB Of The Receiver")
        transferamount = st.number_input("Amount to Transfer", min_value=1.0, step=10.0)
        
        if st.button("Transfer"):
            user = st.session_state.username
            balance = st.session_state.balance
            bop = BankAccount(user)
            balance1, balance= bop.transfer(ribreceiver, balance, transferamount)

            if balance1 != -1:
                st.success(f"${transferamount} successfully transferred to {ribreceiver}!")
                
                # Update the DataFrame and write to CSV
                df = pd.read_csv('user_data.csv')
                df['RIB'] = df['RIB'].astype(str)
                user = st.session_state.username
                
                if ribreceiver in df['RIB'].values:
                    df.loc[df['RIB'] == ribreceiver, 'Balance'] = balance1
                    df.to_csv('user_data.csv', index=False)  # Save changes to CSV
                    print(f"Balance for {ribreceiver} updated to {balance1}.")
                else:
                    st.error(f"Receiver with the username {user} not found in the CSV.")
                if user in df['Username'].values:
                    df.loc[df['Username'] == user, 'Balance'] = balance
                    df.to_csv('user_data.csv', index=False)  # Save changes to CSV
                    print(f"Balance for the user {user} updated to {balance}.")
                else:
                    st.error(f"Receiver with user {user} not found in the CSV.")
            else:
                st.error(f"Failed to transfer ${transferamount} to {ribreceiver}.")
    if st.sidebar.button("Logout"):
        logout()

def register_page():
    page = st.sidebar.radio("Select", ["Register", "Login"])
    if page == "Register":
        st.title("Register")
        username = st.text_input("Username")
        email = st.text_input("Email")
        firstname = st.text_input("First Name")
        lastname = st.text_input("Last Name")
        password = st.text_input("Password", type="password")
        confirmpassword = st.text_input("Confirm Password", type="password")
        if not re.match("^[A-Za-z]+$", username):
            st.error("Username must contain only letters.")
        if not re.match("^[A-Za-z]+$", firstname):
            st.error("First Name must contain only letters.")
        if not re.match("^[A-Za-z]+$", lastname):
            st.error("Last Name must contain only letters.")
        if st.button("Register"):
            st.session_state.button_clicked = True
            Bank.register(username, firstname, lastname, email, password, confirmpassword)
            result = Bank.register(username, firstname, lastname, email, password, confirmpassword)  
            print(result)
            if result == -1:
                st.error("User already exists")
            else:
                st.success("Registration successful!")

    elif page == "Login":
        login_page()

if not st.session_state.logged_in:
    register_page()
else:
    main_page()

##if st.session_state.registerbut == 1:
    ##register_page()
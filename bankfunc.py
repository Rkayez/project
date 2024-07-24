import pandas as pd  
import csv
import random
default = 0

class Bank:
  def __init__(self, current_user=None, transactions_file='transactions.csv'):
    self.transactions_file = transactions_file
    self.user_data_file = 'user_data.csv'
    self.current_user = current_user
    self.load_user_data()

  def load_user_data(self):
    self.user_data = {}
    try:
      with open(self.user_data_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
          email = row['Email']
          username = row['Username']
          balance = row['Balance']
          self.user_data[email] = row 
          self.user_data[username] = row 
          self.user_data[balance] = row 
    except FileNotFoundError:
      with open(self.user_data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "First Name", "Second Name", "Email", "Password", "Balance"])

  def login(self, username, password):
      if "@" in username:
         email = username
         if email.lower() in self.user_data and self.user_data[email.lower()]['Password'].lower() == password.lower():
          return 1
         else:
          return -1
      else:
         if username.lower() in self.user_data and self.user_data[username.lower()]['Password'].lower() == password.lower():
          return 1
         else:
           return -1

  def register(username, first_name, second_name, email, password, confirmpassword):
        df = pd.read_csv('user_data.csv')   

        if email not in df['Email'].values and username not in df['Username'].values:
            if password == confirmpassword:
              data="user_data.csv"
              RIB = random.randint(111111111,999999999)
              with open(data, 'a', newline='') as file:  
                  writer = csv.writer(file)
                  writer.writerow([username, first_name, second_name, email, password, default, RIB, default])
              return 1
        else:
          print("Error.")
          return -1
  
class BankAccount:
    def __init__(self, name, balance=0, cash=0):
        self.name = name
        self.balance = balance
        self.cash = cash
        self.transactions = pd.DataFrame(columns=['Transaction', 'Amount', 'Balance'])
    
    def balance1(self, csv_file):
      df = pd.read_csv(csv_file)

      # Ensure 'Username' column exists
      if 'Username' not in df.columns:
          raise ValueError("'Username' column not found in the DataFrame")

      # Clean up 'Username' column
      df['Username'] = df['Username'].str.strip()

      # Convert username to lowercase for case-insensitive 
      username = self.name
      username = username.lower()

      # Debugging: Print out usernames and the search term
      print("Usernames in DataFrame (lowercase):", df['Username'].str.lower().tolist())
      print("Searching for username:", username)

      # Check if the username exists
      if username in df['Username'].str.lower().values:
          # Filter rows to find the username
          user_row = df[df['Username'].str.lower() == username]
          
          # Debugging: Print the filtered rows
          print("Filtered rows:\n", user_row)

          # Assuming there's only one row per username
          if not user_row.empty:
              # Get the balance
              balance_column = 'Balance'
              if balance_column in df.columns:
                  balance = user_row[balance_column].values[0]
                  return balance
              else:
                  raise ValueError(f"'{balance_column}' column not found in the DataFrame")
          else:
              return "Username not found1"  # Should not reach here based on previous check
      else:
          return "Username not found2"
    
    def deposit(self, amount, balance, cash):
        if cash >= amount:
            cash -= amount
            balance += amount
            new_transaction = pd.DataFrame([{'Transaction': 'Withdraw', 'Amount': amount, 'Balance': self.balance}])
            new_transaction_cleaned = new_transaction.dropna(axis=1, how='all')
            self.transactions = pd.concat([self.transactions, new_transaction_cleaned], ignore_index=True)
            return balance, cash;
        elif balance >= amount:
            return -1
        else:
            return -1
    
    def withdraw(self, amount, balance, cash):
        if balance >= amount:
            balance -= amount
            cash += amount
            new_transaction = pd.DataFrame([{'Transaction': 'Withdraw', 'Amount': amount, 'Balance': balance}])
            new_transaction_cleaned = new_transaction.dropna(axis=1, how='all')
            self.transactions = pd.concat([self.transactions, new_transaction_cleaned], ignore_index=True)
            return balance, cash;
        elif balance <= amount:
            return -1;
    def transfer(self, ribreceiver, balance, balancerib):
        df = pd.read_csv('user_data.csv')
        df['RIB'] = df['RIB'].astype(str)
        
        if ribreceiver in df['RIB'].values:
            rib_details = df.loc[df['RIB'] == ribreceiver]
            print(f"The RIB {ribreceiver} was found successfully.")
            print(rib_details)
            
            if balance >= balancerib:
                balance -= balancerib
                
                # Ensure that balance1 is a scalar
                balance1 = df.loc[df['RIB'] == ribreceiver, 'Balance'].values[0]
                print(f"Balance of {ribreceiver} is {balance1}.")
                
                balance1 += balancerib
                
                # Update the balance in DataFrame
                df.loc[df['RIB'] == ribreceiver, 'Balance'] = balance1
                
                # Create new transaction record
                new_transaction = pd.DataFrame([{'Transaction': 'Deposit', 'Amount': balancerib, 'Balance': balance1}])
                self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)
                
                # Save changes to CSV
                df.to_csv('user_data.csv', index=False)
                
                return balance1, balance
            else:
                return -1  # Not enough balance
        else:
            return -1  # RIB not found
        
    
operation = Bank()

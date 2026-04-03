# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 13:53:06 2025

@author: Zen
"""

class CustomerAccount:
    def __init__(self, fname, lname, address, account_no, balance, flag):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.account_no = account_no
        self.balance = float(balance)
        self.flag = flag
    
    def update_first_name(self, fname):
        self.fname = fname
    
    def update_last_name(self, lname):
        self.lname = lname
                
    def get_first_name(self):
        return self.fname
    
    def get_last_name(self):
        return self.lname
        
    def update_address(self, addr):
        self.address = addr
        
    def get_address(self):
        return self.address
    
    def deposit(self, amount):
        self.balance +=amount
        
    def withdraw(self, amount):
        self.balance -= amount
        
    def print_balance(self):
        print("\n The account balance is %.2f" %self.balance)
        
    def get_balance(self):
        return self.balance
    
    def get_account_no(self):
        return self.account_no
    
    def update_flag(self, flag):
        self.flag = flag
    
    def account_menu(self):
        print ("\n Your Transaction Options Are:")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Deposit money")
        print ("2) Withdraw money")
        print ("3) Check balance")
        print ("4) Update customer name")
        print ("5) Update customer address")
        print ("6) Show customer details")
        print ("7) Back")
        print (" ")
        option = int(input ("Choose your option: "))
        return option
    
    def print_details(self):
        print("Account Type: %s" %type(self).__name__) # Fetch account type based on class name
        print("First name : %s" %self.fname)
        print("Last name : %s" %self.lname)
        print("Account No : %s" %self.account_no)
        print("Address : %s" %self.address[0])
        print("          %s" %self.address[1])
        print("          %s" %self.address[2])
        print(" ")
   
    def run_account_options(self):
        loop = 1
        while loop == 1:
            choice = self.account_menu()
            if choice == 1:
                amount = float(input("\n Please enter amount to be deposited : "))
                self.deposit(amount)
                self.print_balance()
            elif choice == 2:
                amount = float(input("\n Please enter amount to be withdrawn : "))
                self.withdraw(amount)
                self.print_balance()
            elif choice == 3:
                 self.print_balance()
            elif choice == 4:
                fname = input("\n Enter new customer first name : ")
                self.update_first_name(fname)
                sname = input("\n Enter new customer last name : ")
                self.update_last_name(sname)
            elif choice == 5:
                address = input("\n Enter new customer address : ")
                self.update_address(address)
            elif choice == 6:
                self.print_details()
            elif choice == 7:
                loop = 0
        print ("\n Exit account operations")
        
    def return_flag(self):
        return self.flag       
        
class SavingsAccount(CustomerAccount):
        def __init__(self, fname, lname, address, account_no, balance, flag, interest_rate):
            super().__init__(fname, lname, address, account_no, balance, flag) #Inheritance from CustomerAccount superclass
            
            self.interest_rate = interest_rate
            
        def get_interest(self):
            return self.interest_rate
            
        def apply_interest(self):
            self.balance += self.balance * (self.interest_rate / 100)
            print(f"\n Interest applied! New balance : {self.balance: .2f}")
            
        def print_details(self):
            super().print_details() 
            print(f"Interest Rate : {self.interest_rate}%")

class CurrentAccount(CustomerAccount):
    def __init__(self, fname, lname, address, account_no, balance, flag, overdraft_limit):
        super().__init__(fname, lname, address, account_no, balance, flag)
        self.overdraft_limit = overdraft_limit
        
    def withdraw(self, amount):
        if amount <= self.balance + self.overdraft_limit:
            self.balance -= amount 
            print(f"\n Withdrawal successful! New balance : {self.balance: .2f}")
        else:
            print("\n Withdrawl failed! Overdraft limit exceeded.")
            
    def get_overdraft(self):
        return self.overdraft_limit
    
    def print_details(self):
        super().print_details()
        print(f"Overdraft Limit: {self.overdraft_limit}")
        
        
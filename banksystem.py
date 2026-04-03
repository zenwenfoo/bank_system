# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 13:51:49 2025

@author: Zen
"""

from admin import Admin
from customer_account import SavingsAccount
from customer_account import CurrentAccount

import re

import tkinter
import tkinter.font
import tkinter.messagebox

accounts_list = []
admins_list = []

class BankSystem(object):
    def __init__(self):               #Initialise bank system
        self.accounts_list = []       #Empty array
        self.admins_list = []         #Empty array
        self.current_admin = None     #Track Current admin
        self.load_bank_data()
        
    def load_bank_data(self):         #Load bank account data from text file
        try: 
            with open("bank_account_database.txt", "r") as file:
                for line in file:
                    data = line.strip().split(", ")
                    if data[0] == "SAVINGS":
                        first_name, last_name, address, account_no, balance, flag, interest_rate = (data[1], data[2], data[3:-4], int(data[-4]), float(data[-3]), data[-2], float(data[-1]))
                        customer = SavingsAccount(first_name, last_name, address, account_no, balance, flag, interest_rate)
                        self.accounts_list.append(customer)
                    elif data[0] == "CURRENT":
                        first_name, last_name, address, account_no, balance, flag, overdraft_limit = (data[1], data[2], data[3:-4], int(data[-4]), float(data[-3]), data[-2], float(data[-1]))
                        customer = CurrentAccount(first_name, last_name, address, account_no, balance, flag, overdraft_limit)
                        self.accounts_list.append(customer)
                    elif data[0] == "ADMIN":
                        first_name, last_name, address, user_name, password, is_superuser = data[1], data[2], data[3:-3], data[-3], data[-2], data[-1] == "True"
                        admin = Admin(first_name, last_name, address, user_name, password, is_superuser)
                        self.admins_list.append(admin)
        except FileNotFoundError:
               print("Error: The file 'bank_data.txt' does not exist!")
               
    def save_bank_data(self):         #Save bank account data to text file
        try:
            with open("bank_account_database.txt", "w") as file:
                 for account in self.accounts_list:
                     if isinstance(account, SavingsAccount):
                        file.write(f"SAVINGS, {account.get_first_name()}, {account.get_last_name()}, {', '.join(account.get_address())}, "
                                   f"{account.get_account_no()}, {account.get_balance():.2f}, {account.return_flag()}, {account.interest_rate}\n")
                     elif isinstance(account, CurrentAccount):
                         file.write(f"CURRENT, {account.get_first_name()}, {account.get_last_name()}, {', '.join(account.get_address())}, "
                                    f"{account.get_account_no()}, {account.get_balance():.2f}, {account.return_flag()}, {account.overdraft_limit}\n")
                 for admin in self.admins_list:
                     file.write(f"ADMIN, {admin.fname}, {admin.lname}, {', '.join(admin.address)}, {admin.user_name}, {admin.password}, {admin.full_admin_rights}\n")
            print("Bank account data saved successfully")
        except Exception as e:
            print(f"Error saving bank data: {e}")
               
    #Tkinter Pages
    def main_menu(self):              #Welcome Screen
        #Window Creation
        self.mw = tkinter.Tk()
        self.mw.title("Python Bank System")
        self.mw.geometry("300x200")
        self.mw.resizable(False, False) #Disable window resizing
        self.mw.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.mw)
        self.bot_frame = tkinter.Frame(self.mw)
        
        #Widgets
        self.wl_mm_1 = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.wl_mm_2 = tkinter.Label(self.top_frame, text = "Welcome to the Python Bank System")
        self.wl_mm_3 = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.mm_option1 = tkinter.Button(self.bot_frame, text = "Admin Login", command = self.admin_login , width = 10, bg = "Red", fg = "white", cursor = "hand2", relief = "flat")
        self.mm_option1.bind("<Enter>", self.on_hover)
        self.mm_option1.bind("<Leave>", self.on_leave)
        self.mm_option2 = tkinter.Button(self.bot_frame, text = "Quit", command = self.mw.destroy, width = 10, bg = "Red", fg = "white", cursor = "hand2", relief = "flat")
        self.mm_option2.bind("<Enter>", self.on_hover)
        self.mm_option2.bind("<Leave>", self.on_leave)
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.bot_frame.pack()
        
        self.wl_mm_1.pack(side = "top")
        self.wl_mm_2.pack(side = "top")
        self.wl_mm_3.pack(side = "top")
        self.mm_option1.pack(side = "top", pady = 5)
        self.mm_option2.pack(side = "top", pady = 5)
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.wl_mm_1.configure(font = cf)
        self.wl_mm_2.configure(font = cf)
        self.wl_mm_3.configure(font = cf)
        self.mm_option1.configure(font = cf)
        self.mm_option2.configure(font = cf)
        
        tkinter.mainloop()
       
    def admin_login(self):            #Admin Login Screen (-u -p)
        self.mw.destroy()
        
        #Window Creation
        self.al = tkinter.Tk()
        self.al.title("Admin Login")
        self.al.geometry("300x250")
        self.al.resizable(False, False) #Disable window resizing
        self.al.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.al)
        self.mid_frame1 = tkinter.Frame(self.al)
        self.mid_frame2 = tkinter.Frame(self.al)
        self.bot_frame = tkinter.Frame(self.al)
        self.bot_frame2 = tkinter.Frame(self.al)
        
        #Widgets
        self.wl_al_1 = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~~~~")
        self.wl_al_2 = tkinter.Label(self.top_frame, text = "Python Bank System")
        self.wl_al_3 = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~~~~")
        self.admin_label1 = tkinter.Label(self.mid_frame1, text = "Please input username : ")
        self.username_entry = tkinter.Entry(self.mid_frame1, width = 10, relief = "flat", highlightthickness = 2)
        self.admin_label2 = tkinter.Label(self.mid_frame2, text = "Please input password : ")
        self.password_entry = tkinter.Entry(self.mid_frame2, width = 10, relief = "flat", highlightthickness = 2)
        self.login_button = tkinter.Button(self.bot_frame, text = "Login", command = self.run_admin_login, bg = "Red", fg = "White", cursor = "hand2", relief = "flat", width = 10, height = 1)
        self.login_button.bind("<Enter>", self.on_hover)
        self.login_button.bind("<Leave>", self.on_leave)
        self.lab_var = tkinter.StringVar()
        self.al_warning_label = tkinter.Label(self.bot_frame2, textvariable = self.lab_var, fg = "red")
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.mid_frame1.pack()
        self.mid_frame2.pack()
        self.bot_frame.pack()
        self.bot_frame2.pack()
        
        self.wl_al_1.pack(side = "top")
        self.wl_al_2.pack(side = "top")
        self.wl_al_3.pack(side = "top")
        self.admin_label1.pack(side = "left", pady = 10)
        self.username_entry.pack(side = "left", pady = 10)
        self.admin_label2.pack(side = "left", pady = 10)
        self.password_entry.pack(side = "left", pady = 10)
        self.login_button.pack(side = "top")
        self.al_warning_label.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.wl_al_1.configure(font = cf)
        self.wl_al_2.configure(font = cf)
        self.wl_al_3.configure(font = cf)
        self.admin_label1.configure(font = cf)
        self.username_entry.configure(font = cf)
        self.admin_label2.configure(font = cf)
        self.password_entry.configure(font = cf)
        self.al_warning_label.configure(font = cf)
        
        #ENTER Key Functionality
        self.al.bind("<Return>", self.run_admin_login)
    
    def admin_menu(self):     #Admin Main Menu Operations Screen
        #Window Creation
        self.am = tkinter.Tk()
        self.am.title("Admin Menu")
        self.am.geometry("350x330")
        self.am.resizable(False, False) #Disable window resizing
        self.am.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.am)
        self.mid_frame = tkinter.Frame(self.am)
        
        #Admin Update
        admin_fname, admin_lname = self.current_admin.get_first_name(), self.current_admin.get_last_name()
        is_superuser = self.current_admin.has_full_admin_right()
        
        #Widgets
        self.wl_am_1 = tkinter.Label(self.top_frame, text = f"Welcome Admin {admin_fname} {admin_lname}")
        self.wl_am_2 = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.am_option1 = tkinter.Button(self.mid_frame, text = "Transfer Money", bg = "Red", fg = "White", cursor = "hand2", relief = "flat", width = 36, height = 1, command = self.load_admin_option1, state="normal" if is_superuser else "disabled")
        self.am_option2 = tkinter.Button(self.mid_frame, text = "Customer account operations & profile settings", bg = "Red", fg = "White", cursor = "hand2", relief = "flat", width = 36, height = 1, command = self.load_admin_option2)
        self.am_option3 = tkinter.Button(self.mid_frame, text = "Delete Customer", bg = "Red", fg = "White", cursor = "hand2", relief = "flat", width = 36, height = 1, command = self.load_admin_option3, state="normal" if is_superuser else "disabled")
        self.am_option4 = tkinter.Button(self.mid_frame, text = "Print All Customer Details", bg = "Red", fg = "White", cursor = "hand2", relief = "flat", width = 36, height = 1, command = self.load_admin_option4)
        self.am_option5 = tkinter.Button(self.mid_frame, text = "Update Name", bg = "Red", fg = "White", cursor = "hand2", relief = "flat", width = 36, height = 1, command = self.load_admin_option5)
        self.am_option6 = tkinter.Button(self.mid_frame, text = "Update Address", bg = "Red", fg = "White", cursor = "hand2", relief = "flat", width = 36, height = 1, command = self.load_admin_option6)
        self.am_option7 = tkinter.Button(self.mid_frame, text = "Sign Out", bg = "Red", fg = "White", cursor = "hand2", relief = "flat", width = 36, height = 1, command = lambda: self.go_back(self.am, self.main_menu))
        
        self.am_option1.bind("<Enter>", self.on_hover)
        self.am_option1.bind("<Leave>", self.on_leave)
        self.am_option2.bind("<Enter>", self.on_hover)
        self.am_option2.bind("<Leave>", self.on_leave)
        self.am_option3.bind("<Enter>", self.on_hover)
        self.am_option3.bind("<Leave>", self.on_leave)
        self.am_option4.bind("<Enter>", self.on_hover)
        self.am_option4.bind("<Leave>", self.on_leave)
        self.am_option5.bind("<Enter>", self.on_hover)
        self.am_option5.bind("<Leave>", self.on_leave)
        self.am_option6.bind("<Enter>", self.on_hover)
        self.am_option6.bind("<Leave>", self.on_leave)
        self.am_option7.bind("<Enter>", self.on_hover)
        self.am_option7.bind("<Leave>", self.on_leave)
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.mid_frame.pack()
        
        self.wl_am_1.pack(side = "top")
        self.wl_am_2.pack(side = "top")
        self.am_option1.pack(side = "top", pady = 1)
        self.am_option2.pack(side = "top", pady = 1)
        self.am_option3.pack(side = "top", pady = 1)
        self.am_option4.pack(side = "top", pady = 1)
        self.am_option5.pack(side = "top", pady = 1)
        self.am_option6.pack(side = "top", pady = 1)
        self.am_option7.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        cf2 = tkinter.font.Font(family = "Calibri", size = 11)
        self.wl_am_1.configure(font = cf)
        self.wl_am_2.configure(font = cf)
        self.am_option1.configure(font = cf2)
        self.am_option2.configure(font = cf2)
        self.am_option3.configure(font = cf2)
        self.am_option4.configure(font = cf2)
        self.am_option5.configure(font = cf2)
        self.am_option6.configure(font = cf2)
        self.am_option7.configure(font = cf2)
    
    def admin_option1(self):  #Transfer Money
        #Window Creation
        self.o1 = tkinter.Tk()
        self.o1.title("Transfer Money")
        self.o1.geometry("300x300")
        self.o1.resizable(False, False) #Disable window resizing 
        self.o1.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.o1)
        self.mid_frame1 = tkinter.Frame(self.o1)
        self.mid_frame2 = tkinter.Frame(self.o1)
        self.mid_frame3 = tkinter.Frame(self.o1)
        self.bot_frame = tkinter.Frame(self.o1)
        self.bot_frame2 = tkinter.Frame(self.o1)
        
        self.o1.grid_columnconfigure(0, weight = 1)
        
        #Widgets
        self.o1_title = tkinter.Label(self.top_frame, text = "Transfer")
        self.o1_title_design = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~~~~~")
        self.o1_sender_acc = tkinter.Label(self.mid_frame1, text = "Sender Account/No : ")
        self.o1_sender_acc_input = tkinter.Entry(self.mid_frame1, width = 10, relief = "flat", highlightthickness = 2)
        self.o1_receiver_acc = tkinter.Label(self.mid_frame2, text = "Receiver Account/No: ")
        self.o1_receiver_acc_input = tkinter.Entry(self.mid_frame2, width = 10, relief = "flat", highlightthickness = 2)
        self.o1_amount_transfer = tkinter.Label(self.mid_frame3, text = "Input Amount : ")
        self.o1_amount_transfer_input = tkinter.Entry(self.mid_frame3, width = 10, relief = "flat", highlightthickness = 2)
        self.o1_submit_button = tkinter.Button(self.bot_frame, text = "Submit", bg = "Red", fg = "White", cursor = "hand2", relief = "flat", width = 10, height = 1, command = self.run_admin_option1)
        self.o1_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.o1, self.admin_menu))
        
        self.o1_submit_button.bind("<Enter>", self.on_hover)
        self.o1_submit_button.bind("<Leave>", self.on_leave)
        self.o1_back.bind("<Enter>", self.on_hover)
        self.o1_back.bind("<Leave>", self.on_leave)
        
        self.o1_lab_var = tkinter.StringVar()
        self.o1_label = tkinter.Label(self.bot_frame2, textvariable = self.o1_lab_var, fg = "red")
        
        #Positioning
        self.top_frame.grid(row = 0, column = 0, pady = 5)
        self.mid_frame1.grid(row = 1, column = 0, padx = 2, pady = 5, sticky = "w")
        self.mid_frame2.grid(row = 2, column = 0, padx = 2, pady = 5, sticky = "w")
        self.mid_frame3.grid(row = 3, column = 0, padx = 2, pady = 5, sticky = "w")
        self.bot_frame.grid(row = 4, column = 0, pady = 10)
        self.bot_frame2.grid(row = 5, column = 0, pady = 10)
        
        self.o1_title.grid(row = 0, column = 0)
        self.o1_title_design.grid(row = 1, column = 0)
        self.o1_sender_acc.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = 5)
        self.o1_sender_acc_input.grid(row = 0, column = 1, padx = 10, pady = 5)
        self.o1_receiver_acc.grid(row = 1, column = 0, sticky = "w", padx = 10, pady = 5)
        self.o1_receiver_acc_input.grid(row = 1, column = 1, pady = 5)
        self.o1_amount_transfer.grid(row = 2, column = 0, sticky = "w", padx = 10, pady = 5)
        self.o1_amount_transfer_input.grid(row = 2, column = 1, padx = 48, pady = 5)
        self.o1_submit_button.grid(row = 3, column = 0, padx = 5)
        self.o1_back.grid(row = 3, column = 1, padx = 5)
        self.o1_label.grid(row = 4, column = 0)
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.o1_title.configure(font = cf)
        self.o1_title_design.configure(font = cf)
        self.o1_sender_acc.configure(font = cf)
        self.o1_sender_acc_input.configure(font = cf)
        self.o1_receiver_acc.configure(font = cf)
        self.o1_receiver_acc_input.configure(font = cf)
        self.o1_amount_transfer.configure(font = cf)
        self.o1_amount_transfer_input.configure(font = cf)
        self.o1_submit_button.configure(font = cf)
        self.o1_back.configure(font = cf)
        self.o1_label.configure(font = cf)
        
        #ENTER Key Functionality
        self.o1.bind("<Return>", self.run_admin_option1)
        
    def admin_option2(self):          #Customer Operations
        #Window Creation
        self.o2 = tkinter.Tk()
        self.o2.title("Customer account operations & profile settings")
        self.o2.geometry("300x160")
        self.o2.resizable(False, False) #Disable window resizing
        self.o2.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.o2)
        self.mid_frame = tkinter.Frame(self.o2)
        self.bot_frame = tkinter.Frame(self.o2)
        self.bot_frame2 = tkinter.Frame(self.o2)
        
        #Widgets
        self.o2_title = tkinter.Label(self.top_frame, text = "Search for Customer...")
        self.o2_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~~~~~~~~~~")
        self.o2_prompt = tkinter.Label(self.mid_frame, text = "Enter Customer Acc/No : ")
        self.o2_input = tkinter.Entry(self.mid_frame, width = 10, relief = "flat", highlightthickness = 2)
        self.o2_submit = tkinter.Button(self.bot_frame, text = "Submit", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = self.run_admin_option2)
        
        self.o2_submit.bind("<Enter>", self.on_hover)
        self.o2_submit.bind("<Leave>", self.on_leave)
        
        self.o2_lab_var = tkinter.StringVar()
        self.o2_label = tkinter.Label(self.bot_frame2, textvariable = self.o2_lab_var, fg = "red")
        
        #Positioning
        self.top_frame.pack()
        self.mid_frame.pack(pady = 2)
        self.bot_frame.pack(pady = 5)
        self.bot_frame2.pack()
        
        self.o2_title.pack(side = "top")
        self.o2_title_deco.pack(side = "top")
        self.o2_prompt.pack(side = "left")
        self.o2_input.pack(side = "left")
        self.o2_submit.pack(side = "top")
        self.o2_label.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.o2_title.configure(font = cf)
        self.o2_title_deco.configure(font = cf)
        self.o2_prompt.configure(font = cf)
        self.o2_input.configure(font = cf)
        self.o2_submit.configure(font = cf)
        self.o2_label.configure(font = cf)
        
        #ENTER Key Functionality
        self.o2.bind("<Return>", self.run_admin_option2)
        
    def admin_option3(self):  #Delete Customer
        #Window Creation
        self.o3 = tkinter.Tk()
        self.o3.title("Customer Deletion")
        self.o3.geometry("300x190")
        self.o3.resizable(False, False) #Disable window resizing
        self.o3.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.o3)
        self.mid_frame = tkinter.Frame(self.o3)
        self.bot_frame = tkinter.Frame(self.o3)
        self.bot_frame2 = tkinter.Frame(self.o3)
        
        #Widgets
        self.o3_title = tkinter.Label(self.top_frame, text = "Delete a Customer...")
        self.o3_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~~~~~~~~~~")
        self.o3_prompt = tkinter.Label(self.mid_frame, text = "Enter Customer Acc/No : ")
        self.o3_input = tkinter.Entry(self.mid_frame, width = 10, relief = "flat", highlightthickness = 2)
        self.o3_submit = tkinter.Button(self.bot_frame, text = "Submit", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = self.run_admin_option3)
        self.o3_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.o3, self.admin_menu))
        
        self.o3_submit.bind("<Enter>", self.on_hover)
        self.o3_submit.bind("<Leave>", self.on_leave)
        self.o3_back.bind("<Enter>", self.on_hover)
        self.o3_back.bind("<Leave>", self.on_leave)
        
        self.o3_lab_var = tkinter.StringVar()
        self.o3_label = tkinter.Label(self.bot_frame2, textvariable = self.o3_lab_var, fg = "red")
        
        #Positioning
        self.top_frame.pack(pady = 5)
        self.mid_frame.pack(pady = 10)
        self.bot_frame.pack(pady = 5)
        self.bot_frame2.pack(pady = 5)
        
        self.o3_title.pack(side = "top")
        self.o3_title_deco.pack(side = "top")
        self.o3_prompt.pack(side = "left")
        self.o3_input.pack(side = "left")
        self.o3_submit.pack(side = "left", padx = 5)
        self.o3_back.pack(side = "left", padx = 5)
        self.o3_label.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.o3_title.configure(font = cf)
        self.o3_title_deco.configure(font = cf)
        self.o3_prompt.configure(font = cf)
        self.o3_input.configure(font = cf)
        self.o3_submit.configure(font = cf)
        self.o3_back.configure(font = cf)
        self.o3_label.configure(font = cf)
        
    def admin_option4(self, count_cust, sum_balance, total_interest, total_overdraft): #Print Report
        #Window Creation
        self.o4 = tkinter.Tk()
        self.o4.title("Management Report")
        self.o4.geometry("400x220")
        self.o4.resizable(False, False) #Disable window resizing
        self.o4.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.o4)
        self.mid_frame1 = tkinter.Frame(self.o4)
        self.mid_frame2 = tkinter.Frame(self.o4)
        self.mid_frame3 = tkinter.Frame(self.o4)
        self.mid_frame4 = tkinter.Frame(self.o4)
        self.bot_frame = tkinter.Frame(self.o4)
        
        #Widgets
        self.o4_title = tkinter.Label(self.top_frame, text = "Management Report")
        self.o4_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~~~~~~~~~~")
        
        self.o4_total_count = tkinter.Label(self.mid_frame1, text = "Total Count (Of Customers) : ")
        self.o4_lab_var1 = tkinter.StringVar()
        self.o4_lab_var1.set(f"{count_cust}")
        self.o4_label1 = tkinter.Label(self.mid_frame1, textvariable = self.o4_lab_var1, fg = "blue")
        
        self.o4_total_balance = tkinter.Label(self.mid_frame2, text = "Total Balance (Across All Accounts) : ")
        self.o4_lab_var2 = tkinter.StringVar()
        self.o4_lab_var2.set(f"£{sum_balance:.2f}")
        self.o4_label2 = tkinter.Label(self.mid_frame2, textvariable = self.o4_lab_var2, fg = "blue")
        
        self.o4_total_interest = tkinter.Label(self.mid_frame3, text = "Total Interest Payable (This Year) : ")
        self.o4_lab_var3 = tkinter.StringVar()
        self.o4_lab_var3.set(f"£{total_interest:.2f}")
        self.o4_label3 = tkinter.Label(self.mid_frame3, textvariable = self.o4_lab_var3, fg = "blue")
        
        self.o4_total_overdrafts = tkinter.Label(self.mid_frame4, text = "Total Overdrafts (Currently Taken) : ")
        self.o4_lab_var4 = tkinter.StringVar()
        self.o4_lab_var4.set(f"£{total_overdraft:.2f}")
        self.o4_label4 = tkinter.Label(self.mid_frame4, textvariable = self.o4_lab_var4, fg = "blue")
        
        self.o4_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.o4, self.admin_menu))
        self.o4_back.bind("<Enter>", self.on_hover)
        self.o4_back.bind("<Leave>", self.on_leave)
        
        #Positioning
        self.top_frame.pack()
        self.mid_frame1.pack()
        self.mid_frame2.pack()
        self.mid_frame3.pack()
        self.mid_frame4.pack()
        self.bot_frame.pack(pady = 10)
        
        self.o4_title.pack(side = "top")
        self.o4_title_deco.pack(side = "top")
        self.o4_total_count.pack(side = "left")
        self.o4_label1.pack(side = "left")
        self.o4_total_balance.pack(side = "left")
        self.o4_label2.pack(side = "left")
        self.o4_total_interest.pack(side = "left")
        self.o4_label3.pack(side = "left")
        self.o4_total_overdrafts.pack(side = "left")
        self.o4_label4.pack(side = "left")
        self.o4_back.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.o4_title.configure(font = cf)
        self.o4_title_deco.configure(font = cf)
        self.o4_total_count.configure(font = cf)
        self.o4_label1.configure(font = cf)
        self.o4_total_balance.configure(font = cf)
        self.o4_label2.configure(font = cf)
        self.o4_total_interest.configure(font = cf)
        self.o4_label3.configure(font = cf)
        self.o4_total_overdrafts.configure(font = cf)
        self.o4_label4.configure(font = cf)
        self.o4_back.configure(font = cf)
        
    def admin_option5(self): #Update Admin Name
        #Window Creation
        self.o5 = tkinter.Tk()
        self.o5.title("Update Name")
        self.o5.geometry("380x250")
        self.o5.resizable(False, False) #Disable window resizing
        self.o5.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.o5)
        self.mid_frame = tkinter.Frame(self.o5)
        self.mid_frame2 = tkinter.Frame(self.o5)
        self.bot_frame = tkinter.Frame(self.o5)
        self.bot_frame2 = tkinter.Frame(self.o5)
        
        #Widgets
        self.o5_title = tkinter.Label(self.top_frame, text = "Update Name")
        self.o5_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~")
        self.o5_fname_prompt = tkinter.Label(self.mid_frame, text = "Enter New First Name : ")
        self.o5_fname_input = tkinter.Entry(self.mid_frame, width = 10, relief = "flat", highlightthickness = 2)
        self.o5_lname_prompt = tkinter.Label(self.mid_frame2, text = "Enter New Last Name : ")
        self.o5_lname_input = tkinter.Entry(self.mid_frame2, width = 10, relief = "flat", highlightthickness = 2)
        self.o5_submit = tkinter.Button(self.bot_frame, text = "Change", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = self.run_admin_option5)
        self.o5_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.o5, self.admin_menu))
        
        self.o5_submit.bind("<Enter>", self.on_hover)
        self.o5_submit.bind("<Leave>", self.on_leave)
        self.o5_back.bind("<Enter>", self.on_hover)
        self.o5_back.bind("<Leave>", self.on_leave)
        
        self.o5_lab_var = tkinter.StringVar()
        self.o5_label = tkinter.Label(self.bot_frame2, textvariable = self.o5_lab_var, fg = "red")
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.mid_frame.pack(pady = 10)
        self.mid_frame2.pack(pady = 10)
        self.bot_frame.pack(pady = 10)
        self.bot_frame2.pack()
        
        self.o5_title.pack(side = "top")
        self.o5_title_deco.pack(side = "top")
        self.o5_fname_prompt.pack(side = "left")
        self.o5_fname_input.pack(side = "left")
        self.o5_lname_prompt.pack(side = "left")
        self.o5_lname_input.pack(side = "left")
        self.o5_submit.pack(side = "left", padx = 5)
        self.o5_back.pack(side = "left", padx = 5)
        self.o5_label.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.o5_title.configure(font = cf)
        self.o5_title_deco.configure(font = cf)
        self.o5_fname_prompt.configure(font = cf)
        self.o5_fname_input.configure(font = cf)
        self.o5_lname_prompt.configure(font = cf)
        self.o5_lname_input.configure(font = cf)
        self.o5_submit.configure(font = cf)
        self.o5_back.configure(font = cf)
        self.o5_label.configure(font = cf)
        
    def admin_option6(self): #Update Admin Address
        #Window Creation
        self.o6 = tkinter.Tk()
        self.o6.title("Update Address")
        self.o6.geometry("380x200")
        self.o6.resizable(False, False) #Disable window resizing
        self.o6.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.o6)
        self.mid_frame = tkinter.Frame(self.o6)
        self.bot_frame = tkinter.Frame(self.o6)
        self.bot_frame2 = tkinter.Frame(self.o6)
        
        #Widgets
        self.o6_title = tkinter.Label(self.top_frame, text = "Update Address")
        self.o6_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~")
        self.o6_prompt = tkinter.Label(self.mid_frame, text = "Enter New Address")
        self.o6_input = tkinter.Entry(self.mid_frame, width = 10, relief = "flat", highlightthickness = 2)
        self.o6_submit = tkinter.Button(self.bot_frame, text = "Submit", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = self.run_admin_option6)
        self.o6_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.o6, self.admin_menu))
        
        self.o6_submit.bind("<Enter>", self.on_hover)
        self.o6_submit.bind("<Leave>", self.on_leave)
        self.o6_back.bind("<Enter>", self.on_hover)
        self.o6_back.bind("<Leave>", self.on_leave)
        
        self.o6_lab_var = tkinter.StringVar()
        self.o6_label = tkinter.Label(self.bot_frame2, textvariable = self.o6_lab_var, fg = "red")
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.mid_frame.pack(pady = 10)
        self.bot_frame.pack(pady = 10)
        self.bot_frame2.pack()
        
        self.o6_title.pack(side = "top")
        self.o6_title_deco.pack(side = "top")
        self.o6_prompt.pack(side = "left")
        self.o6_input.pack(side = "left")
        self.o6_submit.pack(side = "left", padx = 5)
        self.o6_back.pack(side = "left", padx = 5)
        self.o6_label.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.o6_title.configure(font = cf)
        self.o6_title_deco.configure(font = cf)
        self.o6_prompt.configure(font = cf)
        self.o6_input.configure(font = cf)
        self.o6_submit.configure(font = cf)
        self.o6_back.configure(font = cf)
        self.o6_label.configure(font = cf)
        
    def customer_menu(self, account_no):   #Admin > Customer Account Main Menu Operations Screen
        #Window Creation
        self.co = tkinter.Tk()
        self.co.title("Customer Account Operations")
        self.co.geometry("380x390")
        self.co.resizable(False, False) #Disable window resizing
        self.co.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.frame1 = tkinter.Frame(self.co)
        self.frame2 = tkinter.Frame(self.co)
        
        #Checking Admin Privilege
        is_superuser = self.current_admin.has_full_admin_right()
        
        #Widgets
        self.co_title = tkinter.Label(self.frame1, text = f"Account No : {account_no}")
        self.co_title2 = tkinter.Label(self.frame1, text = "Transactions Options")
        self.co_title_deco = tkinter.Label(self.frame1, text = "~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.co_option1 = tkinter.Button(self.frame2, text = "Deposit Money", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 34, height = 1, command = lambda: self.load_cust_option1(account_no), state="normal" if is_superuser else "disabled")
        self.co_option2 = tkinter.Button(self.frame2, text = "Withdraw Money", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 34, height = 1, command = lambda: self.load_cust_option2(account_no), state="normal" if is_superuser else "disabled")
        self.co_option3 = tkinter.Button(self.frame2, text = "Check Balance", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 34, height = 1, command = lambda: self.load_cust_option3(account_no))
        self.co_option4 = tkinter.Button(self.frame2, text = "Update Name", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 34, height = 1, command = lambda: self.load_cust_option4(account_no), state="normal" if is_superuser else "disabled")
        self.co_option5 = tkinter.Button(self.frame2, text = "Update Address", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 34, height = 1, command = lambda: self.load_cust_option5(account_no), state="normal" if is_superuser else "disabled")
        self.co_option6 = tkinter.Button(self.frame2, text = "Show Details", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 34, height = 1, command = lambda: self.load_cust_option6(account_no))
        self.co_option7 = tkinter.Button(self.frame2, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 34, height = 1, command = lambda: self.go_back(self.co, self.admin_menu))
        
        self.co_option1.bind("<Enter>", self.on_hover)
        self.co_option1.bind("<Leave>", self.on_leave)
        self.co_option2.bind("<Enter>", self.on_hover)
        self.co_option2.bind("<Leave>", self.on_leave)
        self.co_option3.bind("<Enter>", self.on_hover)
        self.co_option3.bind("<Leave>", self.on_leave)
        self.co_option4.bind("<Enter>", self.on_hover)
        self.co_option4.bind("<Leave>", self.on_leave)
        self.co_option5.bind("<Enter>", self.on_hover)
        self.co_option5.bind("<Leave>", self.on_leave)
        self.co_option6.bind("<Enter>", self.on_hover)
        self.co_option6.bind("<Leave>", self.on_leave)
        self.co_option7.bind("<Enter>", self.on_hover)
        self.co_option7.bind("<Leave>", self.on_leave)
        
        #Positioning
        self.frame1.pack(pady = 10)
        self.frame2.pack()
        
        self.co_title.pack(side = "top")
        self.co_title2.pack(side = "top")
        self.co_title_deco.pack(side = "top")
        self.co_option1.pack(side = "top", pady = 1)
        self.co_option2.pack(side = "top", pady = 1)
        self.co_option3.pack(side = "top", pady = 1)
        self.co_option4.pack(side = "top", pady = 1)
        self.co_option5.pack(side = "top", pady = 1)
        self.co_option6.pack(side = "top", pady = 1)
        self.co_option7.pack(side = "top", pady = 30)
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.co_title.configure(font = cf)
        self.co_title2.configure(font = cf)
        self.co_title_deco.configure(font = cf)
        self.co_option1.configure(font = cf)
        self.co_option2.configure(font = cf)
        self.co_option3.configure(font = cf)
        self.co_option4.configure(font = cf)
        self.co_option5.configure(font = cf)
        self.co_option6.configure(font = cf)
        self.co_option7.configure(font = cf)
        
    def cust_option1(self, account_no):    #Deposit
        #Window Creation
        self.co1 = tkinter.Tk()
        self.co1.title("Deposit")
        self.co1.geometry("300x200")
        self.co1.resizable(False, False) #Disable window resizing
        self.co1.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.co1)
        self.mid_frame = tkinter.Frame(self.co1)
        self.bot_frame = tkinter.Frame(self.co1)
        self.bot_frame2 = tkinter.Frame(self.co1)
        
        #Widgets
        self.co1_title = tkinter.Label(self.top_frame, text = "Deposit")
        self.co1_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~")
        self.co1_prompt = tkinter.Label(self.mid_frame, text = "Enter Deposit Amount : ")
        self.co1_input = tkinter.Entry(self.mid_frame, width = 10, relief = "flat", highlightthickness = 2)
        self.co1_submit = tkinter.Button(self.bot_frame, text = "Submit", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.run_cust_option1(account_no))
        self.co1_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.co1, self.customer_menu, account_no))
        
        self.co1_submit.bind("<Enter>", self.on_hover)
        self.co1_submit.bind("<Leave>", self.on_leave)
        self.co1_back.bind("<Enter>", self.on_hover)
        self.co1_back.bind("<Leave>", self.on_leave)
        
        self.co1_lab_var = tkinter.StringVar()
        self.co1_label = tkinter.Label(self.bot_frame2, textvariable = self.co1_lab_var, fg = "red")
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.mid_frame.pack(pady = 10)
        self.bot_frame.pack(pady = 10)
        self.bot_frame2.pack()
        
        self.co1_title.pack(side = "top")
        self.co1_title_deco.pack(side = "top")
        self.co1_prompt.pack(side = "left")
        self.co1_input.pack(side = "left")
        self.co1_submit.pack(side = "left", padx = 5)
        self.co1_back.pack(side = "left", padx = 5)
        self.co1_label.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.co1_title.configure(font = cf)
        self.co1_title_deco.configure(font = cf)
        self.co1_prompt.configure(font = cf)
        self.co1_input.configure(font = cf)
        self.co1_submit.configure(font = cf)
        self.co1_back.configure(font = cf)
        self.co1_label.configure(font = cf)
        
        #ENTER Key Functionality
        self.co1.bind("<Return>", self.run_cust_option1)
    
    def cust_option2(self, account_no):    #Withdraw
        #Window Creation
        self.co2 = tkinter.Tk()
        self.co2.title("Withdraw")
        self.co2.geometry("300x200")
        self.co2.resizable(False, False) #Disable window resizing
        self.co2.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.co2)
        self.mid_frame = tkinter.Frame(self.co2)
        self.bot_frame = tkinter.Frame(self.co2)
        self.bot_frame2 = tkinter.Frame(self.co2)
        
        #Widgets
        self.co2_title = tkinter.Label(self.top_frame, text = "Withdraw")
        self.co2_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~")
        self.co2_prompt = tkinter.Label(self.mid_frame, text = "Enter Withdraw Amount : ")
        self.co2_input = tkinter.Entry(self.mid_frame, width = 10, relief = "flat", highlightthickness = 2)
        self.co2_submit = tkinter.Button(self.bot_frame, text = "Submit", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.run_cust_option2(account_no))
        self.co2_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.co2, self.customer_menu, account_no))
        
        self.co2_submit.bind("<Enter>", self.on_hover)
        self.co2_submit.bind("<Leave>", self.on_leave)
        self.co2_back.bind("<Enter>", self.on_hover)
        self.co2_back.bind("<Leave>", self.on_leave)
        
        self.co2_lab_var = tkinter.StringVar()
        self.co2_label = tkinter.Label(self.bot_frame2, textvariable = self.co2_lab_var, fg = "red")
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.mid_frame.pack(pady = 10)
        self.bot_frame.pack(pady = 10)
        self.bot_frame2.pack()
        
        self.co2_title.pack(side = "top")
        self.co2_title_deco.pack(side = "top")
        self.co2_prompt.pack(side = "left")
        self.co2_input.pack(side = "left")
        self.co2_submit.pack(side = "left", padx = 5)
        self.co2_back.pack(side = "left", padx = 5)
        self.co2_label.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.co2_title.configure(font = cf)
        self.co2_title_deco.configure(font = cf)
        self.co2_prompt.configure(font = cf)
        self.co2_input.configure(font = cf)
        self.co2_submit.configure(font = cf)
        self.co2_back.configure(font = cf)
        self.co2_label.configure(font = cf)
        
        #ENTER Key Functionality
        self.co2.bind("<Return>", self.run_cust_option2)
        
    def cust_option3(self, account_no, found_balance):  #Check balance
        #Window Creation
        self.co3 = tkinter.Tk()
        self.co3.title("Check Balance")
        self.co3.geometry("300x200")
        self.co3.resizable(False, False) #Disable window resizing
        self.co3.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.co3)
        self.mid_frame = tkinter.Frame(self.co3)
        self.bot_frame = tkinter.Frame(self.co3)
        
        #Widgets
        self.co3_title = tkinter.Label(self.top_frame, text = "Account Balance")
        self.co3_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~")
        self.co3_lab_var = tkinter.StringVar()
        self.co3_lab_var.set(f"{found_balance:.2f}")
        self.co3_label = tkinter.Label(self.mid_frame, textvariable = self.co3_lab_var, fg = "red")
        self.co3_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.co3, self.customer_menu, account_no))
        
        self.co3_back.bind("<Enter>", self.on_hover)
        self.co3_back.bind("<Leave>", self.on_leave)
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.mid_frame.pack(pady = 10)
        self.bot_frame.pack(pady = 10)
        
        self.co3_title.pack(side = "top")
        self.co3_title_deco.pack(side = "top")
        self.co3_label.pack(side = "top")
        self.co3_back.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        cf2 = tkinter.font.Font(family = "Times New Roman", size = 15, weight = "bold")
        self.co3_title.configure(font = cf)
        self.co3_title_deco.configure(font = cf)
        self.co3_label.configure(font = cf2)
        self.co3_back.configure(font = cf)
        
    def cust_option4(self, account_no):  #Update Customer Name
        #Window Creation
        self.co4 = tkinter.Tk()
        self.co4.title("Update Name")
        self.co4.geometry("380x250")
        self.co4.resizable(False, False) #Disable window resizing
        self.co4.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.co4)
        self.mid_frame = tkinter.Frame(self.co4)
        self.mid_frame2 = tkinter.Frame(self.co4)
        self.bot_frame = tkinter.Frame(self.co4)
        self.bot_frame2 = tkinter.Frame(self.co4)
        
        #Widgets
        self.co4_title = tkinter.Label(self.top_frame, text = "Update Name")
        self.co4_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~")
        self.co4_fname_prompt = tkinter.Label(self.mid_frame, text = "Enter New First Name : ")
        self.co4_fname_input = tkinter.Entry(self.mid_frame, width = 10, relief = "flat", highlightthickness = 2)
        self.co4_lname_prompt = tkinter.Label(self.mid_frame2, text = "Enter New Last Name : ")
        self.co4_lname_input = tkinter.Entry(self.mid_frame2, width = 10, relief = "flat", highlightthickness = 2)
        self.co4_submit = tkinter.Button(self.bot_frame, text = "Change", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.run_cust_option4(account_no))
        self.co4_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.co4, self.customer_menu, account_no))
        
        self.co4_submit.bind("<Enter>", self.on_hover)
        self.co4_submit.bind("<Leave>", self.on_leave)
        self.co4_back.bind("<Enter>", self.on_hover)
        self.co4_back.bind("<Leave>", self.on_leave)
        
        self.co4_lab_var = tkinter.StringVar()
        self.co4_label = tkinter.Label(self.bot_frame2, textvariable = self.co4_lab_var, fg = "red")
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.mid_frame.pack(pady = 10)
        self.mid_frame2.pack(pady = 10)
        self.bot_frame.pack(pady = 10)
        self.bot_frame2.pack()
        
        self.co4_title.pack(side = "top")
        self.co4_title_deco.pack(side = "top")
        self.co4_fname_prompt.pack(side = "left")
        self.co4_fname_input.pack(side = "left")
        self.co4_lname_prompt.pack(side = "left")
        self.co4_lname_input.pack(side = "left")
        self.co4_submit.pack(side = "left", padx = 5)
        self.co4_back.pack(side = "left", padx = 5)
        self.co4_label.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.co4_title.configure(font = cf)
        self.co4_title_deco.configure(font = cf)
        self.co4_fname_prompt.configure(font = cf)
        self.co4_fname_input.configure(font = cf)
        self.co4_lname_prompt.configure(font = cf)
        self.co4_lname_input.configure(font = cf)
        self.co4_submit.configure(font = cf)
        self.co4_back.configure(font = cf)
        self.co4_label.configure(font = cf)
        
    def cust_option5(self, account_no):  #Update Customer Address
        #Window Creation
        self.co5 = tkinter.Tk()
        self.co5.title("Update Address")
        self.co5.geometry("380x200")
        self.co5.resizable(False, False) #Disable window resizing
        self.co5.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.co5)
        self.mid_frame = tkinter.Frame(self.co5)
        self.bot_frame = tkinter.Frame(self.co5)
        self.bot_frame2 = tkinter.Frame(self.co5)
        
        #Widgets
        self.co5_title = tkinter.Label(self.top_frame, text = "Update Address")
        self.co5_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~")
        self.co5_prompt = tkinter.Label(self.mid_frame, text = "Enter New Address")
        self.co5_input = tkinter.Entry(self.mid_frame, width = 10, relief = "flat", highlightthickness = 2)
        self.co5_submit = tkinter.Button(self.bot_frame, text = "Submit", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.run_cust_option5(account_no))
        self.co5_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.co5, self.customer_menu, account_no))
        
        self.co5_submit.bind("<Enter>", self.on_hover)
        self.co5_submit.bind("<Leave>", self.on_leave)
        self.co5_back.bind("<Enter>", self.on_hover)
        self.co5_back.bind("<Leave>", self.on_leave)
        
        self.co5_lab_var = tkinter.StringVar()
        self.co5_label = tkinter.Label(self.bot_frame2, textvariable = self.co5_lab_var, fg = "red")
        
        #Positioning
        self.top_frame.pack(pady = 10)
        self.mid_frame.pack(pady = 10)
        self.bot_frame.pack(pady = 10)
        self.bot_frame2.pack()
        
        self.co5_title.pack(side = "top")
        self.co5_title_deco.pack(side = "top")
        self.co5_prompt.pack(side = "left")
        self.co5_input.pack(side = "left")
        self.co5_submit.pack(side = "left", padx = 5)
        self.co5_back.pack(side = "left", padx = 5)
        self.co5_label.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.co5_title.configure(font = cf)
        self.co5_title_deco.configure(font = cf)
        self.co5_prompt.configure(font = cf)
        self.co5_input.configure(font = cf)
        self.co5_submit.configure(font = cf)
        self.co5_back.configure(font = cf)
        self.co5_label.configure(font = cf)
        
    def cust_option6(self, fname, lname, address, account_no, balance, interest_rate, overdraft_limit): #Print Account Report
        #Window Creation
        self.co6 = tkinter.Tk()
        self.co6.title("Customer Details")
        self.co6.geometry("380x380")
        self.co6.resizable(False, False) #Disable window resizing
        self.co6.eval("tk::PlaceWindow . center")
        
        #Frame Creation
        self.top_frame = tkinter.Frame(self.co6)
        self.mid_frame1 = tkinter.Frame(self.co6)
        self.mid_frame2 = tkinter.Frame(self.co6)
        self.mid_frame3 = tkinter.Frame(self.co6)
        self.mid_frame4 = tkinter.Frame(self.co6)
        self.mid_frame5 = tkinter.Frame(self.co6)
        self.mid_frame6 = tkinter.Frame(self.co6)
        self.mid_frame7 = tkinter.Frame(self.co6)
        self.bot_frame = tkinter.Frame(self.co6)
        
        #Widgets
        self.co6_title = tkinter.Label(self.top_frame, text = "Customer Details")
        self.co6_title_deco = tkinter.Label(self.top_frame, text = "~~~~~~~~~~~~~~")
        
        self.co6_fname = tkinter.Label(self.mid_frame1, text = "First Name : ")
        self.co6_lab_var1 = tkinter.StringVar()
        self.co6_lab_var1.set(f"{fname}")
        self.co6_label1 = tkinter.Label(self.mid_frame1, textvariable = self.co6_lab_var1, fg = "blue")
        
        self.co6_lname = tkinter.Label(self.mid_frame2, text = "Last Name : ")
        self.co6_lab_var2 = tkinter.StringVar()
        self.co6_lab_var2.set(f"{lname}")
        self.co6_label2 = tkinter.Label(self.mid_frame2, textvariable = self.co6_lab_var2, fg = "blue")
        
        self.co6_address = tkinter.Label(self.mid_frame3, text = "Address : ")
        self.co6_lab_var3 = tkinter.StringVar()
        self.co6_lab_var3.set(f"{address}")
        self.co6_label3 = tkinter.Label(self.mid_frame3, textvariable = self.co6_lab_var3, fg = "blue")
        
        self.co6_acc_no = tkinter.Label(self.mid_frame4, text = "Account/No : ")
        self.co6_lab_var4 = tkinter.StringVar()
        self.co6_lab_var4.set(f"{account_no}")
        self.co6_label4 = tkinter.Label(self.mid_frame4, textvariable = self.co6_lab_var4, fg = "blue")
        
        self.co6_balance = tkinter.Label(self.mid_frame5, text = "Balance : ")
        self.co6_lab_var5 = tkinter.StringVar()
        self.co6_lab_var5.set(f"{balance}")
        self.co6_label5 = tkinter.Label(self.mid_frame5, textvariable = self.co6_lab_var5, fg = "blue")
        
        self.co6_ir = tkinter.Label(self.mid_frame6, text = "Interest Rate : ")
        self.co6_lab_var6 = tkinter.StringVar()
        self.co6_lab_var6.set(f"{interest_rate}")
        self.co6_label6 = tkinter.Label(self.mid_frame6, textvariable = self.co6_lab_var6, fg = "blue")
        
        self.co6_ol = tkinter.Label(self.mid_frame7, text = "Overdraft Limit : ")
        self.co6_lab_var7 = tkinter.StringVar()
        self.co6_lab_var7.set(f"{overdraft_limit}")
        self.co6_label7 = tkinter.Label(self.mid_frame7, textvariable = self.co6_lab_var7, fg = "blue")
        
        self.co6_back = tkinter.Button(self.bot_frame, text = "Back", bg = "red", fg = "white", cursor = "hand2", relief = "flat", width = 10, height = 1, command = lambda: self.go_back(self.co6, self.customer_menu, account_no))
        
        self.co6_back.bind("<Enter>", self.on_hover)
        self.co6_back.bind("<Leave>", self.on_leave)
        
        #Positioning
        self.top_frame.pack()
        self.mid_frame1.pack()
        self.mid_frame2.pack()
        self.mid_frame3.pack()
        self.mid_frame4.pack()
        self.mid_frame5.pack()
        self.mid_frame6.pack()
        self.mid_frame7.pack()
        self.bot_frame.pack()
        
        self.co6_title.pack(side = "top") #title
        self.co6_title_deco.pack(side = "top")
        self.co6_fname.pack(side = "left") #fname
        self.co6_label1.pack(side = "left")
        self.co6_lname.pack(side = "left") #lname
        self.co6_label2.pack(side = "left")
        self.co6_address.pack(side = "left") #address
        self.co6_label3.pack(side = "left")
        self.co6_acc_no.pack(side = "left") #acc_no
        self.co6_label4.pack(side = "left")
        self.co6_balance.pack(side = "left") #balance
        self.co6_label5.pack(side = "left")
        self.co6_ir.pack(side = "left") #interest rate
        self.co6_label6.pack(side = "left")
        self.co6_ol.pack(side = "left") #overdraft limit
        self.co6_label7.pack(side = "left")
        self.co6_back.pack(side = "top")
        
        #Custom Font
        cf = tkinter.font.Font(family = "Times New Roman", size = 12, weight = "bold")
        self.co6_title.configure(font = cf)
        self.co6_title_deco.configure(font = cf)
        self.co6_fname.configure(font = cf)
        self.co6_label1.configure(font = cf)
        self.co6_lname.configure(font = cf)
        self.co6_label2.configure(font = cf)
        self.co6_address.configure(font = cf)
        self.co6_label3.configure(font = cf)
        self.co6_acc_no.configure(font = cf)
        self.co6_label4.configure(font = cf)
        self.co6_balance.configure(font = cf)
        self.co6_label5.configure(font = cf)
        self.co6_ir.configure(font = cf)
        self.co6_label6.configure(font = cf)
        self.co6_ol.configure(font = cf)
        self.co6_label7.configure(font = cf)
        self.co6_back.configure(font = cf)
        
    #Function Calls
    def on_hover(self, event):
        self.done = 0 
        event.widget['bg'] = "White"
        event.widget['fg'] = "Red"
        
    def on_leave(self, event):
        self.done = 0 
        event.widget['bg'] = "Red"
        event.widget['fg'] = "White"
        
    def search_admins_by_name(self, admin_username):
        found_admin = None
        for a in self.admins_list:
            username = a.get_username()
            if username == admin_username:
                found_admin = a
        if found_admin == None:
            self.lab_var.set("The admin %s does not exist! Try again..." %admin_username)
        return found_admin
        
    def run_admin_login(self, event = None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.lab_var.set("")
        
        found_admin = self.search_admins_by_name(username)
        if found_admin != None:
            if found_admin.get_password() == password:
                self.current_admin = found_admin   #Store current admin
                self.al_warning_label.config(text = "Login is successful.", fg = "green")
                self.al.destroy()
                self.admin_menu()
            else:
                self.lab_var.set("Login has failed.", fg = "red")
    
    def load_admin_option1(self):
        self.am.destroy()
        self.admin_option1()
        
    def load_admin_option2(self):
        self.am.destroy()
        self.admin_option2()
        
    def load_admin_option3(self):
        self.am.destroy()
        self.admin_option3()
        
    def load_admin_option4(self):   #Admin Management Report
        self.am.destroy()
        
        count_cust = 0 
        for a in self.accounts_list:
            if isinstance(a, (SavingsAccount, CurrentAccount)):
                count_cust += 1
                
        sum_balance = 0 
        for a in self.accounts_list:
            sum_balance += a.get_balance()
            
        total_interest = 0 
        for a in self.accounts_list:
            if isinstance(a, SavingsAccount):
                total_interest += a.get_balance() * (a.get_interest()/100)
            
        total_overdraft = 0 
        for a in self.accounts_list:
            if isinstance(a, CurrentAccount):
                total_overdraft += a.get_overdraft() - a.get_balance()
        
        self.admin_option4(count_cust, sum_balance, total_interest, total_overdraft)
        
    def load_admin_option5(self):
        self.am.destroy()
        self.admin_option5()
        
    def load_admin_option6(self):
        self.am.destroy()
        self.admin_option6()
    
    def search_cust_by_acc(self, cus_account):  
        found_cust = None
        
        for a in self.accounts_list:
            account = a.get_account_no()
            if int(account) == int(cus_account):
               found_cust = a
        return found_cust
    
    def run_admin_option1(self):    #Admin Transfer Function
        sender = self.o1_sender_acc_input.get()
        receiver = self.o1_receiver_acc_input.get()
        amount = self.o1_amount_transfer_input.get()
        amount = float(amount)
        self.o1_lab_var.set("")
        
        if not sender or not receiver or not amount:
            self.o1_lab_var.set("Fields cannot be empty!")
            return
        
        if not sender.isdigit():
            self.o1_lab_var.set("Invalid Sender Account Number.")
            return
        if not receiver.isdigit():
            self.o1_lab_var.set("Invalid Receiver Account Number.")
            return
        
        try:  
            if amount <= 0:
                self.o1_lab_var.set("Transfer amount must be greater than zero.")
                return
        except ValueError:
            self.o1_lab_var.set("Invalid Deposit Amount.")
            return
        
        found_sender = self.search_cust_by_acc(sender)
        found_receiver = self.search_cust_by_acc(receiver)
        if found_sender == None:
           self.o1_lab_var.set("Sender Account Not Found.")
        else:
            if found_receiver == None:
               self.o1_lab_var.set("Receiver Account Not Found.")
            else:
                if int(sender) <= 0:
                    self.o1_lab_var.set("Invalid Sender Account Number")
                    return
                elif int(receiver) <= 0:
                    self.o1_lab_var.set("Invalid Receiver Account Number")
                    return
                else:
                    if found_sender == found_receiver:
                        self.o1_lab_var.set("Cannot transfer to the same account!")
                        return
                    else:
                        available_balance = found_sender.get_balance()
                        available_balance = float(available_balance)
                    
                        if amount > available_balance:
                           self.o1_lab_var.set("Insufficient Balance.")
                        else:
                           found_sender.withdraw(amount)
                           found_receiver.deposit(amount)
                           self.save_bank_data()
                           self.o1_lab_var.set("Transfer Successful.")
                   
    def run_admin_option2(self, event = None):    #Admin > Search for Customer Account
        account = self.o2_input.get().strip()
        self.o2_lab_var.set("")
        
        if not account:
            self.o2_lab_var.set("Account number required!")
            return
        if not account.isdigit():
            self.o2_lab_var.set("Invalid Account Number.")
            return
        if int(account) <= 0:
            self.o2_lab_var.set("Invalid Account Number.")
            return
        
        found_acc = self.search_cust_by_acc(account)
        if found_acc == None:
           self.o2_lab_var.set(f"Error: Account {account} Not Found.")
        else:
           account_no = found_acc.get_account_no()
           self.o2.destroy()
           self.customer_menu(account_no)
    
    def run_admin_option3(self):      #Admin Delete Customer Account Function
        account = self.o3_input.get()
        self.o3_lab_var.set("")
        
        if not account:
            self.o3_lab_var.set("Account Number Required.")
            return
        if not account.isdigit():
            self.o3_lab_var.set("Please enter a valid account number.")
            return
        
        found_account = self.search_cust_by_acc(account)
        if found_account == None:
            self.o3_lab_var.set(f"Account {account} Not Found.")
        else:
            confirm = tkinter.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete account {account}?")
            if confirm:
                self.accounts_list.remove(found_account)
                self.save_bank_data()
                self.o3_lab_var.set(f"Account {account} has been successfully deleted.") 
        
    def run_admin_option5(self):   #Admin Update Name Function
        new_fname = self.o5_fname_input.get().strip().capitalize()
        new_lname = self.o5_lname_input.get().strip().capitalize()
        
        if not new_fname or not new_lname:
            self.o5_lab_var.set("Names cannot be empty")
            return
        if not re.match(r"^[A-Za-z]+$", new_fname) or not re.match(r"^[A-Za-z]+$", new_lname):
            self.o5_lab_var.set("Invalid Name! Use Letters Only.")
            return
        if len(new_fname) > 15 or len(new_lname) > 15:
            self.o5_lab_var.set("Name too long! Max 15 characters.")
            return
        
        self.current_admin.update_first_name(new_fname)
        self.current_admin.update_last_name(new_lname)
        self.save_bank_data()
        fname = self.current_admin.get_first_name()
        lname = self.current_admin.get_last_name()
        self.o5_lab_var.set(f"New Name : {fname} {lname}")
        
    def run_admin_option6(self):   #Admin Update Address Function
        new_address = self.o6_input.get()
        new_address = new_address.strip()
        
        if not new_address:
            self.o6_lab_var.set("Address cannot be empty.")
            return
        if not re.match(r"^[A-Za-z0-9\s,.-]+$", new_address):
            self.o6_lab_var.set("Invalid Address!")
            return
        
        self.current_admin.update_address(new_address.split(", "))
        self.save_bank_data()
        address = self.current_admin.get_address()
        self.o6_lab_var.set(f"New Address : {', '.join(address)}")  
                  
    def load_cust_option1(self, account_no):
        self.co.destroy()
        self.cust_option1(account_no)
        
    def load_cust_option2(self, account_no):
        self.co.destroy()
        self.cust_option2(account_no)
        
    def load_cust_option3(self, account_no):
        self.co.destroy()
        
        found_balance = None
        for a in self.accounts_list:
            account = a.get_account_no()
            if account == account_no:
               found_balance = a.get_balance()
               break
        self.cust_option3(account_no, found_balance)
        
    def load_cust_option4(self, account_no):
        self.co.destroy()
        self.cust_option4(account_no)
        
    def load_cust_option5(self, account_no):
        self.co.destroy()
        self.cust_option5(account_no)
        
    def load_cust_option6(self, account_no):
        self.co.destroy()
        
        found_account = None
        for a in self.accounts_list:
            if str(a.get_account_no()) == str(account_no):  #Ensure correct type comparison
                found_account = a
                break
        if found_account is None:
            print("Error: Account not found.")
            return
        
        found_fname = found_account.get_first_name()
        found_lname = found_account.get_last_name()
        found_address = ", ".join(found_account.get_address())  #Format for display
        found_account_no = found_account.get_account_no()
        found_balance = found_account.get_balance()
        
        if isinstance(found_account, SavingsAccount):
            found_interest_rate = found_account.interest_rate
        else:
            found_interest_rate = "N/A"
        if isinstance(found_account, CurrentAccount):
            found_overdraft_limit = found_account.overdraft_limit
        else:
            found_overdraft_limit = "N/A"
        
        self.cust_option6(found_fname, found_lname, found_address, found_account_no, 
                      found_balance, found_interest_rate, found_overdraft_limit)
        
    def go_back(self, current_window, previous_window, *args):  #Universal Go Back Function
        if hasattr(current_window, "destroy"):  
            current_window.destroy() 
            previous_window(*args)
        else:
            print("Error: Current window is not a valid Tkinter instance.")      
        
    def run_cust_option1(self, account_no):  #Customer Deposit Function
        deposit_amount = self.co1_input.get()
        self.co1_lab_var.set("")
        
        if not deposit_amount:
            self.co1_lab_var.set("Enter a deposit amount.")
            return
        
        try:
            deposit_amount = float(deposit_amount)
            if deposit_amount <= 0:
                self.co1_lab_var.set("Deposit amount must be greater than zero.")
                return
        except ValueError:
            self.co1_lab_var.set("Invalid Deposit Amount. Try Again.")
            return
        
        if not re.match(r"^\d+(\.\d{1,2})?$", deposit_amount): 
            self.co1_lab_var.set("Max 2 decimal places.")
            return
        
        max_deposit_limit = 100000 #Setting Max Deposit 
        if deposit_amount > max_deposit_limit:
            self.co1_lab_var.set(f"{deposit_amount} exceeds limit.")
            return
            
        found_account = None    
        for a in self.accounts_list:
            if str(a.get_account_no()) == str(account_no):
                found_account = a
                break
        if found_account == None:
            self.co1_lab_var.set("Something went wrong. Please try again.")
            return
        if isinstance(found_account, SavingsAccount):
            found_account.deposit(deposit_amount)
            found_account.apply_interest()
        elif isinstance(found_account, CurrentAccount):
            found_account.deposit(deposit_amount)
        self.save_bank_data()
        new_balance = found_account.get_balance()
        self.co1_lab_var.set(f"New Balance : {new_balance:.2f}")
        
    def run_cust_option2(self, account_no):  #Customer Withdraw Function
        withdraw_amount = self.co2_input.get()
        self.co2_lab_var.set("")
        
        if not withdraw_amount:
            self.co2_lab_var.set("Enter a valid withdrawal amount.")
            return
        
        try:
            withdraw_amount = float(withdraw_amount)
            if withdraw_amount <= 0:
                self.co2_lab_var.set("Withdraw amount must be greater than zero.")
                return
        except ValueError:
            self.co2_lab_var.set("Invalid Withdraw Amount. Try Again.")
            return
        
        if not re.match(r"^\d+(\.\d{1,2})?$", withdraw_amount):  
            self.co2_lab_var.set("Max 2 decimal places.")
            return
        
        max_withdraw_limit = 100000
        if withdraw_amount > max_withdraw_limit:
            self.co2_lab_var.set(f"{withdraw_amount} exceeds limit.")
        
        found_account = None
        for a in self.accounts_list:
            if str(a.get_account_no()) == str(account_no):
                found_account = a 
                break
        if found_account == None:
            self.co2_lab_var.set("Something went wrong. Please try again.")
            return
        if isinstance(found_account, CurrentAccount):
            available_funds = found_account.get_balance() + found_account.overdraft_limit
            if withdraw_amount > available_funds:
                self.co2_lab_var.set("Overdraft limit exceeded.")
                return
        else:
            if withdraw_amount > found_account.get_balance():
                self.co2_lab_var.set("Insufficient balance.")
                return
        found_account.withdraw(withdraw_amount)
        self.save_bank_data()
        new_balance = found_account.get_balance()
        self.co2_lab_var.set(f"New Balance : {new_balance:.2f}")
        
        
    def run_cust_option4(self, account_no):  #Customer Update Name Function
        new_fname = self.co4_fname_input.get().strip().capitalize()
        new_lname = self.co4_lname_input.get().strip().capitalize()
        
        if not new_fname or not new_lname:
            self.co4_lab_var.set("Names cannot be empty.")
            return
        
        if not re.match(r"^[A-Za-z]+$", new_fname) or not re.match(r"^[A-Za-z]+$", new_lname):
            self.co4_lab_var.set("Invalid Name! Use Letters Only.")
            return
        
        if len(new_fname) > 15 or len(new_lname) > 15:
            self.o5_lab_var.set("Name too long! Max 15 characters.")
            return
        
        found_account = None
        for a in self.accounts_list:
            if str(a.get_account_no()) == str(account_no):
                found_account = a 
                break
        if found_account == None:
            self.co4_lab_var.set("Something went wrong. Please try again.")
            return
        found_account.update_first_name(new_fname)
        found_account.update_last_name(new_lname)
        self.save_bank_data()
        fname = found_account.get_first_name()
        lname = found_account.get_last_name()
        self.co4_lab_var.set(f"New Name : {fname} {lname}")
        
    def run_cust_option5(self, account_no):  #Customer Update Address Function
        new_address = self.co5_input.get()
        new_address = new_address.strip()
        
        if not new_address:
            self.co5_lab_var.set("Address cannot be empty.")
            return
        if not re.match(r"^[A-Za-z0-9\s,.-]+$", new_address):
            self.co5_lab_var.set("Invalid Address!")
            return
        found_account = None
        for a in self.accounts_list:
            if str(a.get_account_no()) == str(account_no):
                found_account = a 
                break
        if found_account == None:
            self.co5_lab_var.set("Something went wrong. Please try again.")
            return
        found_account.update_address(new_address.split(", "))
        self.save_bank_data()
        address = found_account.get_address()
        self.co5_lab_var.set(f"New Address : {', '.join(address)}")         
        
gui = BankSystem()
gui.main_menu()
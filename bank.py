import sys
import datetime
from login import check_login


current_datetime = datetime.datetime.now()
day = current_datetime.day
suffix = "th"

if 4 <= day <= 20 or 24 <= day <= 30:
    suffix = "th"
elif day == 1 or day % 10 == 1:
    suffix = "st"
elif day == 2 or day % 10 == 2:
    suffix = "nd"
elif day == 3 or day % 10 == 3:
    suffix = "rd"
formatted_datetime = current_datetime.strftime(f"{day}{suffix} %B %H:%M")


def get_user_input():
    try:
        user_input = input("Enter a command: ")
    except EOFError:
        user_input = "/exit"
    return user_input


def display_balance(username):
    with open("user_credentials.txt", "r") as file:
        for line in file:
            stored_username, stored_password, balance, *_ = line.strip().split(",")
            if stored_username == username:
                print("Your balance:", balance)
                break


def change_password(username):
    current_password = input("Enter your current password: ")
    new_password = input("Enter your new password: ")
    confirm_password = input("Confirm your new password: ")

    # Verify the current password using the check_login function
    if check_login(username, current_password):
        if new_password == confirm_password:
            # Change the password in the user_credentials.txt file

            with open("user_credentials.txt", "r") as file:
                lines = file.readlines()

            with open("user_credentials.txt", "w") as file:
                for line in lines:
                    stored_username, stored_password, balance, *transactions = line.strip().split(",")
                    if stored_username == username:
                        file.write(f"{stored_username},{new_password},{balance},{','.join(transactions)}\n")
                        print("Password changed successfully!")
                    else:
                        file.write(line)
        else:
            print("New passwords do not match.")
    else:
        print("Authentication failed. Please check your credentials.")


def deposit(username):
    amount = float(input("Enter the amount to deposit: "))

    with open("user_credentials.txt", "r") as file:
        lines = file.readlines()

    with open("user_credentials.txt", "w") as file:
        for line in lines:
            stored_username, stored_password, balance, *transactions = line.strip().split(",")
            if stored_username == username:
                new_balance = float(balance) + amount
                transactions.append(f"Deposited {amount}")
                file.write(f"{stored_username},{stored_password},{new_balance},{','.join(transactions)}\n")
                print("Deposit successful!")
            else:
                file.write(line)


def withdraw(username):
    amount = float(input("Enter the amount to withdraw: "))

    with open("user_credentials.txt", "r") as file:
        lines = file.readlines()

    with open("user_credentials.txt", "w") as file:
        for line in lines:
            stored_username, stored_password, balance, *transactions = line.strip().split(",")
            if stored_username == username:
                current_balance = float(balance)
                if amount > current_balance:
                    print("Insufficient balance.")
                    file.write(line)  # Rewrite the line without updating the balance
                else:
                    new_balance = current_balance - amount
                    transactions.append(f"Withdrew {amount}")
                    file.write(f"{stored_username},{stored_password},{new_balance},{','.join(transactions)}\n")
                    print("Withdrawal successful!")
            else:
                file.write(line)


def display_transactions(username):
    with open("user_credentials.txt", "r") as file:
        for line in file:
            stored_username, *_ = line.strip().split(",")
            if stored_username == username:
                print("Account Statements:")
                # Print the transactions associated with the user
                transactions = line.strip().split(",")[3:]
                for transaction in transactions:
                    print(transaction)
                break


def display_account_info(username):
    with open("user_credentials.txt", "r") as file:
        for line in file:
            stored_username, stored_password, balance, *_ = line.strip().split(",")
            if stored_username == username:
                print("Account Information:")
                print("Username:", stored_username)
                print("Balance:", balance)
                break


def bank_interface(local_input_username):
    while True:
        try:
            print("Hi", input_username, "! It's now", formatted_datetime)
            user_input = input("Enter a command: ")
        except EOFError:
            user_input = "/exit"

        if user_input == "/test":
            print("Test command executed")
        elif user_input == "/balance":
            display_balance(local_input_username)
        elif user_input == "/exit":
            print("Exiting the script")
            sys.exit()
        elif user_input == "/deposit":
            deposit(local_input_username)
        elif user_input == "/withdraw":
            withdraw(local_input_username)
        elif user_input == "/transactions":
            display_transactions(local_input_username)
        elif user_input == "/changepassword":
            change_password(local_input_username)
        elif user_input == "/account statements":
            display_account_info(local_input_username)
        else:
            print("Unknown command")


if __name__ == "__main__":
    with open("username.txt", "r") as f:
        input_username = f.readline().strip()

    bank_interface(input_username)

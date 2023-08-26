import sys
import datetime

current_datetime = datetime.datetime.now()  # Get the current local date and time
day = current_datetime.day
suffix = "th"  # Default suffix

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
        user_input = "/exit"  # Handle EOFError specifically
    return user_input


def display_balance(username):
    with open("user_credentials.txt", "r") as file:
        for line in file:
            stored_username, stored_password, balance = line.strip().split(",")
            if stored_username == username:
                print("Your balance:", balance)
                break


def deposit(username):
    amount = float(input("Enter the amount to deposit: "))
    lines = []

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
    lines = []

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
            stored_username, _, _, *transactions = line.strip().split(",")
            if stored_username == username:
                print("Transaction History:")
                for transaction in transactions:
                    print(transaction)
                break


def main():
    with open("username.txt", "r") as f:
        input_username = f.readline().strip()
    print("Hi!", input_username, "It's now", formatted_datetime)
    while True:
        try:
            user_input = input("Enter a command: ")
        except EOFError:
            user_input = "/exit"

        if user_input == "/test":
            print("Test command executed")
        elif user_input == "/balance":
            display_balance(input_username)  # Call the function here
        elif user_input == "/exit":
            print("Exiting the script")
            sys.exit()
        elif user_input == "/deposit":
            deposit(input_username)
        elif user_input == "/withdraw":
            withdraw(input_username)
        elif user_input == "/transactions":
            display_transactions(input_username)
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()

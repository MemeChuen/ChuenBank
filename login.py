def check_login(username, password):
    with open("user_credentials.txt", "r") as file:
        for line in file:
            stored_username, stored_password, _ = line.strip().split(",", 2)
            if stored_username == username and stored_password == password:
                return True
    return False

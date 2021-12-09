from funktiot import *
credentials = {
    'admin': 'admin',
    'user': 'user'
}

teatteri = ElokuvaTeatteri()

def main():
    account = menu_notloggedin()
    if account == "admin":
        admin_menu()
    elif account == "user":
        menu_loggedin()

if __name__ == "__main__":
    main()
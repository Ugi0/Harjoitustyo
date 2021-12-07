from funktiot import *

credentials = {
    'admin': 'admin',
    'user': 'user'
}

elokuvat = getshows()
Salit = [
    Sali(1,12,10).lisää_elokuva(elokuvat[0],0,"20:00"),
    Sali(2,15,10).lisää_elokuva(elokuvat[0],0,"12:00").lisää_elokuva(elokuvat[1],6,"18:05").lisää_elokuva(elokuvat[0],0,"20:00")
    ]

def main():
    account = menu_notloggedin()
    if account == "admin":
        admin_menu()
    elif account == "user":
        menu_loggedin()

if __name__ == "__main__":
    main()

    # TODO
    # Varmista että admin ei laita elokuvia päällekkäin
    # Parempi asettelu buttoneille
    # Varmista että teksteissä ei ole englantia jäljellä
    # Documentation

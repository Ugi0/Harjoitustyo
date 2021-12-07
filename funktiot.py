import PySimpleGUI as sg
import copy

from PySimpleGUI.PySimpleGUI import Button, popup

class Sali:
    def __init__(self, ID, rivit, rivinpenkit):
        self.ID = ID
        self.rows = rivit
        self.columns = rivinpenkit
        self.shows = {x:[] for x in range(7)}
    def lisää_elokuva(self, elokuva, paiva, aloitusaika):
        kopio = copy.deepcopy(elokuva)
        self.shows[paiva].append((aloitusaika,kopio))
        kopio.size = (self.rows,self.columns)
        kopio.seats = [[0 for x in range(self.columns)] for x in range(self.rows)]
        return self
    def get_shows(self):
        return self.shows
    def vapaa(self,aloitusaika,kesto):
        aloitusaika = 60*int(aloitusaika.split(":")[0])+ int(aloitusaika.split(":")[1])
        return fit(aloitusaika, int(kesto), self.shows)

class Näytös:
    def __init__(self, nimi, kuvaus, kesto):
        self.kesto = int(kesto)
        self.nimi = nimi
        self.desc = kuvaus
        self.size = (0,0)
        self.seats = []
    def __str__(self):
        return self.nimi
    def varaapaikka(self, row, seat, customer):
        self.seats[row][seat] = customer
    def get_info(self):
        return "{};{};{}".format(self.nimi,self.desc,self.kesto)

def fit(aika, kesto, elokuvat):
    sor = sorted(elokuvat, key = lambda x: x.alkuaika)[::-1]
    for i in range(len(sor)):
        if aika+kesto < sor[i].alkuaika:
            if i+1 == len(sor):
                return True
            elif sor[i+1].loppuaika < aika:
                return True
    return False


def add_movie():
    Näytökset = getshows()
    layout = [[sg.Text("Elokuvan nimi",size=(10,1)),sg.Input()], 
    [sg.Text("Kuvaus",size=(10,1)),sg.Multiline()],
    [sg.Text("Kesto (mins)",size=(10,1)),sg.Spin([x for x in range(0,12)]),sg.Text("h",pad=(0,0)),sg.Spin([x for x in range(0,60)]),sg.Text("m",pad=(0,0))],
    [sg.Stretch(),sg.Button("Lisää elokuva")]]
    window = sg.Window(title="Elokuvan lisäys", layout=layout, size=(400, 400))
    while True:
        event, values = window.read()
        if event == "Lisää elokuva":
            if values[0] == "" or (values[2] == '0' and values[3] == '0'):
                sg.popup("Jokin syötteistä ei ole täytetty")
            else:
                print(values)
                Näytökset.append(Näytös(values[0],values[1],60*values[2]+values[3]))
                with open("elokuvat.txt","w",encoding='utf-8') as t:
                    for z in Näytökset:
                        t.write(z.get_info()+"\n")
                break
        if event == sg.WIN_CLOSED:
            break
    window.close()

def tonum(num):
    return 60*int(num.split(":")[0])+ int(num.split(":")[1])

def getspace(kesto,num,num2):
    num = tonum(num)+int(kesto)
    num2 = tonum(num2)
    return (num2-num)

def editshow(sali,movie,user=False):
    layout = [[sg.Text(f"Elokuva {movie[1].nimi}")],[sg.Button("Poista tämä ohjelmistosta",key="poista")],[sg.Button("Muuta varauksia")]]
    window = sg.Window(title="Ohjelmiston muutos", layout=layout, size=(400, 400))
    while True:
        event, values = window.read()
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
        if event == "poista":
            sali.shows[movie[2]].remove(movie[:2])
            window.close()
            return True
        if event == "Muuta varauksia":
            showseats(movie[1],user)
            break
    window.close()

def lisääohjelmasaliin(sali):
    päivät = ["Maanantai","Tiistai","Keskiviikko","Torstai","Perjantai","Lauantai","Sunnuntai"]
    elokuvat = getshows()
    layout = [[sg.Text("Elokuva",size=(7,1)),sg.Combo(values = [x for x in elokuvat])],[sg.Text("Päivä",size=(7,1)),sg.Combo(values = päivät)],
    [sg.Text("Aika",size=(7,1)),sg.Spin([x for x in range(12,24)]),sg.Text(":",pad=(0,0)),sg.Spin([x for x in range(0,60)])],[sg.Button("Valmis")]]
    window = sg.Window(title="Lisää elokuva ohjelmistoon", layout=layout, size=(400, 400))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if any([values[x] == '' for x in values]):
            sg.popup("You need to fill all of the inputs")
        elif event == "Valmis":
            movie = copy.deepcopy(values[0])
            päivä = päivät.index(values[1])
            aika = f"{values[2]}:{values[3]}"
            sali.lisää_elokuva(movie,päivä,aika)
            window.close()
            return True
    window.close()


def näytäohjelmisto(sali,user):
    width = 18
    height = 3
    layout = [ [
        sg.Column(
            [[sg.Text("Maanantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[0]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(0,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[0]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[0])]
        ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Tiistai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[1]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(1,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[1]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[1])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Keskiviikko",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[2]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(2,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[2]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[2])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Torstai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[3]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(3,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[3]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[3])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Perjantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[4]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(4,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[4]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[4])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Lauantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[5]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(5,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[5]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[5])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Sunnuntai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[6]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(6,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[6]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[6])]
            )
            ]]
    if user == True:
        layout[0].append(sg.Column(
        [[sg.Button("Lisää ohjelmistoa\n saliin", size=(10,4),key="lisää")]]
            ,vertical_alignment='bottom')
        )
    window = sg.Window(title=f"Salin {sali.ID} ohjelmisto", layout=layout, size=(1330 if user == True else 1220, 830))
    while True:
        event, values = window.read()
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
        if event == "lisää":
            if lisääohjelmasaliin(sali):
                layout = [ [sg.Column([[sg.Text("Maanantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[0]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(0,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[0]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[0])]),sg.VSeparator(),sg.Column([[sg.Text("Tiistai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[1]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(1,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[1]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[1])]),sg.VSeparator(),sg.Column([[sg.Text("Keskiviikko",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[2]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(2,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[2]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[2])]),sg.VSeparator(),sg.Column([[sg.Text("Torstai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[3]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(3,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[3]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[3])]),sg.VSeparator(),sg.Column([[sg.Text("Perjantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[4]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(4,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[4]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[4])]),sg.VSeparator(),sg.Column([[sg.Text("Lauantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[5]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(5,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[5]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[5])]),sg.VSeparator(),sg.Column([[sg.Text("Sunnuntai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[6]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(6,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[6]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[6])])]]
                window1 = sg.Window(title=f"Salin {sali.ID} ohjelmisto", layout=layout, size=(1330 if user == True else 1220, 830))
                window.close()
                window = window1
        elif type(event) == tuple:
            if user == "notloggedin":
                sg.popup("Kirjaudu sisään niin voit varata paikan")
            elif user:
                if editshow(sali,event,user):
                    window[event].update(visible=False)
                    sg.popup("Elokuva poistettu")
            else:
                showseats(event[1])
    window.close()

def salivalinta(user = False):
    from Harjoitustyö import Salit
    layout = [[sg.Text(f"Näytä ohjelmisto salille")]] + [[sg.Button(f"Sali numero {x.ID}, koko {x.rows}x{x.columns}", key=x)] for x in Salit] + [[sg.Stretch(),sg.Button("Valmis")]]
    window = sg.Window(title="Valitse sali", layout=layout, size=(400, 400))
    while True:
        event, values = window.read()
        if event in Salit:
            näytäohjelmisto(event,user)
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
    window.close()

def admin_menu():
    layout = [[sg.Text("Elokuvateatterin varausjärjestelmä: Admin")],
    [sg.Button("Näytä salin ohjelmisto")],
    [sg.Button("Lisää elokuva")],
    [sg.Button("Selaa elokuvia")], 
    [sg.Stretch(),sg.Button("Valmis")]]
    window = sg.Window(title="Elokuvateatterin varausjärjestelmä", layout=layout, size=(400, 400))
    while True:
        event, values = window.read()
        if event == "Näytä salin ohjelmisto":
            salivalinta(True)
        if event == "Lisää elokuva":
            add_movie()
        if event == "Selaa elokuvia":
            browse(0,"admin")
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
    window.close()

def totime(num,num2):
    hour = num // 60
    minute = str(num % 60)
    hour2 = num2 // 60
    minute2 = str(num2 % 60)
    minute = "0"+minute if len(minute) == 1 else minute
    minute2 = "0"+minute2 if len(minute2) == 1 else minute2
    txt = f"{hour}:{minute} - {hour2}:{minute2}"
    return txt

def checkwindow():
    layout = [[sg.Text("Oletko varma että haluat varata tämän paikan?")],[sg.Button("Kyllä"),sg.Button("En")]]
    window = sg.Window(title="Varmistus", layout=layout, size=(300, 100))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "En":
            window.close()
            return False
        if event == "Kyllä":
            window.close()
            return True

def adminseatwindow(movie,seat):
    layout = [[sg.Text("Muuta varausta tälle paikalle")],
    [sg.Button("Poista varaus"),sg.Button("Tämä penkki ei ole käytössä")]]
    window = sg.Window(title="Paikan varaus", layout=layout, size=(50*movie.size[1], 50*movie.size[0]))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Poista varaus":
            movie.seats[seat[0]][seat[1]] = 0
            window.close()
            return 0
        if event == "Tämä penkki ei ole käytössä":
            movie.seats[seat[0]][seat[1]] = 1
            window.close()
            return 1
    window.close()

def showseats(movie,user=False):
    layout = [[sg.Text(f"Varaa paikka elokuvaan {movie.nimi}")]] + [[sg.Stretch()]+[sg.Button('',button_color=("green" if movie.seats[i][j] == 0 else "red"), size=(4, 2), key=(i,j), pad=((0,2),(0,2))) for j in range(movie.size[1])]+[sg.Stretch()] for i in range(movie.size[0])] + [[sg.Stretch(),sg.Text("Teatterin kangas on tässä"),sg.Stretch()]]
    window = sg.Window(title="Paikan varaus", layout=layout, size=(50*movie.size[1], 50*movie.size[0]))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if user == True:
            num = adminseatwindow(movie,event)
            window[event].update(button_color=("green" if num == 0 else "red"))
        else:
            if movie.seats[event[0]][event[1]]:
                popup("Paikka on jo varattu")
            elif checkwindow():
                movie.varaapaikka(event[0],event[1],"user")
                break
    window.close()

def getmovietimes(elokuva):
    from Harjoitustyö import Salit
    li = []
    for sali in Salit:
        for z in range(7):
            päivä = sali.shows[z]
            for x in päivä:
                if x[1].nimi == elokuva.nimi:
                    li.append((z,x[0],x[1],sali.ID))
    return sorted(sorted(li,key=lambda x : x[1]), key=lambda x : x[0])

def reservewindow(movie):
    päivät = ["Maanantai","Tiistai","Keskiviikko","Torstai","Perjantai","Lauantai","Sunnuntai"]
    elokuvat = getmovietimes(movie)
    layout = [[sg.Text(f"Varaa aika elokuvaan {movie.nimi}")]] + [[sg.Button(f"{päivät[x[0]]} {x[1]} Sali {x[3]}", key = x[2])] for x in elokuvat]
    window = sg.Window(title="Ajan varaus", layout=layout, size=(400, 400))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        else:
            showseats(event)
            window.close()
    window.close()

def getshows():
    return [Näytös(x.split(";")[0],x.split(";")[1],x.split(";")[2]) for x in open("elokuvat.txt","r",encoding="utf-8").read().split("\n") if x != '']

def browse(i,log=True):
    elokuvat = getshows()
    layout = [ [
        sg.Column([
            [sg.Text(elokuvat[i%len(elokuvat)].nimi)], [sg.Text(elokuvat[i%len(elokuvat)].desc,size=(30, 26))], [sg.Button("Valmis"),sg.Stretch(),sg.Button("Varaa paikka",key="-FIRST-")]
            ]),
        sg.VSeparator(),
        sg.Column([
            [sg.Text(elokuvat[(i+1)%len(elokuvat)].nimi)], [sg.Text(elokuvat[(i+1)%len(elokuvat)].desc,size=(30, 26))], [sg.Button("Varaa paikka",key="-SECOND-"),sg.Stretch(),sg.Button("Selaa lisää elokuvia")]
            ])
    ]]
    if log == "admin":
        layout = [[sg.Column([[sg.Text(elokuvat[i%len(elokuvat)].nimi)], [sg.Text(elokuvat[i%len(elokuvat)].desc,size=(30, 26))], [sg.Button("Valmis"),sg.Stretch()]]),sg.VSeparator(),sg.Column([[sg.Text(elokuvat[(i+1)%len(elokuvat)].nimi)], [sg.Text(elokuvat[(i+1)%len(elokuvat)].desc,size=(30, 26))], [sg.Stretch(),sg.Button("Selaa lisää elokuvia")]])]]
    window = sg.Window(title="Elokuvateatterin nykyiset elokuvat", layout=layout, size=(565, 500))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Valmis":
            break
        if event == "Selaa lisää elokuvia":
            window.close()
            return browse(i+2,log)
        if log == False:
            sg.popup("Kirjaudu sisään varaksesi paikan")
        elif event == "-FIRST-":
            reservewindow(elokuvat[i%len(elokuvat)])
        elif event == "-SECOND-":
            reservewindow(elokuvat[(i+1)%len(elokuvat)])
    window.close()

def menu_notloggedin():
    layout = [[sg.Stretch(),sg.Button("Kirjaudu")],
    [sg.Button("Selaa salien näytöksiä",size=(20,1))], [sg.Button("Selaa elokuvia",size=(20,1))], [sg.Stretch(),sg.Button("Valmis")]]
    window = sg.Window(title="Elokuvateatterin varausjärjestelmä", layout=layout, size=(400, 400))
    while True:
        event, values = window.read()
        if event == "Selaa elokuvia":
            browse(0,False)
        if event == "Kirjaudu":
            account, log = login()
            if log == True:
                window.close()
                return account
        if event == "Selaa salien näytöksiä":
            salivalinta("notloggedin")
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
    window.close()

def menu_loggedin():
    layout = [[sg.Stretch(),sg.Text("Elokuvateatterin varausjärjestelmä: Käyttäjä")],
        [sg.Button("Selaa salien näytöksiä")], 
        [sg.Button("Selaa elokuvia")],
        [sg.Button("Valmis")]]
    window = sg.Window(title="Elokuvateatterin varausjärjestelmä", layout=layout, size=(400, 400))
    while True:
        event, values = window.read()
        if event == "Selaa elokuvia":
            browse(0)
        if event == "Selaa salien näytöksiä":
            salivalinta()
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
    window.close()

def login():
    from Harjoitustyö import credentials
    layout = [[sg.Text("Käyttäjänimi",size = (9,1)),sg.Input("")], 
    [sg.Text("Salasana",size = (9,1)),sg.Input("")],
    [sg.Stretch(),sg.Button("Kirjaudu")]]
    window = sg.Window(title="Sisäänkirjautuminen", layout=layout, size=(300, 100))
    while True:
        event, values = window.read()
        if event == "Kirjaudu":
            if credentials.get(values[0],0) == values[1]:
                window.close()
                return values[0],True
            else:
                sg.popup("Incorrect credentials")
        if event == sg.WIN_CLOSED:
            window.close()
            return None,False
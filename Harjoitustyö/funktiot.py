import PySimpleGUI as sg
import copy
import pickle

class ElokuvaTeatteri:
    def __init__(self):
        self.salit = []
        self.elokuvat = []
        self.load()
    def asetasalit(self,salit):
        self.salit = salit
        self.save()
    def asetaelokuvat(self,elokuvat):
        self.elokuvat = elokuvat
        self.save()
    def lisääelokuva(self,elokuva):
        self.elokuvat.append(elokuva)
        self.save()
    def save(self):
        file = open('data.txt','wb')
        file.write(pickle.dumps(self.__dict__))
        file.close()
    def load(self):
        file = open('data.txt','rb')
        self.__dict__ = pickle.load(file)
        return self

class Sali:
    def __init__(self, ID, rivit, rivinpenkit):
        self.ID = ID
        self.rows = rivit
        self.columns = rivinpenkit
        self.shows = {x:[] for x in range(7)}
    def lisää_elokuva(self, elokuva, paiva, aloitusaika):
        kopio = copy.deepcopy(elokuva)
        if fit(aloitusaika,elokuva.kesto,[(x[0],x[1].kesto) for x in self.shows[paiva]]):
            self.shows[paiva].append((aloitusaika,kopio))
            kopio.size = (self.rows,self.columns)
            kopio.seats = [[0 for x in range(self.columns)] for x in range(self.rows)]
            return self
        return False
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
    sor = [(1441,0)] + [(tonum(z[0]),z[1]) for z in sorted(elokuvat, key = lambda x: x[0])][::-1] + [(719,0)]
    for i in range(len(sor)):
        if tonum(aika)+kesto < sor[i][0]:
            if sor[i+1][0]+sor[i+1][1] < tonum(aika):
                return True
    return False


def add_movie():
    from Harjoitustyö import teatteri
    layout = [[sg.Text("Elokuvan nimi",size=(10,1)),sg.Input()], 
    [sg.Text("Kuvaus",size=(10,1)),sg.Multiline()],
    [sg.Text("Kesto (mins)",size=(10,1)),sg.Spin([x for x in range(0,12)]),sg.Text("h",pad=(0,0)),sg.Spin([x for x in range(0,60)]),sg.Text("m",pad=(0,0))],
    [sg.Stretch(),sg.Button("Lisää elokuva",pad=((0,0),(100,0)))]]
    window = sg.Window(title="Elokuvan lisäys", layout=layout, size=(400, 250),modal=True)
    while True:
        event, values = window.read()
        if event == "Lisää elokuva":
            if values[0] == "" or (values[2] == '0' and values[3] == '0'):
                sg.popup("Jokin syötteistä ei ole täytetty")
            else:
                teatteri.lisääelokuva(Näytös(values[0],values[1],60*values[2]+values[3]))
                break
        if event == sg.WIN_CLOSED:
            break
    teatteri.save()
    window.close()

def tonum(num):
    return 60*int(num.split(":")[0])+ int(num.split(":")[1])

def getspace(kesto,num,num2):
    num = tonum(num)+int(kesto)
    num2 = tonum(num2)
    return (num2-num)

def editshow(sali,movie,user=False):
    layout = [[sg.Stretch(),sg.Text(f"Elokuva {movie[1].nimi}",pad=((0,0),(0,50))),sg.Stretch()],[sg.Stretch(),sg.Button("Poista tämä ohjelmistosta",key="poista"),sg.Stretch()],[sg.Stretch(),sg.Button("Muuta varauksia"),sg.Stretch()]]
    window = sg.Window(title="Ohjelmiston muutos", layout=layout, size=(400, 200),modal=True)
    while True:
        event, values = window.read()
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
        if event == "poista":
            from Harjoitustyö import teatteri
            teatteri.salit[sali.ID-1].shows[movie[2]].remove(movie[:2])
            teatteri.save()
            window.close()
            return True
        if event == "Muuta varauksia":
            showseats(movie[1],user,sali.ID,movie[2])
            break
    window.close()

def lisääohjelmasaliin(sali):
    päivät = ["Maanantai","Tiistai","Keskiviikko","Torstai","Perjantai","Lauantai","Sunnuntai"]
    elokuvat = getshows()
    layout = [[sg.Text("Elokuva",size=(7,1)),sg.Combo(values = [x for x in elokuvat])],[sg.Text("Päivä",size=(7,1)),sg.Combo(values = päivät)],
    [sg.Text("Aika",size=(7,1)),sg.Spin([x for x in range(12,24)]),sg.Text(":",pad=(0,0)),sg.Spin([x for x in range(0,60)])],
    [sg.Stretch(),sg.Button("Valmis",pad=((0,0),(70,0)))]]
    window = sg.Window(title="Lisää elokuva ohjelmistoon", layout=layout, size=(400, 200),modal=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if any([values[x] == '' for x in values]):
            sg.popup("Elokuva tarvitsee otsikon ja keston")
        elif event == "Valmis":
            movie = copy.deepcopy(values[0])
            päivä = päivät.index(values[1])
            aika = f"{values[2]}:{values[3]}"
            from Harjoitustyö import teatteri
            if teatteri.salit[sali.ID-1].lisää_elokuva(movie,päivä,aika) != False:
                teatteri.save()
                window.close()
                return True
            sg.popup("Elokuva ei mahdu tähän aikaan")
    window.close()


def näytäohjelmisto(sali,user):
    width = 18
    height = 3
    layout = [ [
        sg.Column(
            [[sg.Text("Maanantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[0]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(0,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[0]+ [('24:00',0)])[i+1][0]))),expand_x=True)] for i,x in enumerate(sali.shows[0])]
        ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Tiistai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[1]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(1,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[1]+ [('24:00',0)])[i+1][0]))),expand_x=True)] for i,x in enumerate(sali.shows[1])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Keskiviikko",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[2]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(2,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[2]+ [('24:00',0)])[i+1][0]))),expand_x=True)] for i,x in enumerate(sali.shows[2])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Torstai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[3]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(3,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[3]+ [('24:00',0)])[i+1][0]))),expand_x=True)] for i,x in enumerate(sali.shows[3])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Perjantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[4]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(4,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[4]+ [('24:00',0)])[i+1][0]))),expand_x=True)] for i,x in enumerate(sali.shows[4])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Lauantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[5]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(5,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[5]+ [('24:00',0)])[i+1][0]))),expand_x=True)] for i,x in enumerate(sali.shows[5])]
            ),
        sg.VSeparator(),
        sg.Column(
            [[sg.Text("Sunnuntai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[6]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(6,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[6]+ [('24:00',0)])[i+1][0]))),expand_x=True)] for i,x in enumerate(sali.shows[6])]
            )
            ]]
    if user == True:
        layout[0].append(sg.Column(
        [[sg.Button("Lisää ohjelmistoa\n saliin", size=(10,4),key="lisää")]]
            ,vertical_alignment='bottom')
        )
    window = sg.Window(title=f"Salin {sali.ID} ohjelmisto", layout=layout, size=(1330 if user == True else 1220, 830),modal=True)
    while True:
        event, values = window.read()
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
        if event == "lisää":
            if lisääohjelmasaliin(sali):
                layout = [ [sg.Column([[sg.Text("Maanantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[0]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(0,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[0]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[0])]),sg.VSeparator(),sg.Column([[sg.Text("Tiistai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[1]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(1,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[1]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[1])]),sg.VSeparator(),sg.Column([[sg.Text("Keskiviikko",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[2]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(2,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[2]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[2])]),sg.VSeparator(),sg.Column([[sg.Text("Torstai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[3]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(3,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[3]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[3])]),sg.VSeparator(),sg.Column([[sg.Text("Perjantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[4]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(4,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[4]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[4])]),sg.VSeparator(),sg.Column([[sg.Text("Lauantai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[5]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(5,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[5]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[5])]),sg.VSeparator(),sg.Column([[sg.Text("Sunnuntai",size=(width, height),pad=((0,0), (0,getspace(0,"12:00",(sali.shows[6]+ [('24:00',0)])[0][0]))))]] + [[sg.Button(x[1].nimi+"\n"+totime(tonum(x[0]),tonum(x[0])+x[1].kesto),key=x+(6,),size=(17,x[1].kesto//16),pad=((0,0), (0,getspace(x[1].kesto,x[0],(sali.shows[6]+ [('24:00',0)])[i+1][0]))))] for i,x in enumerate(sali.shows[6])])]]
                layout[0].append(sg.Column([[sg.Button("Lisää ohjelmistoa\n saliin", size=(10,4),key="lisää")]],vertical_alignment='bottom'))
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
                showseats(event[1],False,sali.ID,event[2])
    window.close()

def remove_movie():
    from Harjoitustyö import teatteri
    leng = len(teatteri.elokuvat)
    layout = [[sg.Column([[sg.Stretch(),sg.Text(f"Valitse elokuva",pad=((0,0),(0,50))),sg.Stretch()]] + 
    [[sg.Stretch()]+[sg.Button(f"{x.nimi}", key=x)]+[sg.Stretch()] for x in teatteri.elokuvat] +
     [[sg.Stretch(),sg.Button("Valmis",pad=((0,0),(90,0)))]], expand_y=True, expand_x=True)]]
    window = sg.Window(title="Valitse elokuva poistamiseen", layout=layout, size=(400, 190+leng*35),modal=True)
    while True:
        event, values = window.read()
        if event in teatteri.elokuvat:
            if checkwindow("Haluatko poistaa tämän elokuvan?"):
                teatteri.elokuvat.remove(event)
                teatteri.save()
                break
            else:
                break
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
    window.close()

def salivalinta(user = False):
    from Harjoitustyö import teatteri
    Salit = teatteri.salit
    layout = [[sg.Column([[sg.Stretch(),sg.Text(f"Näytä ohjelmisto salille",pad=((0,0),(0,50))),sg.Stretch()]] + 
    [[sg.Stretch()]+[sg.Button(f"Sali numero {x.ID}, koko {x.rows}x{x.columns}", key=x)]+[sg.Stretch()] for x in Salit] + 
    [[sg.Stretch(),sg.Button("Valmis",pad=((0,0),(210,0)))]], expand_x=True, expand_y=True)]]
    window = sg.Window(title="Valitse sali", layout=layout, size=(400, 400),modal=True)
    while True:
        event, values = window.read()
        if event in Salit:
            näytäohjelmisto(event,user)
        if event == "Valmis" or event == sg.WIN_CLOSED:
            break
    window.close()

def admin_menu():
    layout = [[sg.Column([[sg.Stretch(),sg.Text("Elokuvateatterin varausjärjestelmä: Admin",pad=((0,0),(0,50)))],
    [sg.Stretch(),sg.Button("Näytä salin ohjelmisto",size=(20,1)),sg.Stretch()],
    [sg.Stretch(),sg.Button("Lisää elokuva",size=(20,1)),sg.Stretch()],
    [sg.Stretch(),sg.Button("Poista elokuva ohjelmistosta",size=(20,1)),sg.Stretch()],
     [sg.Stretch(),sg.Button("Selaa elokuvia",size=(20,1),pad=((0,0),(0,160))),sg.Stretch()],
     [sg.Stretch(),sg.Button("Sulje",size=(10,1))]], expand_y=True, expand_x=True)]]
    window = sg.Window(title="Elokuvateatterin varausjärjestelmä", layout=layout, size=(400, 400), modal=True)
    while True:
        event, values = window.read()
        if event == "Näytä salin ohjelmisto":
            salivalinta(True)
        if event == "Lisää elokuva":
            add_movie()
        if event == "Poista elokuva ohjelmistosta":
            remove_movie()
        if event == "Selaa elokuvia":
            browse(0,"admin")
        if event == "Sulje" or event == sg.WIN_CLOSED:
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

def checkwindow(text):
    layout = [[sg.Text(text)],[sg.Button("Kyllä"),sg.Button("En")]]
    window = sg.Window(title="Varmistus", layout=layout, size=(300, 65),modal=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "En":
            window.close()
            return False
        if event == "Kyllä":
            window.close()
            return True

def adminseatwindow(movie,seat,salinum,paiva):
    from Harjoitustyö import teatteri
    layout = [[sg.Text("Muuta varausta tälle paikalle")],
    [sg.Button("Poista varaus"),sg.Button("Tämä penkki ei ole käytössä")]]
    window = sg.Window(title="Paikan varaus", layout=layout, size=(300, 70),modal=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Poista varaus":
            [x for x in teatteri.salit[salinum-1].shows[paiva] if x[1] == movie][0][1].seats[seat[0]][seat[1]] = 0
            teatteri.save()
            window.close()
            return 0
        if event == "Tämä penkki ei ole käytössä":
            [x for x in teatteri.salit[salinum-1].shows[paiva] if x[1] == movie][0][1].seats[seat[0]][seat[1]] = 1
            teatteri.save()
            window.close()
            return 1
    window.close()

def showseats(movie,user,salinum,paiva):
    from Harjoitustyö import teatteri
    layout = [[sg.Stretch(),sg.Text(f"Varaa paikka elokuvaan {movie.nimi}",pad=((0,0),(0,30))),sg.Stretch()]] + [[sg.Stretch()]+[sg.Button('',button_color=("green" if movie.seats[i][j] == 0 else "red"), size=(4, 2), key=(i,j), pad=((0,2),(0,2))) for j in range(movie.size[1])]+[sg.Stretch()] for i in range(movie.size[0])] + [[sg.Stretch(),sg.Text("Teatterin kangas on tässä",font="bold",pad=((0,0),(30,0))),sg.Stretch()]]
    window = sg.Window(title="Paikan varaus", layout=layout, size=(50+45*movie.size[1], 110+45*movie.size[0]),modal=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if user == True:
            num = adminseatwindow(movie,event,salinum,paiva)
            window[event].update(button_color=("green" if num == 0 else "red"))
        else:
            if movie.seats[event[0]][event[1]]:
                sg.popup("Paikka on jo varattu")
            elif checkwindow("Oletko varma että haluat varata tämän paikan?"):
                [x for x in teatteri.salit[salinum-1].shows[paiva] if x[1] == movie][0][1].varaapaikka(event[0],event[1],"user")
                teatteri.save()
                break
    window.close()

def getmovietimes(elokuva):
    from Harjoitustyö import teatteri
    Salit = teatteri.salit
    li = []
    for sali in Salit:
        for z in range(7):
            päivä = sali.shows[z]
            for x in päivä:
                if x[1].nimi == elokuva.nimi:
                    li.append((z,x[0],x[1],sali.ID))
    return sorted(sorted(li,key=lambda x : x[1]), key=lambda x : x[0])

def fixtime(num: str):
    hour,minute = num.split(":")
    if len(minute) == 1:
        minute = "0"+minute
    return hour+":"+minute

def reservewindow(movie):
    päivät = ["Maanantai","Tiistai","Keskiviikko","Torstai","Perjantai","Lauantai","Sunnuntai"]
    elokuvat = getmovietimes(movie)
    layout = [[sg.Stretch(),sg.Text(f"Varaa aika elokuvaan {movie.nimi}",pad=((0,0),(0,50))),sg.Stretch()]] + [[sg.Stretch()]+[sg.Button(f"{päivät[x[0]]} {fixtime(x[1])} Sali {x[3]}", key = x)]+[sg.Stretch()] for x in elokuvat]
    window = sg.Window(title="Ajan varaus", layout=layout, size=(400, 200+35*len(elokuvat)),modal=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        else:
            showseats(event[2],False,event[3],event[0])
            window.close()
    window.close()

def getshows():
    from Harjoitustyö import teatteri
    return teatteri.elokuvat

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
    window = sg.Window(title="Elokuvateatterin nykyiset elokuvat", layout=layout, size=(565, 500),modal=True)
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
    layout = [[sg.Column([[sg.Stretch(),sg.Button("Kirjaudu",size=(10,1),pad=((0,0),(0,50)))],
    [sg.Stretch(),sg.Button("Selaa salien näytöksiä",size=(20,1)),sg.Stretch()], [sg.Stretch(),sg.Button("Selaa elokuvia",size=(20,1),pad=((0,0),(0,210))),sg.Stretch()], [sg.Stretch(),sg.Button("Sulje",size=(10,1))]], expand_y=True, expand_x=True)]]
    window = sg.Window(title="Elokuvateatterin varausjärjestelmä", layout=layout, size=(400, 400),modal=True)
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
        if event == "Sulje" or event == sg.WIN_CLOSED:
            break
    window.close()

def menu_loggedin():
    layout = [[sg.Column([[sg.Stretch(),sg.Text("Elokuvateatterin varausjärjestelmä: Käyttäjä",pad=((0,0),(0,50)))],
    [sg.Stretch(),sg.Button("Selaa salien näytöksiä",size=(20,1)),sg.Stretch()],
     [sg.Stretch(),sg.Button("Selaa elokuvia",size=(20,1),pad=((0,0),(0,210))),sg.Stretch()],
     [sg.Stretch(),sg.Button("Sulje",size=(10,1))]], expand_y=True, expand_x=True)]]
    window = sg.Window(title="Elokuvateatterin varausjärjestelmä", layout=layout, size=(400, 400),modal=True)
    while True:
        event, values = window.read()
        if event == "Selaa elokuvia":
            browse(0)
        if event == "Selaa salien näytöksiä":
            salivalinta()
        if event == "Sulje" or event == sg.WIN_CLOSED:
            break
    window.close()

def login():
    from Harjoitustyö import credentials
    layout = [[sg.Text("Käyttäjänimi",size = (9,1)),sg.Input("")], 
    [sg.Text("Salasana",size = (9,1)),sg.Input("")],
    [sg.Stretch(),sg.Button("Kirjaudu",pad=((0,0),(10,0)))]]
    window = sg.Window(title="Sisäänkirjautuminen", layout=layout, size=(300, 100),modal=True)
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
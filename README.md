# Dokumentaatio

## Työn aihe ja kuvaus
Elokuvateatterin varausjärjestelmä, jossa graafinen käyttöliittymä

Työn käyttämät tiedot talletetaan `data.txt` tiedostoon.

## Työn ratkaisuperiaate
Työ ratkaistaan määrittelemällä kolme luokkaa: `Näytös`, `Sali` ja `Elokuvateatteri`

ElokuvaTeatteri luokka sisältää Näytös ja Sali objektit. Luokkaa käytetään ohjelmiston säästönä ja ElokuvaTeatteri objekti talletetaan tiedostoon.

Sali objektit sisältävät aikataulun ja salin koon. Aikataulu sisältää kopioita Näytös objekteista ja alkuajan jokaiselle näytökselle.

Näytös objekti sisältää listan paikoista, joita voi varata, elokuvan pituuden, nimen ja kuvauksen. Koska Saleissa olevat Näytös objektit ovat kopioita, on jokaisella näytöksellä omat penkit, joita voi varata.

Käyttöliittymä on rakennettu erilaisista funktioista, jotka aloittavat uuden ikkunan. Funktiot kutsuvat toisiaan jolloin käyttöliittymässä pystyy liikkumaan eteenpäin.

## Työn rakenne: miten se on jaettu funktioihin
menu_notloggedin -> menu ennen kirjautumista

menu_loggedin -> menu käyttäjälle

admin_menu -> menu ylläpitäjälle

login -> valikko, jossa voi kirjautua ylläpitäjänä tai käyttäjänä

browse -> selaa ElokuvaTeatterin näytöksiä

getshows -> palauttaa näytökset

reservewindow -> Näyttää ikkunan jossa on kaikki tietyn elokuvan näytökset

fixtime -> Muuttaa ajan tavalliseen muotoon. "19:0" -> 19:00

getmovietimes -> Palauttaa kaikki ajat tietylle näytökselle kaikissa saleissa

showseats -> Näyttää vapaat ja varatut paikat tietylle näytökselle

checkwindow -> Varmistus siitä että käyttäjä on varma että haluaa tehdä jotain

totime -> muuttaa int tyyppisen ajan luettavaan muotoon. 720 -> "12:00"

salivalinta -> Näyttää ikkunan jossa on salit

näytäohjelmisto -> Näyttää ohjelmiston tietylle salille

editshow -> Ikkuna, jossa ylläpitäjä voi valita miten näytöstä muutetaan

getspace -> palauttaa paljonko väliä näytösten välillä on oltava piirretyssä ikkunassa

tonum -> muuttaa str tyyppisen ajan int tyyppiseksi. "12:00" -> 720

lisääohjelmasaliin -> Ikkuna, jossa ylläpitäjä voi valita näytöksen, päivän ja ajan lisättäväksi tiettyyn saliin

adminseatwindow -> Ylläpitäjän ikkuna jossa voi muuttaa tietyn näytöksen paikkojen varauksia

remove_movie -> Ikkuna jossa ylläpitäjä voi poistaa näytöksen ohjelmistosta

add_movie -> Ikkuna jossa voi lisätä uuden näytöksen ohjelmistoon

fit -> tarkistaa mahtuuko näytös annetulle ajalle

## Mahdolisten ulkoisten kirjastojen käyttö
* Graafisen käyttöliittymän rakentamiseen on käytetty kirjastoa nimeltä `PySimpleGUI`
* Luokkien kopioimiseen on käytetty `copy` kirjastoa
* Ohjelman tietojen tallentamiseen ja lataamiseen käytetään `pickle` kirjastoa

## Työn suoritus
* Ohjelma suoritetaan suorittamalla `Harjoitustyö.py` tiedoston.
* Kirjautuminen tapahtuu painalla `kirjaudu` nappia ja kirjautumalla joko käyttäjänä `user, user` tai ylläpitäjänä `admin, admin` 
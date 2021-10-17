## Ravintolasovellus
Sovelluksessa näkyy valitun kaupungin ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.
[dokumentaatio](https://github.com/EternalAzure/Ravintolasovellus/blob/main/dokumentaatio.md)
### Nykytila:
#### Autentikaatio ja kirjautuminen
Kokonaisuudessaan toteutettu
- [x] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- [x] Uloskirjautuneen istuntoa ei voi väärin käyttää
#### Karta
- [x] Käyttäjä näkee ravintolat kartalla
- [x] Käyttäjä voi klitata ravintolaa kartalla ja se tarjoaa linkkiä ravintolan info sivulle
- [x] Käyttäjä voi klikata ravintolan 'Näytä kartalla' ja sivu ohjaa kartalle ja kartta kohdistaa oikeaan sijaintiin
- [x] Käyttäjä voi valita kaupungin, jonka ravintolat näytetään
- [ ] Näyttää joitain tietoja kartan info window ikkunassa.
#### Ylläpito
- [x] Voi rekisteröityä osoitteessa '/admin', jonne ei ole linkkiä ja reitti on IP suojattu.
- [x] Voi poistaa ravintolan
- [x] Voi poistaa tunnisteen ravintolalta
- [x] Voi poistaa käyttäjän arvion
- [x] Määrittää linkin ravintolan sivuille
#### Käyttäjä
- [x] Voi antaa arvion (tähdet ja kommentti) ravintolasta
- [x] Voi lukea arvioita
- [x] Voi lisätä ravintolan
- [x] Voi vaihtaa kaupunkia istunnon ajaksi
- [x] Voi päivittää ravintolan tietoja
- [x] Näkee järjestetyn listan ravintoloista
#### Haku
##### Tunniste
- [x] Voi etsiä ravintolat tunnisteen perusteella
- [x] Tiukka hakumoodi
- [x] Löyhä hakumoodi
##### Nimi
- [x] Voi hakea ravintolat nimen perusteella
<br>
<br>
<p>https://polar-scrubland-57061.herokuapp.com/
admin:admin <br>
</p>
<br>

<img src="https://github.com/EternalAzure/Ravintolasovellus/blob/main/pictures/index.jpg" height="502" />

### Oivalluksia

#### Ongelma
Projektin kehitykseen kuului vaihe, jossa kommunikaatio serverin kanssa toteutettiin lähes yksinomaan lomakkeiden kautta. Ongelma lomakkeissa on se, että pyynnön käsittelevän ```@app.route``` sisältävän funktion (myöhemmin 'route') on joko suoritettava rendere_template() tai muuten palautettava html. Tämä johtaa nykyisen sivun menetykseen uuden sivun latauksena tai nykyisen sivun uudelleen latauksena. Näistä jälkimmäinen on usein epätoivottavaa, sillä se johtaa muuttujien sekä ```style="display: '' / style="display: none"``` tyylillä toteutettujen "näkymien" nollaantumiseen.

#### Ratkaisu
Tämä johti lomakkeiden hylkäämiseen ja tiedon hakuun javascriptin kautta API kutsuilla sekä localStoragen käyttöönottoon.

#### Ongelma
Nyt projektissa on kaksi viestintäväylää selaimen ja serverin välillä: API ja lomakkeet. Olisi selkeämpää, jos toteutuksista valittaisiin vain toinen. Lisäksi toteutusten välillä on päällekkäisyyksiä, joka johtaa toisteiseen koodiin.

#### Ratkaisu
Siirrytään yksinomaan API kutsuihin ja siirretään API omaan ```.py``` tiedostoonsa erilleen sivut näyttävistä routeista.

#### Ongelmia
HTML koodissa toistuu samat elementit, Globaalit muuttujat ovat tehokkaita tiedon välittäjiä, mutta tiedostoilla ei ole kapsulointia ja muuttujan voi lukea ja yli kirjoittaa toisesta ```.js``` tiedostosta, joka on ladattu samalle HTML sivulle. 

#### Ratkaisu
Siirrytään käyttämään FrameWorkkiä kuten React, joka tukee komponentteja. Client puolen sovellus eristää ```.js``` tiedostot toisistaan.

### Kurssista
Kurssi on ollut näkökulmastani äärimmäisen onnistunut. Olen oppinut sekä yksittäisiä web teknologioita, että saanut syvempää ymmärrystä olemassa olevista suunnittelu kuvioista (design patterns). Olen yhdistänyt oppimaani Full Stack kurssiin. Olen oppinut Python Flaskin käyttöä, Jinja2 kaavoja ja layout kuvion, jossa pohja tiedostoa laajennetaan käyttäen ```{% extends 'layout.html' %}```, Herokua, Postgres, CSS ja HTML. Erittäin hyödyllistä oli ottaa käyttöön Photon niminen valmis nettisivu ratkaisu, jonka kautta opin suuret määrät muotoilullisia asioita ja niiden toteutuksesta.

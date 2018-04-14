# Recommender demo API

Repozitorij za back-end sustava za preporučavanje slika na temelju njihovog sadržaja. Poslužitelj je pisan u `Python` programskom jeziku (verzija 3.6.5), a oslanja se na `Django` (2.0.3) radni okvir. Svi podaci aplikacije pohranjuju se u `PostgreSQL` bazu podataka (verzija 9.5.12).

Razvijani sustav se sastoji od [SPA](https://en.wikipedia.org/wiki/Single-page_application "Single Page Application") klijenta,
[REST API](https://en.wikipedia.org/wiki/Representational_state_transfer "Representational state transfer") poslužitelja i [AWS S3](https://aws.amazon.com/s3/ "Amazon Web Services Simple Storage Service") usluge za pohranu i posluživanje podataka.

## Struktura projekta
 
 Struktura bitnih datoteka projekta prikazana je u nastavku: 
 
 ```
 .
│   README.md
└───app                  ....... Root for Django web aplication served.
│   └───...         
└───project              ....... Root for Django server configuration.
│   └───...         
└───scripts              ....... Root for additional utility scripts used.
│   │   └───data         ....... 
│   │   │   └───...
│   │   └───notebooks    ....... Jupyter notebooks for setting up images in the database.
│   │   │   └───...
│   │   └───...
└───static               ....... Root of static files sereved.
    └───...         
 ```

## Postavljanje

Instrukcije za postavljanje pisane su za Linux ( Ubuntu 16.04.4 LTS ). Korisnici drugih operacijskih sustava mogu pronaći ekvivalentne naredbe za svoja računala na webu.

### Preuzimanje 

Kod ovog poslužitelja može se preuzeti putem komandne linije na računalu koje ima postavljen git sustav za verzioniranje idućim naredbama: 

```
mkdir -p ~/Documents/gitrepos && cd "$_"
git clone https://github.com/vribic/recommender-demo-api.git && cd recommender-demo-api/
```

Alternativno kod je moguće preuzeti kao .zip datoteku pritiskom na gumb `Clone or download` te `Downlaod ZIP`.

### Konfiguracija

Nakon što je kod preuzet potrebno je instalirati dodatne pakete. Preporuča se stvaranje novog python virtualnog okruženja, aktivacija istog i instalacija potrebnih paketa naredbama:

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Nakon što su svi paketi uspješno instalirani potrebno je stvoriti tekstualnog naziva `.env` idućeg formata : 

```
SECRET_KEY=<SECRET_KEY*>
DEBUG=True
ALLOWED_HOSTS=.localhost,.herokuapp.com
DATABASE_URL=<DATABASE_URL*>
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID*>
AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY*>
AWS_STORAGE_BUCKET_NAME=<AWS_STORAGE_BUCKET_NAME*>
```

`<SECRET_KEY*>` : Automatski generirani tajni ključ Django projekta. Za potrebe isprobavanja sustava potrebno je generirati novi ključ (npr. [ovdje](https://www.miniwebtool.com/django-secret-key-generator/) ).

`<DATABASE_URL**>` : Url za spajanje na bazu podataka, koja za potrebe testiranja mora biti lokalno postavljena, dok se za deployment na `Heroku` platformi automatski konfigurira u varijablama okruženja. Format urla je idući: `postgresql://[user[:password]@][netloc][:port][/dbname]` \*.

`<AWS_ACCESS_KEY_ID*> , <AWS_SECRET_ACCESS_KEY*> , <AWS_STORAGE_BUCKET_NAME*>` : podaci preuzeti sa AWS S3 poslužitelja. Detaljne informacije o postavljanju cloud storagea možete pronaći [ovdje](https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html). 

*\*Note:* Korisnici koji nemaju postavljenu PostgreSQL bazu podataka na svom računalu mogu to učiniti prateći korake [ovdje](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04). Postgre je pretpostavljena baza podataka na Heroku poslužitelju. Ukoliko korisnik želi koristiti drugu bazu potrebno je promjeniti postavke na Heroku poslužitelju. Više o tome korisnik može pronaći na internetu. 


### Pokretanje

Jednom kad su svi paketi postavljeni i datoteke konfigurirane sve što preostaje je izvršiti migracije Django modela u bazu podataka i pokrenuti server : 

```
python manage.py migrate
python manage.py runserver
```

Time će server postati funkcionalan i spreman za posluživanje. Kako baza podataka nije postavljena u ovaj repozitorij korisnik će morati sam dopuniti bazu podataka i postaviti slike na mrežni poslužitelj. 


## Postavljanje slika

Idući odjeljak prolazi kroz nužne korake postavljanja slika u radno okruženje i popunjavanje baze podataka potrebnim informacijama. 

Prvi korak je preuzimanje podataka korištenih na projektu na idućem [link]( http://test-bucket-vribic.s3.amazonaws.com/django-project/scripts/data.zip). Podaci su u obliku zip datoteke koja se mora postaviti u `scripts/` direktorij preuzetog projekta.

Jednom kad su podaci raspakirani potrebno ih je registrirati u bazi i pripremiti za posluživanje. Projekt sarži potrebni program u obliku Jupyter bilježnice u kojem je moguće izvršiti upravo to. Kako bi se Jupyter okruženje povezalo s Django radnim okruženjem potrebno je pokrenuti iduću naredbu u vršnom direktoriju projekta: 

`python manage.py shell_plus --notebook`

Zatim korisnik mora kroz web sučelje navigirati do datoteke `./scripts/notebooks/DatabasePopulate.ipynb`. U izbornoj traci dovoljno je pokrenuti `Cells/Run all`.

Jednom kad je program završio sa izvršavanjem sakupljene slike je potrebno poslati na cloud storage. Projekt sadrži paket za automatsko migriranje statičkih podataka na AWS servis. Korisnik još samo moram porkrenuti naredbu : 

`python manage.py collectstatic`

## O projektu

Repozitorij je dio projekta razvijanog za Rektorovu nagradu 2017./18 pod nazivom "Ekstrahiranje značajki slika pomoću dubokog učenja u svrhu poboljšanja sustava preporuke slika".

Autori projekta su [Toni Vlaić](https://github.com/Mungosin) i [Viran Ribić](https://github.com/vribic), pod vodstvom mentora prof. dr. [Marin Šilić](https://www.fer.unizg.hr/marin.silic). 

## Vanjski linkovi

Repozitorij front-end koda aplikacije : [link](https://github.com/vribic/recommender-demo)

Repozitorij teksta rada : [link](https://github.com/Mungosin/Rektorova)

Link na web aplikaciju posluženu na Heroku platformi : [demo aplikaicije](https://recommender-demo.herokuapp.com/login).

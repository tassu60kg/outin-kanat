# outin-kanat

[Backlog](https://docs.google.com/spreadsheets/d/1uv1LO1OkqLnA6712Gbt_XNfljoTwxtXnqFgYwr6e3Qw/edit?gid=0#gid=0)

Definition of done = koodi toimii, testit menevät läpi, koodi on siistiä (pylint), kaveri katselmoi koodin.

[![CI](https://github.com/tassu60kg/outin-kanat/actions/workflows/main.yml/badge.svg)](https://github.com/tassu60kg/outin-kanat/actions/workflows/main.yml)

## Asennus- ja käyttöohje

PostgreSQL asennusohjeet:

Voit luoda PostgreSQL:ään oman tietokannan seuraavasti

```
$ psql
user=# CREATE DATABASE <tietokannan-nimi>;
```

Repositorio asennusohjeet:

Luo hakemisto tälle repolle esim:

```
mkdir testi
```

ja luo reitti sille:

```
cd testi
```

Kloonaa repositorio omalle koneellesi komennolla

```
git clone git@github.com:tassu60kg/outin-kanat.git
```

Tämän jälkeen avaa reitti hakemistoon

```
cd testi/src
```

(näet komennolla ls, oletko repositiossa, pitäisi näkyä kaikki sovelluksen osat esim app.py, schema.sql yms. Jos ei näy, niin sinun pitää mennä ns syvemmälle, avaa siis tiedosto koneella ja katso reitti, se voi olla esim. Documents/testi/repon_nimi/src ja yritä sitten: cd Documents/testi/repon_nimi/src)

Luo myös oma .env kansio tähän lokaaliin repoon, jonne teet oman salaisen avaimen seuraavasti:

```
SECRET_KEY=(itse luomasi sercetkey)
```

Lisää .env kansioon myös tekemäsi tietokannan osoite seuraavasti, esim: jos loit tietokannan nimeltä testi, tulisi uudeksi tietokannan osoitteeksi postgresql:///testi

```
DATABASE_URL=postgresql:///testi
```

Luo schemat tietokantaan:

```
psql -d (oman tietokannan nimi) < schema.sql
```

Aja sitten pohjakansiossa:

```
poetry install
```

virtuaaliympäristön saa auki:

```
eval $(poetry env activate)
```

Käynnistä sovellus:

```
flask run
```

# Elections Scraper

Třetí projekt pro Python Akademii od Engeta.

## Popis projektu

Tento projekt slouží k extrahování výsledků voleb do Poslanecké sněmovny Parlamentu ČR z roku 2017 z webu https://volby.gov.cz/.

Program stáhne výsledky hlasování pro všechny obce zvoleného územního celku a uloží je do CSV souboru.

## Instalace knihoven

Projekt byl vytvořen v Pythonu 3.13.6.

Nejdříve vytvořte a aktivujte virtuální prostředí.

Potřebné knihovny nainstalujete pomocí příkazu:

```bash
pip install -r requirements.txt
```

## Spuštění projektu

Program se spouští pomocí dvou argumentů:

1. Odkaz na zvolený územní celek.
2. Název výstupního CSV souboru.

Příklad spuštění:

```bash
python main.py "https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv
```

## Ukázka projektu

### Průběh programu

```text
Stahuji obec: Benešov
Stahuji obec: Bernartice
...
Hotovo.
Výsledky byly uloženy do: vysledky_benesov.csv
```

### Částečný výstup

```text
code,location,registered,envelopes,valid,...
529303,Benešov,13104,8485,8437,...
532568,Bernartice,191,148,148,...
530743,Bílkovice,170,121,118,...
```

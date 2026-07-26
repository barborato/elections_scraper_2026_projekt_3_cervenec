import csv
import sys

import requests
from bs4 import BeautifulSoup


def download_page(url: str) -> str:
    """Stáhne obsah webové stránky."""
    response = requests.get(url, timeout=30)
    return response.text


def get_soup(url: str) -> BeautifulSoup:
    """Převede staženou stránku na objekt BeautifulSoup."""
    html = download_page(url)
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_municipalities(soup: BeautifulSoup) -> list:
    """Najde kódy, názvy a odkazy všech obcí."""
    municipalities = []

    for row in soup.find_all("tr"):
        code_cell = row.find("td", class_="cislo")
        name_cell = row.find("td", class_="overflow_name")

        if code_cell and name_cell:
            link = code_cell.find("a")

            municipality = {
                "code": code_cell.text.strip(),
                "location": name_cell.text.strip(),
                "link": (
                    "https://volby.gov.cz/pls/ps2017nss/"
                    + link["href"]
                )
            }

            municipalities.append(municipality)

    return municipalities


def get_results(soup: BeautifulSoup) -> dict:
    """Získá účast a hlasy pro jednotlivé strany."""
    registered = soup.find(
        "td", headers="sa2"
    ).text.replace("\xa0", "")

    envelopes = soup.find(
        "td", headers="sa3"
    ).text.replace("\xa0", "")

    valid = soup.find(
        "td", headers="sa6"
    ).text.replace("\xa0", "")

    results = {
        "registered": registered,
        "envelopes": envelopes,
        "valid": valid
    }

    for row in soup.find_all("tr"):
        party_name = row.find("td", class_="overflow_name")
        party_votes = row.find(
            "td",
            headers=["t1sa2 t1sb3", "t2sa2 t2sb3"]
        )

        if party_name and party_votes:
            name = party_name.text.strip()
            votes = party_votes.text.replace("\xa0", "")
            results[name] = votes

    return results


def scrape_municipality(municipality: dict) -> dict:
    """Vytvoří jeden výsledný řádek pro obec."""
    detail_soup = get_soup(municipality["link"])
    results = get_results(detail_soup)

    row = {
        "code": municipality["code"],
        "location": municipality["location"]
    }

    row.update(results)
    return row


def scrape_all(municipalities: list) -> list:
    """Stáhne výsledky všech obcí."""
    all_results = []

    for municipality in municipalities:
        print("Stahuji obec:", municipality["location"])

        result = scrape_municipality(municipality)
        all_results.append(result)

    return all_results


def save_csv(data: list, filename: str) -> str:
    """Uloží výsledky do CSV souboru."""
    headers = data[0].keys()

    with open(
        filename,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    return filename


def check_arguments(arguments: list) -> bool:
    """Zkontroluje počet a základní podobu argumentů."""
    if len(arguments) != 3:
        print("Chyba: zadej URL adresu a název CSV souboru.")
        return False

    if not arguments[1].startswith(
        "https://volby.gov.cz/pls/ps2017nss/ps32"
    ):
        print("Chyba: první argument není správný odkaz.")
        return False

    if not arguments[2].endswith(".csv"):
        print("Chyba: název souboru musí končit .csv.")
        return False

    return True


def main() -> None:
    """Spustí celý program."""
    if not check_arguments(sys.argv):
        return

    url = sys.argv[1]
    filename = sys.argv[2]

    main_soup = get_soup(url)
    municipalities = get_municipalities(main_soup)

    if not municipalities:
        print("Chyba: na stránce nebyly nalezeny žádné obce.")
        return

    data = scrape_all(municipalities)
    saved_file = save_csv(data, filename)

    print("Hotovo.")
    print("Výsledky byly uloženy do:", saved_file)


if __name__ == "__main__":
    main()
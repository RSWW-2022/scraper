from bs4 import BeautifulSoup
import requests
import csv


def main():
    with open('tours.csv', mode='w', encoding="utf8", newline='') as csvfile:
        fieldnames = ["id", "destination", "description", "region", "hotel_name", "offer_advantages"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        # Download html
        response = requests.get(
            "https://www.itaka.pl/wyniki-wyszukiwania/wakacje/?view=offerList&package-type=wczasy&adults=2&date-from=2022-04-09&order=popular&total-price=0&page=1&currency=PLN")

        # Parse html
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for tours
        for id, tour in enumerate(soup.find_all("h3", class_="header_title")):
            url = tour.find('a', href=True)

            # Go to the tour page
            response_2 = requests.get("https://www.itaka.pl" + url['href'])

            # Parse html
            soup2 = BeautifulSoup(response_2.text, 'html.parser')

            # Hotel
            hotel_name = soup2.find("span", class_="productName-holder").find('h1').text.replace('<h1>', '')

            # Offer advantages
            offer_advantages = soup2.find("td", class_="event-assets hidden-xs").find_all("li")
            offer_advantages = [x.text.replace('<li>', '') for x in offer_advantages]

            destination = "1"
            description = "1"
            region = "1"

            writer.writerow({
                "id": id,
                "destination": destination,
                "description": description,
                "region": region,
                "hotel_name": hotel_name,
                "offer_advantages": offer_advantages
            })

            print(id)


if __name__ == "__main__":
    main()

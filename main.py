import datetime
import random

from bs4 import BeautifulSoup
import requests
import csv


def randdate():
    start_date = datetime.date(2022, 5, 1)
    end_date = datetime.date(2022, 8, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


# Information about hotel and available transport and booking options
def scraper(filename, page):
    with open(filename, mode='w', encoding="utf8", newline='') as csvfile:
        fieldnames = ["id", "hotel_name", "departure_destinations", "arrival_destination", "room_types", "board",
                      "type_of_transport"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        # Download html
        response = requests.get(
            "https://www.itaka.pl/wyniki-wyszukiwania/wakacje/?view=offerList&package-type=wczasy&adults=2&children-age=2017-04-23&order=popular&total-price=0&page={}&currency=PLN".format(
                page))
        # Parse html
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for tours
        for id, tour in enumerate(soup.find_all("h3", class_="header_title")):
            try:
                url = tour.find('a', href=True)

                # Go to the tour page
                response_2 = requests.get("https://www.itaka.pl" + url['href'])

                # Parse html
                soup2 = BeautifulSoup(response_2.text, 'html.parser')

                # Hotel
                hotel_name = soup2.find("span", class_="productName-holder").find('h1').text.replace('<h1>', '')

                # Offer advantages
                # offer_advantages = soup2.find("td", class_="event-assets hidden-xs").find_all("li")
                # offer_advantages = [x.text.replace('<li>', '') for x in offer_advantages]

                # Departure Destinations
                departure_destinations = soup2.find("select", id="departure-select").find_all("option")
                departure_destinations = [x.text.replace('\n', '') for x in departure_destinations]
                departure_destinations = ",".join(departure_destinations)

                # Arrival destination
                arrival_destination = soup2.find("span",
                                                 class_="destination-title destination-country-region").text.replace(
                    '\n', '')

                # Room types
                room_types = soup2.find("select", id="room-select").find_all("option")
                room_types = [x.text.replace('\n', '').split("2")[0].split("3")[0].strip() for x in room_types]
                room_types = list(dict.fromkeys(room_types))
                room_types = ",".join(room_types)

                # Board
                board_types = soup2.find("select", id="food-select").find_all("option")
                board_types = [x.text.replace('\n', '') for x in board_types]
                board_types = ",".join(board_types)

                writer.writerow({
                    "id": id,
                    "hotel_name": hotel_name,
                    "departure_destinations": departure_destinations,
                    "arrival_destination": arrival_destination,
                    "room_types": room_types,
                    "board_types": board_types
                })

                print("{}; {}; {}; {}; {}; {}".format(id, hotel_name, departure_destinations, arrival_destination,
                                                      room_types, board_types))
            except:
                print("Fail")


def insert():
    with open("SQL_scripts/tour.sql", mode='a', encoding="utf8") as f:
        f.write('INSERT INTO "tour" ("hotel_name", "region", "own_transport", "board_types") VALUES\n')

    with open("SQL_scripts/flight.sql", mode='a', encoding="utf8") as f:
        f.write(
            'INSERT INTO "flight" ("flight_date", "departure_destination", "arrival_destination", "number_of_seats") VALUES\n')

    with open("SQL_scripts/room.sql", mode='a', encoding="utf8") as f:
        f.write('INSERT INTO "room" ("hotel_name", "room_type") VALUES\n')

    with open("SQL_scripts/room_availability.sql", mode='a', encoding="utf8") as f:
        f.write('INSERT INTO "room_availability" ("room_id","date") VALUES\n')

    with open("scraper.csv", 'r', encoding="utf8", newline='') as f:
        csvreader = csv.reader(f, delimiter=';')
        header = next(csvreader)
        for id, row in enumerate(csvreader):
            hotel_name = row[1]
            departure_destinations = row[2].split(',')
            arrival_destination = row[3]
            room_types = row[4].split(',')
            board_types = row[5].split(',')
            own_transport = False
            if "Dojazd własny" in departure_destinations:
                own_transport = True
                departure_destinations.remove("Dojazd własny")

            tour(hotel_name, arrival_destination, board_types, own_transport)

            if len(departure_destinations):
                flight(departure_destinations, arrival_destination, 50)

            room(hotel_name, room_types, 50)


def tour(hotel_name, region, board_types, own_transport):
    with open("SQL_scripts/tour.sql", mode='a', encoding="utf8") as f:
        board_types = ",".join(board_types)
        f.write("('{}', '{}', '{}', '{}'),\n".format(hotel_name, region, own_transport, board_types))


def flight(departure_destinations, arrival_destination, size):
    with open("SQL_scripts/flight.sql", mode='a', encoding="utf8") as f:
        for i in range(0, size):
            number_of_seats = random.randint(5, 30)
            flight_date = randdate()
            index = random.randint(0, len(departure_destinations) - 1)
            departure_destination = departure_destinations[index]
            f.write("('{}', '{}', '{}', {}),\n".format(flight_date, departure_destination, arrival_destination,
                                                       number_of_seats))
            flight_date = randdate()
            f.write("('{}', '{}', '{}', {}),\n".format(flight_date, arrival_destination, departure_destination,
                                                       number_of_seats))


def room(hotel_name, room_types, size):
    with open("SQL_scripts/room.sql", mode='a', encoding="utf8") as f:
        for i in range(0, size):
            index = random.randint(0, len(room_types) - 1)
            room_type = room_types[index]
            f.write("('{}', '{}'),\n".format(hotel_name, room_type))
            room_availability(100)
            global room_id
            room_id += 1


def room_availability(size):
    with open("SQL_scripts/room_availability.sql", mode='a', encoding="utf8") as f:
        for i in range(0, size):
            date = randdate()
            f.write("('{}', '{}'),\n".format(room_id, date))


room_id = 1


def main():
    # scraper('scraper.csv', 10)
    insert()


if __name__ == "__main__":
    main()

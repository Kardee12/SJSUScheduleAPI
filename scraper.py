import requests
from bs4 import BeautifulSoup

import json
import requests
from bs4 import BeautifulSoup
import re

class scrapeData():
    def scrapeData(self):
        # Make a GET request to the webpage containing the class schedule table
        url = "https://www.sjsu.edu/classes/schedules/fall-2023.php"
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the class schedule table
        table = soup.find("table", id="classSchedule")
        class_schedule = []

        for row in table.find_all("tr"):
            if row.find("th"):
                continue
            columns = row.find_all("td")

            department, course, section = columns[0].text.strip().split(' ', 2)
            section = re.findall(r'\d+', section)[0]
            class_number = columns[1].text.strip()
            mode_of_instruction = columns[2].text.strip()
            course_title = columns[3].text.strip()
            satisfies = columns[4].text.strip()
            units = columns[5].text.strip()
            class_type = columns[6].text.strip()
            days = columns[7].text.strip()
            times = columns[8].text.strip()
            instructor = columns[9].text.strip()
            location = columns[10].text.strip()
            dates = columns[11].text.strip()
            open_seats = columns[12].text.strip()
            notes = columns[13].text.strip()

            entry = {
                "department": department,
                "course": course,
                "section": section,
                "class_number": class_number,
                "mode_of_instruction": mode_of_instruction,
                "course_title": course_title,
                "satisfies": satisfies,
                "units": units,
                "class_type": class_type,
                "days": days,
                "times": times,
                "instructor": instructor,
                "location": location,
                "dates": dates,
                "open_seats": open_seats,
                "notes": notes
            }

            class_schedule.append(entry)

        return class_schedule

    def to_json(self):
        data = self.scrapeData()
        return data

# # Usage example
# data_scraper = scrapeData()
# json_data = data_scraper.to_json()
# print(json_data)


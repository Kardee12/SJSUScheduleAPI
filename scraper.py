from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
from pydantic import BaseModel

class CourseScheduleEntry(BaseModel):
    term: str
    department: str
    course: str
    section: str
    class_number: str
    mode_of_instruction: str
    course_title: str
    satisfies: str
    units: int
    class_type: str
    days: str
    times: str
    instructor: str
    location: str
    dates: str
    open_seats: int
    notes: str

class ScrapeData:
    def to_json(self, data):
        return [entry.dict() for entry in data]

    def scrapeData(self):
        # Make a GET request to the webpage containing the class schedule table
        url = "https://www.sjsu.edu/classes/schedules/fall-2023.php"
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", id="classSchedule")
        class_schedule = []

        for row in table.find_all("tr"):
            if row.find("th"):
                continue
            columns = row.find_all("td")

            department, course, section = columns[0].text.strip().split(" ", 2)
            section = re.findall(r"\d+", section)[0]
            class_number = columns[1].text.strip()
            mode_of_instruction = columns[2].text.strip()
            course_title = columns[3].text.strip()
            satisfies = columns[4].text.strip()
            units = int(float(columns[5].text.strip()))
            class_type = columns[6].text.strip()
            days = columns[7].text.strip()
            times = columns[8].text.strip()
            instructor = columns[9].text.strip()
            location = columns[10].text.strip()
            dates = columns[11].text.strip()
            open_seats = int(float(columns[12].text.strip()))
            notes = columns[13].text.strip()

            term = self.get_term(dates)
            entry = CourseScheduleEntry(
                term=term,
                department=department,
                course=course,
                section=section,
                class_number=class_number,
                mode_of_instruction=mode_of_instruction,
                course_title=course_title,
                satisfies=satisfies,
                units=units,
                class_type=class_type,
                days=days,
                times=times,
                instructor=instructor,
                location=location,
                dates=dates,
                open_seats=open_seats,
                notes=notes,
            )
            class_schedule.append(entry)

        print("Scraping Class Schedule...")
        return class_schedule

    @staticmethod
    def get_term(dates):
        start_date, end_date = dates.split("-")
        start_month = int(start_date.split("/")[0])
        today = datetime.now()
        year = today.year

        if 1 <= start_month < 5:
            term = "Spring"
        elif 6 <= start_month < 8:
            term = "Summer"
        else:
            term = "Fall"

        return f"{term} {year}"


# Usage example
data_scraper = ScrapeData()
json_data = data_scraper.to_json(data_scraper.scrapeData())
print(json_data)

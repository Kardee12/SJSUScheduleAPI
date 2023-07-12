from typing import List
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import scraper

app = FastAPI()

data_scraper = scraper.ScrapeData()
json_data = data_scraper.to_json(data_scraper.scrapeData())

@app.get("/")
async def root():
    return JSONResponse(content=json_data)


@app.get("/courses/")
async def listCourses(skip: int = 0, limit: int = 10):
    return json_data[skip: skip + limit]


@app.get("/courses/multiple")
async def getMultipleDepartmentsCourses(d: List[str] = Query(...)):
    print(d)
    lowercase_departments = [dept.lower() for dept in d]
    filtered_courses = []
    for course in json_data:
        for dept in lowercase_departments:
            if dept == course.get("department", "").lower():
                filtered_courses.append(course)
                break
    return JSONResponse(content=filtered_courses)


@app.get("/courses/professor")
async def getCoursesByProfessor(professor: str):
    filtered_courses = []

    for course in json_data:
        if professor.lower() in course["instructor"].lower():
            filtered_courses.append(course)

    return JSONResponse(content = filtered_courses)


@app.get("/courses/search")
async def searchCourses(
        department: str = Query(None),
        professor: str = Query(None),
        course: str = Query(None),
        units: float = Query(None),
        mode_of_instruction: str = Query(None)
):
    filtered_courses = []

    for courseEntry in json_data:
        if department and courseEntry["department"].lower() != department.lower():
            continue
        if professor and professor.lower() not in courseEntry["instructor"].lower():
            continue
        if course and course.lower() not in courseEntry["course"].lower():
            continue
        if units and courseEntry["units"] != units:
            continue
        if mode_of_instruction and mode_of_instruction.lower() not in courseEntry["mode_of_instruction"].lower():
            continue
        filtered_courses.append(courseEntry)

    return JSONResponse(content = filtered_courses)


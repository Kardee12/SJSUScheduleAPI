from django.http import JsonResponse
from django.shortcuts import render

import scraper

data_scraper = scraper.ScrapeData()
json_data = data_scraper.to_json(data_scraper.scrapeData())
def search_courses(request):
    filtered_courses = []
    department = request.GET.get('department', None)
    professor = request.GET.get('professor', None)
    course = request.GET.get('course', None)
    units = request.GET.get('units', None)
    mode_of_instruction = request.GET.get('mode_of_instruction', None)

    for courseEntry in json_data:
        if department and courseEntry["department"].lower() != department.lower():
            continue
        if professor and professor.lower() not in courseEntry["instructor"].lower():
            continue
        if course and (not courseEntry["course"] or course.lower() not in courseEntry["course"].lower()):
            continue
        if units and float(courseEntry["units"]) != float(units):
            continue
        if mode_of_instruction and mode_of_instruction.lower() not in courseEntry["mode_of_instruction"].lower():
            continue
        filtered_courses.append(courseEntry)
    context = {'courses': filtered_courses}
    return render(request, 'search.html', context)

    return JsonResponse(filtered_courses, safe=False)


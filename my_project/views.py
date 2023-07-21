from django.http import JsonResponse
from django.shortcuts import render

import scraper
from django.shortcuts import redirect


data_scraper = scraper.ScrapeData()
json_data = data_scraper.to_json(data_scraper.scrapeData())


def home(request):
    return redirect('search_courses')

def search_courses(request):
    data_scraper = scraper.ScrapeData()
    json_data = data_scraper.to_json(data_scraper.scrapeData())

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

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(filtered_courses, safe=False)  # Return JSON for AJAX calls
    else:
        context = {'courses': filtered_courses}
        return render(request, 'search.html', context)  # Render the template for direct page visits

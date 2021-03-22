from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.views import View
from random import sample
from data import tours, title, subtitle, description, departures


class MainView(View):
    def get(self, request):
        return render(request, 'index.html', {'tours': sample(tours.items(), 6), 'title': title, 'subtitle': subtitle,
                                              'description': description, 'departures': departures.items()})


class DepartureView(View):
    def get(self, request, departure):
        tours_by_departure = {}
        for tour_id, tour in tours.items():
            if tour['departure'] == departure:
                tour['departure_name'] = departures[tour['departure']]
                tours_by_departure[tour_id] = tour
        count = len(tours_by_departure)
        price = []
        nights = []
        for tour_id, tour in tours_by_departure.items():
            price.append(tour['price'])
            nights.append(tour['nights'])
        price_min = min(price)
        price_max = max(price)
        nights_min = min(nights)
        nights_max = max(nights)
        try:
            departure = departures[departure]
        except KeyError:
            raise Http404

        return render(request, 'departure.html', {'departures': departures.items(), 'departure': departure,
                                                  'tours': tours_by_departure.items(), 'count': count,
                                                  'price_min': price_min, 'price_max': price_max,
                                                  'nights_min': nights_min, 'nights_max': nights_max})


class TourView(View):
    def get(self, request, id):
        try:
            tour = tours[id]
        except KeyError:
            raise Http404
        dep = departures[tour['departure']]
        return render(request, 'tour.html', {'departures': departures.items(), 'tour': tour, 'dep': dep})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!(404)')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')

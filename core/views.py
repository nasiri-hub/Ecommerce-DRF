import logging
import requests
from django.shortcuts import render, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class Home(APIView):
    @method_decorator(cache_page(timeout=5 * 60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Recieved the response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')
        return HttpResponse(data)

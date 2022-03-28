from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

class categorizar ( APIView):


    def get(self,request,*args, **kwargs):
        pass

    def post(self,request,*args, **kwargs):

        action = request.data.get("action", "get_data")

        
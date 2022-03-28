from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from database.conection import cliente
from dataAnalitics.kappa import *

class data(APIView):


    def get(self, request, *args, **kwargs):
        
        return Response({
            "vars": [ x["key"] for x in categorias["aggregations"]["categorias"]["buckets"]],
            "question": "¿cual de los siguiente aspectos considera importante para el bienestar institucional?"
            })


    def post(self,request, *args, **kwargs):

        categoria = request.data.get("variable", "")
        user = request.data.get("user", "n/a")
        description = request.data.get("description", "")
        puntuacion = request.data.get("numero", 0)
        puntuacion = int(puntuacion)

        categoria = categoria.lower()

        data = cliente.index(
            index = "data-tele", 
            body = { 
                "user" : user,
                "description" : description,
                "score" :  puntuacion,
                "categoria" : categoria
            } 
            
        )

        words = description.split(" ")
        for word in words:
            if word!= "":
                data = cliente.index(
                    index = "data-tele", 
                    body = { 
                        "user" : user,
                        "word" : word.lower(),
                        "score" :  puntuacion,
                        "categoria" : categoria,
                        "id" : data["_id"]
                    } 
                    
                )

        return Response({"data" : data})



class kappaCategorization(APIView):

    def get (self,request,*args,**kwargs):
        
        response = {}
        observadores = categorias["aggregations"]["types_count"]["value"]
        for categoria in categorias["aggregations"]["categorias"]["buckets"]:
            data = cliente.search(
                body = {
                    "size" : 10000,
                    "query" : {
                        "bool" : {
                            "must" : [
                                {"term" : {"categoria.keyword" :  categoria["key"]}}
                                ]
                            }
                        }
                    }
            )

            p = get_p(observadores,data["hits"]["hits"])
            suma = get_suma_mult(observadores,data["hits"]["hits"])
            kappa = get_kappa(observadores,observadores,suma,p)

            response[categoria["key"]] = kappa
            

        return Response ( response)
import pandas as pd

def get_kappa(observadores,sujetos,suma_mult, p ):
    
    q = 1-p

    if p == 0:
        return 0

    print (observadores,sujetos,suma_mult, p)
    K = 1 - ( (suma_mult) / (observadores*sujetos*(observadores - 1)* p*q) )
    return K

def get_suma_mult(observadores,categoria_list):

    suma = 0 
    for  x in categoria_list:
        suma = suma + (x["_source"]["score"] * (observadores - x["_source"]["score"]))

    return suma

def get_p(observadores,categoria_list):
    suma = 0 
    for  x in categoria_list:
        print (x["_source"]["score"])
        suma = suma + x["_source"]["score"]

    suma = suma / (observadores*observadores)

    return suma

from database.conection import cliente


categorias = cliente.search( 

    body = {
        "size" : 0,
        "query" : {
            "bool" : {
                "must" : [
                    {
                        "exists": {
                        "field": "categoria"
                        }
                    }
                ]
            }
        },
        "aggs" : {
            "types_count" : { "value_count" : { "field" : "user.keyword" } },
            "categorias" : { "terms" : {"field" : "categoria.keyword"  }}
        }
    }
 )

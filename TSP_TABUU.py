import math
import random

def distancia(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(0, len(ruta)-1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i+1]
        total = total + distancia(coord[ciudad1], coord[ciudad2])
    ciudad1 = ruta[-1]
    ciudad2 = ruta[0]
    total = total + distancia(coord[ciudad1], coord[ciudad2])
    return total 

def busqueda_tabu(ruta, coord):
    mejor_ruta = ruta 
    memoria_tabu = {}
    persistencia = 5
    mejora = False 
    iteraciones = 100
    
    while iteraciones > 0:
        iteraciones = iteraciones - 1
        dist_actual = evalua_ruta(ruta, coord)
        mejora = False
        for i in range(0, len(ruta)):
            if mejora:
                break
            for j in range(0, len(ruta)):
                if i != j:
                    ruta_tmp = ruta[:]
                    ciudad_tmp = ruta_tmp[i]
                    ruta_tmp[i] = ruta_tmp[j]
                    ruta_tmp[j] = ciudad_tmp
                    dist = evalua_ruta(ruta_tmp, coord)
                    
                    tabu = False
                    if ruta_tmp[i] + "_" + ruta_tmp[j] in memoria_tabu:
                        if memoria_tabu[ruta_tmp[i] + "_" + ruta_tmp[j]] > 0:
                            tabu = True
                        if ruta_tmp[j] + "_" + ruta_tmp[i] in memoria_tabu: 
                            if memoria_tabu[ruta_tmp[j] + "_" + ruta_tmp[i]] > 0:  
                                tabu = True 
                        
                        if dist < dist_actual and not tabu:
                            ruta = ruta_tmp[:]
                            if evalua_ruta(ruta, coord) < evalua_ruta(mejor_ruta, coord):
                                mejor_ruta = ruta[:]
                                memoria_tabu[ruta_tmp[i] + "_" + ruta_tmp[j]] = persistencia
                                mejora = True
                                break
                        elif dist < dist_actual and tabu:
                            if evalua_ruta(ruta_tmp, coord) < evalua_ruta(mejor_ruta, coord):
                                mejor_ruta = ruta_tmp[:]
                                ruta = ruta_tmp[:]
                                memoria_tabu[ruta_tmp[i] + "_" + ruta_tmp[j]] = persistencia 
                                mejora = True
                                break
                    
                    if len(memoria_tabu) > 0:
                        for k in memoria_tabu: 
                            if memoria_tabu[k] > 0:
                                memoria_tabu[k] = memoria_tabu[k] - 1
    return mejor_ruta

if __name__ == "__main__":
    coord = {
        'JiloYork': (19.984146, -99.519127),
        'Toluca': (19.286167856525594, -99.65473296644892),
        'Atlacomulco': (19.796802401380955, -99.87643301629244),
        'Guadalajara': (20.655773344775373, -103.35773871581326),
        'Monterrey': (25.675859554333684, -100.31405053526082),
        'Cancún': (21.158135651777727, -86.85092947858692),
        'Morelia': (19.720961251258654, -101.15929186858635),
        'Aguascalientes': (21.88473831747085, -102.29198705069501),
        'Queretaro': (20.57005870003398, -100.45222862892079),
        'CDMX': (19.429550164848152, -99.13000959477478)
    }

    ruta = list(coord.keys())
    random.shuffle(ruta)

    ruta = busqueda_tabu(ruta, coord)
    print(ruta)
    print("Distancia total: " + str(evalua_ruta(ruta, coord)))

import math
import random

def distancia(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    ciudad1 = ruta[-1]  # Última ciudad
    ciudad2 = ruta[0]  # Regresar a la primera ciudad
    total += distancia(coord[ciudad1], coord[ciudad2])
    return total

def busqueda_tabu(ruta, coord):
    mejora_ruta = ruta
    memoria_tabu = {}
    persistencia = 5
    mejora = False
    iteraciones = 100

    while iteraciones > 0:
        iteraciones -= 1
        dist_actual = evalua_ruta(ruta, coord)
        mejora = False
        for i in range(len(ruta)):
            if mejora:
                break
            for j in range(len(ruta)):
                if i != j:
                    ruta_tmp = ruta[:]
                    ciudad_tmp = ruta_tmp[i]
                    ruta_tmp[i] = ruta_tmp[j]
                    ruta_tmp[j] = ciudad_tmp
                    dist = evalua_ruta(ruta_tmp, coord)

                    tabu = False
                    if (ruta_tmp[i], ruta_tmp[j]) in memoria_tabu:
                        if memoria_tabu[(ruta_tmp[i], ruta_tmp[j])] > 0:
                            tabu = True
                    if (ruta_tmp[j], ruta_tmp[i]) in memoria_tabu:
                        if memoria_tabu[(ruta_tmp[j], ruta_tmp[i])] > 0:
                            tabu = True

                    if dist < dist_actual and not tabu:
                        ruta = ruta_tmp[:]
                        if evalua_ruta(ruta, coord) < evalua_ruta(mejora_ruta, coord):
                            mejora_ruta = ruta[:]
                            memoria_tabu[(ruta_tmp[i], ruta_tmp[j])] = persistencia
                            mejora = True
                            break
                    elif dist < dist_actual and tabu:
                        if evalua_ruta(ruta_tmp, coord) < evalua_ruta(mejora_ruta, coord):
                            mejora_ruta = ruta_tmp[:]
                            memoria_tabu[(ruta_tmp[i], ruta_tmp[j])] = persistencia
                            mejora = True
                            break

        if len(memoria_tabu) > 0:
            for key in list(memoria_tabu.keys()):
                if memoria_tabu[key] > 0:
                    memoria_tabu[key] -= 1
    return mejora_ruta

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

    # Crear ruta inicial aleatoria
    ruta = list(coord.keys())
    random.shuffle(ruta)

    mejora_ruta = busqueda_tabu(ruta, coord)
    print("Ruta mejorada:", mejora_ruta)
    print("Distancia de la ruta mejorada:", evalua_ruta(mejora_ruta, coord))

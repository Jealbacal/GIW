# TODO: rellenar
# Asignatura: GIW
# Práctica XXXXXX
# Grupo: XXXXXXX
# Autores: XXXXXX
#
# Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
# sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
# de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
# de manera directa o indirecta. Declaramos además que no hemos realizado de manera
# deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
# resultados de los demás.


### Formato CSV
def lee_fichero_accidentes(ruta):
    with open("AccidentesBicicletas_2021.csv",encoding="utf-8") as archivo:
        accidentes = []
        
        for linea in archivo:
            linea=linea.rstrip("\n")
            columna = linea.split(",")
            cod_distrito= columna[5]
            cod_lesividad= columna[13]
            coordeanda_x_utm= columna[15]
            coordeanda_y_utm= columna[16]
            distrito= columna[6]
            estado_meteorologico= columna[8]
            fecha= columna[1]
            hora= columna[2]
            localizacion= columna[3]
            num_expediente= columna[0]
            numero= columna[4]
            positiva_alcohol= columna[17]
            positiva_droga= columna[18]
            rango_edad= columna[11]
            sexo= columna[12]
            tipo_accidente= columna[7]
            tipo_lesividad= columna[14]
            tipo_persona= columna[10]
            tipo_vehiculo= columna[9]
            accidentes.append({
                
                "cod_distrito" : cod_distrito,
                "cod_lesividad " :  cod_lesividad,
                "coordeanda_x_utm" : coordeanda_x_utm,
                "coordeanda_y_utm" : coordeanda_y_utm,
                "distrito" : distrito,
                "estado_meteorologico" :  estado_meteorologico,
                "fecha": fecha,
                "hora" : hora,
                "localizacion" : localizacion,
                "num_expediente" : num_expediente,
                "numero" : numero,
                "positiva_alcohol" :  positiva_alcohol,
                "positiva_droga" : positiva_droga,
                "rango_edad" : rango_edad,
                "sexo" : sexo,
                "tipo_accidente" : tipo_accidente,
                "tipo_lesividad" :  tipo_lesividad,
                "tipo_persona" : tipo_persona,
                "tipo_vehiculo" : tipo_vehiculo
                
            })
            
        return accidentes
                
                
            
            
            
            
            
            
        

def accidentes_por_distrito_tipo(datos):
    ...

def dias_mas_accidentes(datos):
    ...

def puntos_negros_distrito(datos, distrito, k):
    ...


#### Formato JSON
def leer_monumentos(json_file):
    ...

def subtipos_monumentos(monumentos):
    ...

def busqueda_palabras_clave(monumentos, palabras):
    ...

def busqueda_distancia(monumentos, calle, distancia):
    ...

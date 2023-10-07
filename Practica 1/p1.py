# TODO: rellenar
# Asignatura: GIW
# Práctica 1
# Grupo: Grupo 04
# Autores: 	Jesús Alberto Barrios Caballero
#			José Javier Carrasco Ferri
#			Enrique Martín Rodríguez
#			Felipe Ye Chen
#
# Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
# sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
# de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
# de manera directa o indirecta. Declaramos además que no hemos realizado de manera
# deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
# resultados de los demás.


#Los prints para comprobar el correcto funcionamiento de las funciones están comentados

# Ejercicio 1
a=[[1, 0, 2],
[0, 3, 3],
[1, 2, 2]]

b=[[0,0],
  [0,0]]

c=[[1,1,1],
  [2,2,2],
  [3,3,3]]

def dimension(matriz):
   
    x=len(matriz)
    y=len(matriz[0])
   
    if(x==0):
        return None
    for i in range(x):
        if(y!=len(matriz[i])):
            return None
    return x,y


def es_cuadrada(matriz):
    x=dimension(matriz)
   
    if(x==None):
        return False
    if(x[0]==x[1]):
        return True
   
    return False
   
   
def es_simetrica(matriz):

    if(es_cuadrada(matriz)):
       
        n = len(matriz)
        for i in range(n):
            for j in range(i + 1, n):
                if matriz[i][j] != matriz[j][i]: #miramos si matriz igual  su traspuesta
                    return False
        return True
   
    return False


def multiplica_escalar(matriz,k):
   
    if(dimension(matriz)==None):
        return None
    rows,cols=dimension(matriz)
   
    matrix_aux = [[0 for _ in range(cols)] for _ in range(rows)]#creamos matriz auxiliar toda a 0
   
    for i in range(cols):
        for j in range(rows):
            matrix_aux[i][j]=matriz[i][j]*k #ponemos en la matriz auxiliar el resultado de multiplicar por escalar
    return matrix_aux
       
       

def suma(matriz1,matriz2):
    if(dimension(matriz1)!=dimension(matriz2)):
        return None
   
    cols,rows=dimension(matriz1)
   
    matrix_aux = [[0 for _ in range(cols)] for _ in range(rows)] #creamos matriz auxiliar toda a 0
   
    for i in range(cols):
        for j in range(rows):
            matrix_aux[i][j]=matriz1[i][j]+matriz2[i][j] #ponemos en la matriz auxiliar la suma de los elementos de ambas matrices
    return matrix_aux
   
# print("\n")   
# print("Matrices\n")
  
# print("EJ1")
# print(dimension(a))

# print("\n")
# print("EJ2")
# print(es_cuadrada(a))

# print("\n")
# print("EJ3")
# print(es_simetrica(b))

# print("\n")
# print("EJ4")
# print(multiplica_escalar(a,2))

# print("\n")
# print("EJ5")
# print(suma(a,c))
	
 
 
 
 
 
	
# Ejercicio 2
automata = {'alfabeto': {'a', 'b'},
'estados': {'r0', 'r1'},
'inicial': 'r0',
'finales': {'r0'},
'transicion': {('r0', 'a'): 'r0',
               ('r0', 'b'): 'r1',
               ('r1', 'a'): 'r1',
               ('r1', 'b'): 'r1',
}
}

automata_ok = {'alfabeto': {'0', '1'},
 'estados': {'p', 'q' , 'r'},
 'inicial': 'p',
 'finales': {'q'},
 'transicion': {('p', '0'): 'q',
 ('p', '1'): 'r',
 ('q', '0'): 'r',
 ('q', '1'): 'q',
 ('r', '0'): 'r',
 ('r', '1'): 'r'
 }
 }

automata_mal1 = {'alfabeto': {},
 'estados': {'p', 'q' , 'r'},
 'inicial': 'p',
 'finales': {'q'},
 'transicion': {('p', '0'): 'q',
 ('p', '1'): 'r',
 ('q', '0'): 'r',
 ('q', '1'): 'q',
 ('r', '0'): 'r',
 ('r', '1'): 'r'
 }
 }
def validar(automata):
   
   
    lista=['alfabeto', 'estados', 'inicial', 'finales' ,'transicion']
    format_keys = str(automata.keys()).replace("dict_keys(", "").replace(")", "")
     
   
    if(str(format_keys)!=str(lista)):#comprueba las claves
        return False
    if(len(automata['alfabeto'])==0):#es vacio el alfabeto
        return False
    if(len(automata['estados'])==0):#es vacio el estado
        return False
    if(automata['inicial'] not in automata['estados']):#inicial aparece en estados
        return False
   
    if(not all(item in automata['estados'] for item in automata['finales'])):#todos los finales aparecen en estados
        return False
    #print(aut['transicion']['r0','a'])
   
    #comprobar que todas las transiciones esten bien
    #try catch
    #en teoria todos los alfabetos y estados se deben de usar
    #por lo que no hay estados sin usar el for no deberia salir fuera de indice
    contador=0
    try:
        for i in automata['estados']:
            for j in automata['alfabeto']:
                contador+=1
                if(automata['transicion'][i,j] not in automata['estados']):
                    return False
    except IndexError:
        print("Tienes un estado o alfabeto sin usar")
        
    return True
 
   
   
# print('\n\n\n')
# print("Automatas\n")

# print("EJ1:")

# print(validar(automata_ok))

# print(validar(automata_mal1))
    




def aceptar(cadena,automata):
    if(not validar(automata)):
        return False
    
    next_state=automata['inicial']
    for i in cadena:
        if(i not in automata['alfabeto']):#si la cadena esta mal
            return False
        
        next_state=automata['transicion'][next_state,i]
        
    if(not next_state in automata['finales']):#comprueba estado final despues de la cadena
        return False
    return True

# print("\n")
# print("EJ2:")

# print(aceptar('',automata_ok))
# print(aceptar('0001',automata_ok))
# print(aceptar('0111',automata_ok))  
# print(aceptar('01a0',automata_ok))    

automata1 = {'alfabeto': {'a', 'b'},
 'estados': {'q0', 'q1' , 'q2'},
 'inicial': 'q0',
 'finales': {'q0', 'q2'},
 'transicion': {('q0', 'a'): 'q2',
 ('q0', 'b'): 'q1',
 ('q1', 'a'): 'q1',
 ('q1', 'b'): 'q1',
 ('q2', 'a'): 'q0',
 ('q2', 'b'): 'q1',
 }
 }

automata2 = {'alfabeto': {'a', 'b'},
 'estados': {'r0', 'r1'},
 'inicial': 'r0',
 'finales': {'r0'},
 'transicion': {('r0', 'a'): 'r0',
 ('r0', 'b'): 'r1',
 ('r1', 'a'): 'r1',
 ('r1', 'b'): 'r1',
 }
 }
automata3 = {'alfabeto': {'a', 'b'},
 'estados': {'s0', 's1', 's2', 's3'},
 'inicial': 's0',
 'finales': {'s2'},
 'transicion': {('s0', 'a'): 's1',
 ('s0', 'b'): 's3',
 ('s1', 'a'): 's3',
 ('s1', 'b'): 's2',
 ('s2', 'a'): 's3',
 ('s2', 'b'): 's2',
 ('s3', 'a'): 's3',
 ('s3', 'b'): 's3',
 }
 }

def equivalentes(aut1, aut2):
    
    #if(not validar(aut1)and validar(aut2)):
        #return False
    
    alfabeto=aut1['alfabeto']#igual en los 2 en teoria
    if(alfabeto!=aut2['alfabeto']):
        return False #just in case
    
    nodos=[(aut1['inicial'],aut2['inicial'])]#inicializo el primer nodo
    nodos_existentes=[(aut1['inicial'],aut2['inicial'])]
    
    while(nodos):
        
        n1,n2=nodos.pop()#borro el ultimo del nodo sino bucle no acaba nunca
        for a in alfabeto:
            next1=aut1['transicion'][n1,a]#cojo las transiciones
            next2=aut2['transicion'][n2,a]
            
            if(next1 is not None and next2 is not None):
                end1=next1 in aut1['finales']
                end2=next2 in aut2['finales']
                if(end1!=end2):#si ambos llegan a un estado final
                    return False
            par=(next1,next2)
            if(par not in nodos_existentes):#se añade un nuevo nodo
                nodos.append(par)
                nodos_existentes.append(par)
    
    #si ha podido salir del while y no ha dado False
    #los dos automatas son equivalentes 
    return True


# print("\n")
# print("EJ3:")

# print(equivalentes(automata1,automata2))
# print(equivalentes(automata2,automata1))
# print(equivalentes(automata1,automata1))
# print(equivalentes(automata1,automata3))



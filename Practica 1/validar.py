
automata_ok={'alfabeto':{0,1},
             'estados':{'p','q','r'},
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

def validarF(automata):
    estados = automata.get('estados')
    finales = automata.get('finales')
    for estado in finales:
        if estado not in estados:
            return False

    return True


def validarT(automata):
    trans = automata. get('transicion')
    estados = automata.get('estados')
    alf = automata.get('alfabeto')
    result=True
    for clave in trans:
        if (trans.get(clave) not in estados) and (clave[0] not in estados) and (clave[1] not in alf):
            result=False
        
    return result and (len(trans)== len(estados)*len(alf))
     
def validar (automata):
    return automata.get('alfabeto') is not None and automata.get('estados') is not None and automata.get('inicial') in automata.get('estados') and validarF(automata) and validarT(automata)
           

print(validar(automata_ok))
    

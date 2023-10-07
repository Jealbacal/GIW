

import xml.sax
import html

def nombres_restaurantes(filename):
    class NameHandler(xml.sax.ContentHandler):
        
        def __init__(self):
            self.curr_path = [] 
            self.name = []

        def startElement(self, name, attrs):
            self.curr_path.append(name)

        def endElement(self, name):
            self.curr_path.pop()

        def characters(self, content):
            if self.curr_path == ["serviceList", "service", "basicData", "name"]:
                self.name.append(html.unescape(content))
            
    parser=xml.sax.make_parser()        
    handler=NameHandler()
    parser.setContentHandler(handler)
    
    with open(filename,"r",encoding="utf-8") as fichero:
        parser.parse(fichero)

    # Return the extracted names
  
    return sorted(handler.name)   
            
#=======================================================
def subcategorias(filename):
    ...


def info_restaurante(filename, name):
    ...


def busqueda_cercania(filename, lugar, n):
    ...


print("funciona")

print(nombres_restaurantes("restaurantes_v1_es.xml"))
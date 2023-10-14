import pprint
import xml.sax

def subcategorias(filename):

    class Ejercicio2Handler(xml.sax.ContentHandler):

        lista = []
        categoria = ""
        subcategoria = ""
        
        def __init__(self):
            self.curr_path = [] 
            self.name = []

        def startElement(self, name, attrs):
            self.curr_path.append(name)
            
            
            if name == "item":
                if attrs["name"] != "idCategoria" or attrs["name"] != "idSubCategoria":
                    self.curr_path.append(name)
            else:
                self.curr_path.append(name)

        def endElement(self, name):
            self.curr_path.pop()

        def characters(self, content):
            if len(self.curr_path) >= 2 and self.curr_path[-2:] == ["categoria","item"]:
                self.categoria = content
            if len(self.curr_path) >= 4 and self.curr_path[-4:] == ["categoria","subcategorias","subcategoria","item"]:
                self.subcategoria = content
                self.lista.append((self.categoria,self.subcategoria))
    
    parser = xml.sax.make_parser()
    parser.setContentHandler(Ejercicio2Handler())
    
    with open(filename,"r",encoding="utf-8") as fichero:
        parser.parse(fichero)

    return Ejercicio2Handler.lista


for i in subcategorias("restaurantes_v1_es_pretty.xml"):
    print(i)


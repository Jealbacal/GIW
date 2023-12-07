from mongoengine import StringField,IntField,ListField,EmbeddedDocumentField,FloatField
from mongoengine import Document,DynamicDocument,EmbeddedDocument
from mongoengine import connect,ValidationError
from datetime import datetime



class Tarjeta(EmbeddedDocument):
    nombre=StringField(required=True,min_length=2)
    numero=StringField(required=True,min_length=16,max_length=16)
    mes=StringField(required=True,min_length=2,max_length=2)
    año=StringField(required=True,min_length=2,max_length=2)
    ccv=StringField(required=True,min_length=3,max_length=3)
    
    def clean(self):
        if not self.numero.isdigit():
             raise ValidationError(f'{self.numero} must contain only numeric digits.')
        if not self.mes.isdigit():
             raise ValidationError(f'{self.mes} must contain only numeric digits.')
        if not self.año.isdigit():
             raise ValidationError(f'{self.año} must contain only numeric digits.')
        if not self.ccv.isdigit():
             raise ValidationError(f'{self.ccv} must contain only numeric digits.')
       
class Linea(EmbeddedDocument):
    num_items=IntField(required=True)
    precio_item=FloatField(required=True)
    nombre_item=StringField(required=True,min_length=2)
    total=FloatField(required=True)
    ref=StringField(required=True) 
    
    def clean(self):
        if self.num_items <=0:
            raise ValidationError(f'{self.num_items}must be a natural number')
        if self.precio_item <=0:
            raise ValidationError(f'{self.precio_item} must a positive number')
        if self.total <=0:
            raise ValidationError(f'{self.total} must a positive number')
        
        
class Producto(Document):
    codigo_barras = StringField(required=True, min_length=13, max_length=13)
    nombre = StringField(required=True, min_length=2)
    categoria_principal = IntField(required=True)
    categoria_secundaria = ListField(IntField(), required=True)
    
    def clean(self):
        if not self.codigo_barras.isdigit():
            raise ValidationError(f'{self.codigo_barras} must contain only numeric digits.')
        if self.categoria_principal <= 0:
            raise ValidationError(f'{self.categoria_principal} must be a natural number')
        if any(num < 0 for num in self.categoria_secundaria):
            raise ValidationError("Numbers in categoria secundaria must be natural numbers")
        
    
     
    
class Pedido(EmbeddedDocument):
    total=IntField(required=True)
    fecha=StringField(required=True)
    lineas= ListField(EmbeddedDocumentField(Linea),required=True)
    
    def clean(self):
        try:
            datetime.strptime(self.fecha, "%Y,%m,%d,%H,%M,%S,%f")
        except ValueError:
            raise ValidationError(f'{self.fecha} must be in the format AAAA,MM,DD,HH,MM,SS,NNNNNN')

    

class Usuario(Document):

        dni = StringField(required=True, unique=True,regex=r'^\d{8}[A-Za-z]$')
        nombre=StringField(required=True,min_length=2)
        apellido1=StringField(required=True,min_length=2)
        apellido2=StringField(required=False)#opcional
        f_nac=StringField(required=True)
        tarjetas = ListField(EmbeddedDocumentField(Tarjeta),required=False)#opcional
        pedidos= ListField(EmbeddedDocumentField(Pedido),required=False)
        
        def clean(self):
            try:
                datetime.strptime(self.f_nac, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(f'{self.f_nac} must be in the format AAAA-MM-DD')
            
        
      

connect('giw_mongoengine') 
Usuario.objects.delete()#reseteo para no comerme el unique todo el rato

producto=Producto(codigo_barras="9780201379624", nombre="Galletas Oreo", categoria_principal=5,
        categoria_secundaria=[5, 8, 9])
producto2=Producto(codigo_barras="1234567891234", nombre="Producto 2", categoria_principal=1,
        categoria_secundaria=[1,2,3,4])

linea=Linea(num_items=3, precio_item=1.5, nombre_item="Galletas Oreo", total=4.5, ref="9780201379624")
linea2=Linea(num_items=100, precio_item=150, nombre_item="Galletas Oreo", total=15000, ref="1234567891234")

tarjeta=Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="19", ccv="852")
tarjeta2=Tarjeta(nombre="Pepe", numero="1234567891234567", mes="05", año="20", ccv="123")

pedido=Pedido(total=4.5, fecha="2016,11,25,10,15,24,000000", lineas=[linea,linea2])


usuario=Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado",
        f_nac="1985-12-11", tarjetas=[tarjeta,tarjeta2], pedidos=[pedido])

usuario.save()

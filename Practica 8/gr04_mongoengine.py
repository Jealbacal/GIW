from mongoengine import StringField,IntField,ListField,FloatField,ReferenceField,ComplexDateTimeField
from mongoengine import Document
from mongoengine import connect,disconnect,ValidationError
from datetime import datetime

connect(db='giw_mongoengine', uuidRepresentation='standard') 


class Tarjeta(Document):
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
       

        
        
class Producto(Document):
    codigo_barras = StringField(required=True,unique=True,min_length=13, max_length=13)#13 digitos
    nombre = StringField(required=True, min_length=2)
    categoria_principal = IntField(required=True)
    categorias_secundarias = ListField(IntField())#opcional
    
    def clean(self):
        if not self.codigo_barras.isdigit():
            raise ValidationError(f'{self.codigo_barras} must contain only numeric digits.')
        if self.categoria_principal <= 0:
            raise ValidationError(f'{self.categoria_principal} must be a natural number')
        if any(num < 0 for num in self.categoria_secundaria):
            raise ValidationError("Numbers in categoria secundaria must be natural numbers")
        #comprobar ean13
       
        suma=0
        num = list(map(int, self.codigo_barras[:-1]))#hasta el penultimo digito
        for i in range (12):
            suma+=num[i]*(3 if i%2!=0 else 1)#empiezo en pos 0
        control=(10-(suma%10))%10
        c=self.codigo_barras[12]
    
        if int(control)!=int(c):#castint a int para no comparar strings que da error
            raise ValidationError(f"Numero de control calculado:{control} es diferente a control en cod_barras:{c}")
        
        #---------categoria secundaria
        if  self.categorias_secundarias and self.categorias_secundarias[0] != self.categoria_principal:
            raise ValidationError(f"el primer elemento de secundaria deberia ser:{self.categoria_principal}")
     
            
class Linea(Document):
    num_items=IntField(required=True,min_value= 0)
    precio_item=FloatField(required=True,min_value= 0)
    nombre_item=StringField(required=True,min_length=2)
    total=FloatField(required=True,min_value= 0)
    ref=ReferenceField(Producto,reverse_delete_rule="CASCADE",required=True)
    
    def clean(self):
       
        # if self.num_items <=0:
        #     raise ValidationError(f'{self.num_items}must be a natural number')
        # if self.precio_item <=0:
        #     raise ValidationError(f'{self.precio_item} must a positive number')
        # if self.total <=0:
        #     raise ValidationError(f'{self.total} must a positive number') 
        
        calc=self.num_items*self.precio_item     
        if self.total!=calc:#comprobacion de total
            raise ValidationError(f'total:{self.total} no coincide con total calculado:{calc}')   
        
        name=self.ref.nombre
        if self.ref.nombre!=self.nombre_item:#comprobacion de nombre
            raise ValidationError(f'ref:{self.nombre_item} no coincide con nombre producto:{type(name)}')   
        
        
class Pedido(Document):
    total=FloatField(required=True)
    fecha=ComplexDateTimeField(required=True)
    lineas= ListField(ReferenceField(Linea),reverse_delete_rule="CASCADE",required=True)
    
    def clean(self):
        
        try:
            suma=0
            for l in self.lineas:
                suma+=l.total
            if suma!=self.total:
                 raise ValidationError(f'la suma de los pedidos no coincide con el total, suma:{suma}, total:{self.total}')
        except Exception as e:
            print(f"An error occurred: {e}")
        try:
            datetime.strptime(self.fecha, "%Y,%m,%d,%H,%M,%S,%f")
        except ValueError:
            raise ValidationError(f'{self.fecha} must be in the format AAAA,MM,DD,HH,MM,SS,NNNNNN')
        try:
            lista=set()
            for l in self.lineas:
             
                if l.ref.codigo_barras in lista:
                    raise ValidationError(f'{l.ref.codigo_barras} esta repetido')
                lista.add(l.ref.codigo_barras)
            
        except Exception as e:
            print(f"An error occurred: {e}")

    

class Usuario(Document):

        dni = StringField(required=True, unique=True,regex=r'^\d{8}[A-Za-z]$')#formato 8 num 1 letra
        nombre=StringField(required=True,min_length=2)
        apellido1=StringField(required=True,min_length=2)
        apellido2=StringField()#opcional
        f_nac=StringField(required=True)
        tarjetas = ListField(ReferenceField(Tarjeta),reverse_delete_rule="CASCADE")#opcional
        pedidos= ListField(ReferenceField(Pedido),reverse_delete_rule="CASCADE")
        
        def clean(self):
                 
            num=int(self.dni[:8])
            letras_dni = 'TRWAGMYFPDXBNJZSQVHLCKE'      
            if self.dni[8].upper() != letras_dni[num % 23]: #comprueba la letra de control
                    raise ValidationError('La letra de control del DNI no es correcta')
          
            try:
                datetime.strptime(self.f_nac, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(f'{self.f_nac} must be in the format AAAA-MM-DD')
            
        
# disconnect()      
# db = Usuario._get_db()
# collections = db.list_collection_names()
# for collection in collections:
#     db.drop_collection(collection)

# producto=Producto(codigo_barras="5901234123457", nombre="Galletas Oreo", categoria_principal=5,
#         categoria_secundaria=[5, 8, 9])
# producto2=Producto(codigo_barras="9780201379624", nombre="Producto 2", categoria_principal=1,
#         categoria_secundaria=[1,2,3,4])

# producto.save()
# producto2.save()

# linea=Linea(num_items=3, precio_item=1.5, nombre_item="Galletas Oreo", total=4.5, ref=producto)
# linea2=Linea(num_items=100, precio_item=150, nombre_item="Producto 2", total=15000, ref=producto2)

# linea.save()
# linea2.save()

# tarjeta=Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="19", ccv="852")
# tarjeta2=Tarjeta(nombre="Pepe", numero="1234567891234567", mes="05", año="20", ccv="123")

# tarjeta.save()
# tarjeta2.save()

# pedido=Pedido(total=15004.5, fecha="2016,11,25,10,15,24,000000", lineas=[linea,linea2])

# pedido.save()

# usuario=Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado",
#         f_nac="1985-12-11", tarjetas=[tarjeta,tarjeta2], pedidos=[pedido])

# usuario.save()



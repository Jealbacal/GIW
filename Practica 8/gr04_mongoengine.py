"""
Asignatura: GIW
Práctica 7
Grupo: 04
Autores:Jesús Alberto Barrios Caballero
        José Javier Carrasco Ferri
        Enrique Martín Rodríguez
        Felipe Ye Chen

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""


from mongoengine import StringField,IntField,ListField,FloatField,ReferenceField,\
    ComplexDateTimeField,EmbeddedDocumentField,PULL
from mongoengine import Document,EmbeddedDocument
from mongoengine import connect,ValidationError

connect(db='giw_mongoengine', uuidRepresentation='standard')


class Tarjeta(EmbeddedDocument):
    '''Definicion de la clase Tarjeta'''
    nombre=StringField(required=True,min_length=2)
    numero=StringField(required=True,min_length=16,max_length=16)
    mes=StringField(required=True,min_length=2,max_length=2)
    año=StringField(required=True,min_length=2,max_length=2)
    ccv=StringField(required=True,min_length=3,max_length=3)

    def clean(self):
        '''Validacion de la clase Tarjeta'''
        self.validate(clean=False)

        if not self.numero.isdigit():
            raise ValidationError(f'{self.numero} must contain only numeric digits.')
        if not self.mes.isdigit():
            raise ValidationError(f'{self.mes} must contain only numeric digits.')
        if not self.año.isdigit():
            raise ValidationError(f'{self.año} must contain only numeric digits.')
        if not self.ccv.isdigit():
            raise ValidationError(f'{self.ccv} must contain only numeric digits.')




class Producto(Document):
    '''Definicion de la clase Producto'''
    codigo_barras = StringField(required=True,unique=True,min_length=13, max_length=13)#13 digitos
    nombre = StringField(required=True, min_length=2)
    categoria_principal = IntField(required=True, min_value=0)
    categorias_secundarias = ListField(IntField(),default=[],required=False)#opcional

    def clean(self):
        '''Validacion de la clase Producto'''
        self.validate(clean=False)

        if not self.codigo_barras.isdigit():
            raise ValidationError(f'{self.codigo_barras} must contain only numeric digits.')
        # if self.categoria_principal <= 0:
        #     raise ValidationError(f'{self.categoria_principal} must be a natural number')

        if any(num < 0 for num in self.categorias_secundarias):
            raise ValidationError("Numbers in categoria secundaria must be natural numbers")


        #comprobar ean13

        suma=0
        num = list(map(int, self.codigo_barras[:-1]))#hasta el penultimo digito
        for i in range (12):
            suma+=num[i]*(3 if i%2!=0 else 1)#empiezo en pos 0
        control=(10-(suma%10))%10
        c=self.codigo_barras[12]

        if int(control)!=int(c):#castint a int para no comparar strings que da error
            raise ValidationError(f"Numero de control calculado:{control}\
                                   es diferente a control en cod_barras:{c}")

        #---------categoria secundaria
        if  self.categorias_secundarias and \
            self.categorias_secundarias[0] != self.categoria_principal:
            raise ValidationError(f"el primer elemento de secundaria deberia ser:\
                                  {self.categoria_principal}")


class Linea(EmbeddedDocument):
    '''Definicion de la clase Linea'''
    num_items=IntField(required=True,min_value= 1)
    precio_item=FloatField(required=True,min_value= 0)
    nombre_item=StringField(required=True,min_length=2)
    total=FloatField(required=True,min_value= 0)
    ref=ReferenceField(Producto,required=True)

    def clean(self):
        '''Validacion de la clase Linea'''
        self.validate(clean=False)


        if self.total != self.num_items * self.precio_item:#comprobacion de total
            raise ValidationError(f'total:{self.total} no coincide con total calculado:\
                                  {self.num_items*self.precio_item}')


        name=self.ref.nombre
        if self.ref.nombre != self.nombre_item:#comprobacion de nombre
            raise ValidationError(f'ref:{self.nombre_item} no coincide con nombre producto:{name}')

        if not self.precio_item > 0 :#comprobacion de nombre
            raise ValidationError(f'ref:{self.nombre_item} un producto no puede valor 0:{name}')

class Pedido(Document):
    '''Definicion de la clase Pedido'''
    total=FloatField(required=True)
    fecha=ComplexDateTimeField(required=True)
    lineas= ListField(EmbeddedDocumentField(Linea),required=True)

    def clean(self):
        '''Validacion de la clase Pedido'''
        self.validate(clean=False)


        suma=0
        for l in self.lineas:
            suma+=l.total
        if suma!=self.total:
            raise ValidationError(f'la suma de los pedidos no coincide con el total, \
                                  suma:{suma}, total:{self.total}')


        lista=set()
        for l in self.lineas:

            if l.ref.codigo_barras in lista:
                raise ValidationError(f'{l.ref.codigo_barras} esta repetido')
            lista.add(l.ref.codigo_barras)





class Usuario(Document):
    '''Definicion de la clase Usuario'''

    dni = StringField(required=True, unique=True,regex=r'^\d{8}[A-Za-z]$')#formato 8 num 1 letra
    nombre=StringField(required=True,min_length=2)
    apellido1=StringField(required=True,min_length=2)
    apellido2=StringField()#opcional
    f_nac=StringField(required=True, regex=r'^\d{4}-\d{2}-\d{2}$')
    tarjetas = ListField(EmbeddedDocumentField(Tarjeta),required=False)#opcional
    pedidos= ListField(ReferenceField(Pedido,reverse_delete_rule=PULL))

    def clean(self):
        '''Validacion de la clase Usuario'''
        self.validate(clean=False)

        num=int(self.dni[:8])
        letras_dni = 'TRWAGMYFPDXBNJZSQVHLCKE'
        if self.dni[8].upper() != letras_dni[num % 23]: #comprueba la letra de control
            raise ValidationError('La letra de control del DNI no es correcta')

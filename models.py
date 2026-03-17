from peewee import *

DATABASE = SqliteDatabase('data.db')



######## DA AGGIUNGERE SUPERADMIN (?) E USER (sicuro) ########
 



######## CAR ########
class Car(Model):
  brand = CharField(max_length=100)
  rent_length = IntegerField() #months
  price = IntegerField() #€/month
  color = CharField(max_length=50)
  trasmission = CharField(max_length=50)
  fuel = CharField(max_length=50)
  power = IntegerField() 
  traction = CharField(max_length=50)
  number_of_seats = IntegerField()

  class Meta:
    database = DATABASE
    table_name = 'cars'
    #orders_by = 'brand'

  def to_dict(self):
    return {
      'id': self.id,
      'brand': self.brand,
      'rent_length': self.rent_length,
      'price': self.price,
      'color': self.color,
      'trasmission': self.trasmission,
      'fuel': self.fuel,
      'power': self.power,
      'traction': self.traction,
      'number_of_seats': self.number_of_seats
    }
  
######## SUPERCAR ########
class Supercar(Model):
  brand = CharField(max_length=100)
  rent_length = IntegerField() #days
  price = IntegerField() #€/day
  color = CharField(max_length=50)
  trasmission = CharField(max_length=50)
  fuel = CharField(max_length=50)
  power = IntegerField() 
  number_of_seats = IntegerField()
  inside_color = CharField(max_length=50)
  inside_material = CharField(max_length=50)

  class Meta:
    database = DATABASE
    table_name = 'supercars'
    #orders_by = 'brand'

  def to_dict(self):
    return {
      'id': self.id,
      'brand': self.brand,
      'rent_length': self.rent_length,
      'price': self.price,
      'color': self.color,
      'trasmission': self.trasmission,
      'fuel': self.fuel,
      'power': self.power,
      'number_of_seats': self.number_of_seats,
      'inside_color': self.inside_color,
      'inside_material': self.inside_material
    }
  
######## CYCLE ########
class Cycle(Model):
  type = CharField(max_length=50) 
  brand = CharField(max_length=100)
  rent_length = IntegerField() #days
  price = IntegerField() #€/day
  frame_size = CharField(max_length=50) #cm
  traction = CharField(max_length=50)
  suspension = CharField(max_length=50)
  accecsories = CharField(max_length=100)
  ideal_terrain = CharField(max_length=50)

  class Meta:
    database = DATABASE
    table_name = 'cycles'
    #orders_by = 'type'

  def to_dict(self):
    return {
      'id': self.id,
      'type': self.type,
      'brand': self.brand,
      'rent_length': self.rent_length,
      'price': self.price,
      'frame_size': self.frame_size,
      'traction': self.traction,
      'suspension': self.suspension,
      'accecsories': self.accecsories,
      'ideal_terrain': self.ideal_terrain
    }
  
######## SCOOTER ########
class Scooter(Model):
  brand = CharField(max_length=100)
  rent_length = IntegerField() #days
  price = IntegerField() #€/day
  color = CharField(max_length=50)
  engine = CharField(max_length=50)
  fuel = CharField(max_length=50)
  power = IntegerField() 
  required_license = CharField(max_length=50)
  number_of_seats = IntegerField()
  storage_space = CharField(max_length=50)
  windshield = BooleanField(default=False)

  class Meta:
    database = DATABASE
    table_name = 'scooters'
    #orders_by = 'brand'

  def to_dict(self):
    return {
      'id': self.id,
      'brand': self.brand,
      'rent_length': self.rent_length,
      'price': self.price,
      'color': self.color,
      'engine': self.engine,
      'fuel': self.fuel,
      'power': self.power,
      'required_license': self.required_license,
      'number_of_seats': self.number_of_seats,
      'storage_space': self.storage_space,
      'windshield': self.windshield
    }
  
######## MOTORCYCLES ########
class Motorcycle(Model):
  brand = CharField(max_length=100)
  rent_length = IntegerField() #days
  price = IntegerField() #€/day
  style = CharField(max_length=50)
  color = CharField(max_length=50)
  engine = CharField(max_length=50)
  fuel = CharField(max_length=50)
  power = IntegerField() 
  required_license = CharField(max_length=50)
  number_of_seats = IntegerField()
  storage_space = CharField(max_length=50)
  trasmission = CharField(max_length=50)

  class Meta:
    database = DATABASE
    table_name = 'motorcycles'
    #orders_by = 'brand'

  def to_dict(self):
    return {
      'id': self.id,
      'brand': self.brand,
      'rent_length': self.rent_length,
      'price': self.price,
      'style': self.style,
      'color': self.color,
      'engine': self.engine,
      'fuel': self.fuel,
      'power': self.power,
      'required_license': self.required_license,
      'number_of_seats': self.number_of_seats,
      'trasmission': self.trasmission,
      'storage_space': self.storage_space
    }
  
######## CAMPER ########
class Camper(Model):
  brand = CharField(max_length=100)
  rent_length = IntegerField() #months
  price = IntegerField() #€/month
  trasmission = CharField(max_length=50)
  fuel = CharField(max_length=50)
  color = CharField(max_length=50)
  type = CharField(max_length=50)
  sleeping_beds = IntegerField()
  approved_seats = IntegerField()
  vehicle_length = CharField(max_length=50)
  type_bathroom = CharField(max_length=50)
  climate_control = BooleanField(default=False)
  pets_allowed = BooleanField(default=False)

  class Meta:
    database = DATABASE
    table_name = 'campers'
    #orders_by = 'brand'

  def to_dict(self):
    return {
      'id': self.id,
      'brand': self.brand,
      'rent_length': self.rent_length,
      'price': self.price,
      'trasmission': self.trasmission,
      'fuel': self.fuel,
      'color': self.color,
      'type': self.type,
      'sleeping_beds': self.sleeping_beds,
      'approved_seats': self.approved_seats,
      'vehicle_length': self.vehicle_length,
      'type_bathroom': self.type_bathroom,
      'climate_control': self.climate_control,
      'pets_allowed': self.pets_allowed
    }
    

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Car, Supercar, Cycle, Scooter, Motorcycle, Camper], safe = True)
	DATABASE.close()  

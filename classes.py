from abc import ABC, abstractmethod

class User:
    def __init__(self, id, first_name, last_name, email, phone, address, birthdate, gender, ssn, admin_role=False, password="1234"):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.birthdate = birthdate
        self.gender = gender
        self.ssn = ssn
        self.admin_role = admin_role
        self.password = password
    
class Admin(User):
    def __init__(self, id, first_name, last_name, email, phone, address, birthdate, gender, ssn, admin_role=True, password="1234"):
        super().__init__(id, first_name, last_name, email, phone, address, birthdate, gender, ssn, admin_role, password)



class Item(ABC):
    def __init__(self, id, name, quantity, price, user_id):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.user_id = user_id

    @abstractmethod
    def update_details(self, **kwargs):
        pass

class ElectricalPart(Item):
    def __init__(self, id, name, description, quantity, price, user_id):
        super().__init__(id, name, quantity, price, user_id)
        self.description = description
        self.type = "Electrical"

    def update_details(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self        

class MechanicalPart(Item):
    def __init__(self, id, name, description, quantity, price, user_id):
        super().__init__(id, name, quantity, price, user_id)
        self.description = description
        self.type = "Mechanical"

    def update_details(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self        

class RawMaterial(Item):
    def __init__(self, id, name, description, quantity, price, user_id):
        super().__init__(id, name, quantity, price, user_id)
        self.description = description
        self.type = "Raw Material"

    def update_details(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self        

from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self,name,username,email,password,contact):
        self.name=name
        self.username=username
        self.email=email
        self.password=password
        self.contact=contact
    
    @abstractmethod
    def login(self):
        pass


class Customer(User):
    customer_count=0
    def __init__(self):
        Customer.customer_count+=1
        super().__init__()
        self.customer_id=f"CUS{Customer.customer_count:03d}"

        

class Admin(User):
    admin_count=0
    def __init__(self):
        Admin.admin_id+=1
        super().__init__()
        self.admin_id=f"A{Admin.admin_id:03d}"


class Client:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        return {
            "Имя": self.name,
            "E-mail": self.email,
            "Номер телефона": self.phone
        }

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            "Название": self.name,
            "Цена": self.price
        }

class Order:
    def __init__(self, client, product, quantity):
        self.client = client
        self.product = product
        self.quantity = quantity

    def to_dict(self):
        return {
            "Клиент": self.client.name,
            "Товар": self.product.name,
            "Количество": self.quantity
        }
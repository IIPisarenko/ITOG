class Client:
    """
    Класс для представления клиента с его персональными данными.
    """

    def __init__(self, name, email, phone):
        """
        Инициализация объекта Клиент.

        :param name: Имя клиента
        :param email: Электронная почта клиента
        :param phone: Телефонный номер клиента
        """
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """
        Преобразует объект Client в словарь для удобства сериализации или отображения.

        :return: словарь с данными клиента
        """
        return {
            "Имя": self.name,
            "E-mail": self.email,
            "Номер телефона": self.phone
        }

class Product:
    """
    Класс для представления товара с его характеристиками.
    """

    def __init__(self, name, price):
        """
        Инициализация объекта Product.

        :param name: Название товара
        :param price: Цена товара
        """
        self.name = name
        self.price = price

    def to_dict(self):
        """
        Преобразует объект Product в словарь для сериализации или отображения.

        :return: словарь с данными товара
        """
        return {
            "Название": self.name,
            "Цена": self.price
        }

class Order:
    """
    Класс для представления заказа, связанного с клиентом и товаром, а также количеством.
    """

    def __init__(self, client, product, quantity):
        """
        Инициализация объекта Order.

        :param client: Объект Client, связанный с заказом
        :param product: Объект Product, связанный с заказом
        :param quantity: Количество товаров в заказе
        """
        self.client = client
        self.product = product
        self.quantity = quantity

    def to_dict(self):
        """
        Преобразует объект Order в словарь для сериализации или отображения.

        :return: словарь с данными заказа
        """
        return {
            "Клиент": self.client.name,
            "Товар": self.product.name,
            "Количество": self.quantity
        }
from abc import ABC, abstractmethod

class BaseProduct(ABC):
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = value

    @classmethod
    @abstractmethod
    def new_product(cls, data_dict):
        """Создание нового продукта из словаря (абстрактный метод)."""
        pass

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        if type(self) is type(other):
            return self.price * self.quantity + other.price * other.quantity
        else:
            raise TypeError(
                f"Нельзя складывать объекты разных классов: {type(self).__name__} и {type(other).__name__}"
            )


class DebugInitMixin:
    def __init__(self, *args, **kwargs):
        print(f"Создан объект класса {self.__class__.__name__} с args={args} kwargs={kwargs}")
        super().__init__(*args, **kwargs)



class Product(DebugInitMixin, BaseProduct):
    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, data_dict):
        return cls(data_dict["name"], data_dict["description"], data_dict["price"], data_dict["quantity"])

class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        base = super().__str__()
        return (f"{base}, Модель: {self.model}, Память: {self.memory}, Цвет: {self.color},"
                f" Производительность: {self.efficiency}")

class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        base = super().__str__()
        return f"{base}, Страна: {self.country}, Срок прорастания: {self.germination_period}, Цвет: {self.color}"


class Category:
    _category_count = 0
    _product_count = 0

    def __init__(self, name, description, products=None):
        """Класс для представления категорий."""
        self.name = name
        self.description = description
        self.__products = []
        Category._category_count += 1
        if products:
            for prod in products:
                self.add_product(prod)

    @property
    def category_count(self):
        return type(self)._category_count

    @property
    def products(self):
        return self.__products[:]

    @property
    def product_count(self):
        return Category._product_count

    @property
    def get_products_list(self):
        """Получение списка товаров в виде строк."""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price:.2f} руб. Остаток: {product.quantity} шт.\n"
        return result

    def add_product(self, product):
        """Добавление товара в категорию."""
        if isinstance(product, Product):
            self.__products.append(product)
            Category._product_count += 1
        else:
            raise TypeError("Необходимо передать объект класса Product или его наследников")

    def get_products(self):
        """Возвращает список товаров (безопасно копируя его)."""
        return self.__products[:]

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                         [product1, product2, product3])

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
                         [product4])

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)

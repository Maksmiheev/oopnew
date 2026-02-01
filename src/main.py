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
    def __repr__(self):
        base_repr = super().__repr__()  # вызов __repr__ родительского класса
        return f"{base_repr} (Debug: создан объект класса {self.__class__.__name__})"



class Product(DebugInitMixin, BaseProduct):
    def __init__(self, name, description, price, quantity):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
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
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        Category._product_count += 1


    def middle_price(self):
        try:
            total_price = sum(product.price for product in self.__products)
            count = len(self.__products)
            average = total_price / count
            return average
        except ZeroDivisionError:
            # Если товаров нет, возвращаем 0
            return 0

    def get_products(self):
        """Возвращает список товаров (безопасно копируя его)."""
        return self.__products[:]

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


if __name__ == '__main__':
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())

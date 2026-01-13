class Product:
    def __init__(self, name, description, price, quantity):
        """Класс для представления продуктов."""
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, value):
        """Сеттер для цены с проверкой на положительность."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

    @classmethod
    def new_product(cls, data_dict):
        """
        Создание нового продукта из словаря.
        """
        return cls(data_dict["name"], data_dict["description"], data_dict["price"], data_dict["quantity"])

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        if isinstance(other, Product):
            return self.price * self.quantity + other.price * other.quantity
        return NotImplemented

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
            raise TypeError("Необходимо передать объект класса Product")

    def get_products(self):
        """Возвращает список товаров (безопасно копируя его)."""
        return self.__products[:]

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self.__products)} шт."


if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)

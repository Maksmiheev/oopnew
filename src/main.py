class Product:
    def __init__(self, name, description, price, quantity):
        """Класс для представления продуктов."""
        self.name = name
        self.description = description
        self._price = price  # Сделали цену приватной
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для цены."""
        return self._price

    @price.setter
    def price(self, value):
        """Сеттер для цены с проверкой на положительность."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = value

    @classmethod
    def new_product(cls, data_dict):
        """
        Создание нового продукта из словаря.
        """
        return cls(data_dict["name"], data_dict["description"], data_dict["price"], data_dict["quantity"])


class Category:
    _category_count = 0  # Приватный статический счётчик категорий
    _product_count = 0  # Приватный статический счётчик товаров

    def __init__(self, name, description, products=None):
        """Класс для представления категорий."""
        self.name = name
        self.description = description
        self.__products = []
        Category._category_count += 1
        if products:
            for prod in products:
                self.add_product(prod)

    def add_product(self, product):
        """Добавление товара в категорию."""
        if isinstance(product, Product):
            self.__products.append(product)
            Category._product_count += 1
        else:
            raise TypeError("Необходимо передать объект класса Product")

    def get_products_list(self):
        """Получение списка товаров в виде строк."""
        result = []
        for p in self.__products:
            result.append(f"{p.name}, {p.price:.2f} руб. Остаток: {p.quantity} шт.")
        return "\n".join(result)

    def get_products(self):
        """Возвращает список товаров (безопасно копируя его)."""
        return self.__products[:]


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.get_products())
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.get_products())

    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)

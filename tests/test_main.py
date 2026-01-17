import unittest

from src.main import Category, LawnGrass, Product, Smartphone


class TestProduct(unittest.TestCase):
    def test_create_product(self):
        product = Product("iPhone 14 Pro Max", "Серебряный корпус, 256 ГБ памяти", 120000.0, 10)
        self.assertEqual(product.name, "iPhone 14 Pro Max")
        self.assertEqual(product.description, "Серебряный корпус, 256 ГБ памяти")
        self.assertEqual(product.price, 120000.0)
        self.assertEqual(product.quantity, 10)

    def test_price_setter_valid_value(self):
        product = Product("iPhone 14 Pro Max", "Серебряный корпус, 256 ГБ памяти", 120000.0, 10)
        product.price = 130000.0
        self.assertEqual(product.price, 130000.0)

    def test_new_product_class_method(self):
        data = {
            "name": "Samsung Galaxy Z Fold 4",
            "description": "Складной экран, 512 ГБ памяти",
            "price": 150000.0,
            "quantity": 5,
        }
        product = Product.new_product(data)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Samsung Galaxy Z Fold 4")
        self.assertEqual(product.description, "Складной экран, 512 ГБ памяти")
        self.assertEqual(product.price, 150000.0)
        self.assertEqual(product.quantity, 5)


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.category = Category("Смартфоны", "Каталог смартфонов")
        self.product1 = Product("iPhone 14 Pro Max", "Серебряный корпус, 256 ГБ памяти", 120000.0, 10)
        self.product2 = Product("Samsung Galaxy S23 Ultra", "Черный корпус, 512 ГБ памяти", 150000.0, 5)

    def test_add_product(self):
        self.category.add_product(self.product1)
        self.assertIn(self.product1, self.category.get_products())
        self.assertEqual(len(self.category.get_products()), 1)

    def test_get_products_list(self):
        self.category.add_product(self.product1)
        expected_output = ["iPhone 14 Pro Max, 120000.00 руб. Остаток: 10 шт."]
        self.assertListEqual(expected_output, self.category.get_products_list.strip().split("\n"))

    def test_category_count_and_product_count(self):
        initial_categories = Category._category_count
        initial_products = Category._product_count

        self.category.add_product(self.product1)
        self.category.add_product(self.product2)

        self.assertEqual(Category._category_count, initial_categories)
        self.assertEqual(Category._product_count, initial_products + 2)

    def test_get_products_returns_copy(self):
        self.category.add_product(self.product1)
        original_products = self.category.get_products()
        original_products.pop()  # Модификация копии списка
        self.assertNotEqual(original_products, self.category.get_products())  # Проверка, что оригинал не изменился


class TestProductMagicMethods(unittest.TestCase):

    def setUp(self):
        self.product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
        self.product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        self.product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    def test_str(self):
        expected = "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
        self.assertEqual(str(self.product1), expected)

    def test_repr(self):
        # __repr__ возвращает то же, что и __str__
        self.assertEqual(repr(self.product2), str(self.product2))

    def test_add(self):
        result = self.product1 + self.product2
        expected = (180000.0 * 5) + (210000.0 * 8)
        self.assertEqual(result, expected)

        result2 = self.product1 + self.product3
        expected2 = (180000.0 * 5) + (31000.0 * 14)
        self.assertEqual(result2, expected2)


class TestProductAndCategory(unittest.TestCase):

    def setUp(self):
        self.smartphone = Smartphone(
            name="iPhone 13",
            description="Смартфон Apple",
            price=79999.0,
            quantity=5,
            efficiency="Высокая",
            model="A2633",
            memory="128GB",
            color="Чёрный",
        )
        self.lawn_grass = LawnGrass(
            name="Газонная трава",
            description="Лучшее покрытие для газона",
            price=1200.5,
            quantity=10,
            country="Украина",
            germination_period="7 дней",
            color="Зелёный",
        )
        self.category = Category(name="Электроника", description="Гаджеты и техника")

    def test_smartphone_str(self):
        s = str(self.smartphone)
        self.assertIn("iPhone 13", s)
        self.assertIn("Модель: A2633", s)
        self.assertIn("Память: 128GB", s)
        self.assertIn("Цвет: Чёрный", s)

    def test_lawn_grass_str(self):
        s = str(self.lawn_grass)
        self.assertIn("Газонная трава", s)
        self.assertIn("Страна: Украина", s)
        self.assertIn("Срок прорастания: 7 дней", s)
        self.assertIn("Цвет: Зелёный", s)

    def test_add_product_correct(self):
        self.category.add_product(self.smartphone)
        self.category.add_product(self.lawn_grass)
        self.assertIn(self.smartphone, self.category.products)
        self.assertIn(self.lawn_grass, self.category.products)
        self.assertEqual(len(self.category.products), 2)

    def test_add_product_invalid_type(self):
        with self.assertRaises(TypeError):
            self.category.add_product("Не продукт")

    def test_product_price_setter(self):
        self.smartphone.price = 50000
        self.assertEqual(self.smartphone.price, 50000)
        # Попытка установить отрицательную цену не должна изменить цену
        self.smartphone.price = -100
        self.assertEqual(self.smartphone.price, 50000)  # Цена осталась прежней

    def test_product_add_same_class(self):
        sp2 = Smartphone("Samsung Galaxy", "Смартфон Samsung", 55999.99, 3, "Средняя", "S21", "256GB", "Белый")
        total_value = self.smartphone + sp2
        expected = self.smartphone.price * self.smartphone.quantity + sp2.price * sp2.quantity
        self.assertEqual(total_value, expected)

    def test_product_add_different_class_raises(self):
        with self.assertRaises(TypeError):
            _ = self.smartphone + self.lawn_grass


if __name__ == "__main__":
    unittest.main()

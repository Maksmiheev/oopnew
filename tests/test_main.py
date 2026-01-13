import unittest

from src.main import Category, Product


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

    def test_add_with_wrong_type(self):
        # При сложении с объектом другого типа должен вернуться NotImplemented
        self.assertEqual(self.product1.__add__(10), NotImplemented)

if __name__ == '__main__':
    unittest.main()

if __name__ == "__main__":
    unittest.main()

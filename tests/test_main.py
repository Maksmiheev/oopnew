import unittest

from src.main import Category, Product


class TestProductCategory(unittest.TestCase):

    def setUp(self):
        # Сбрасываем счетчики перед каждым тестом для изоляции
        Category.category_count = 0
        Category.product_count = 0

        # Создаем продукты для тестов
        self.product1 = Product(
            "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
        )
        self.product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        self.product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
        self.product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)

    def test_product_attributes(self):
        self.assertEqual(self.product1.name, "Samsung Galaxy S23 Ultra")
        self.assertEqual(self.product1.description, "256GB, Серый цвет, 200MP камера")
        self.assertEqual(self.product1.price, 180000.0)
        self.assertEqual(self.product1.quantity, 5)

    def test_category_creation_and_counts(self):
        category = Category(
            "Смартфоны",
            "Описание категории",
            [self.product1, self.product2, self.product3],
        )
        self.assertEqual(category.name, "Смартфоны")
        self.assertEqual(category.description, "Описание категории")
        self.assertEqual(len(category.products), 3)

        # Проверяем счетчики класса
        self.assertEqual(Category.category_count, 1)
        self.assertEqual(Category.product_count, 3)

    def test_multiple_categories_update_counts(self):
        Category("Смартфоны", "Описание", [self.product1, self.product2])
        Category("Телевизоры", "Описание", [self.product4])
        self.assertEqual(Category.category_count, 2)
        self.assertEqual(Category.product_count, 3)  # 2 + 1

    def test_empty_products_list(self):
        category_empty = Category("Пустая", "Без товаров", [])
        self.assertEqual(len(category_empty.products), 0)
        self.assertEqual(Category.product_count, 0)
        self.assertEqual(Category.category_count, 1)

    def test_counters_increment_properly(self):
        initial_category_count = Category.category_count
        initial_product_count = Category.product_count

        Category("Новая", "Описание", [self.product3])

        self.assertEqual(Category.category_count, initial_category_count + 1)
        self.assertEqual(Category.product_count, initial_product_count + 1)


if __name__ == "__main__":
    unittest.main()

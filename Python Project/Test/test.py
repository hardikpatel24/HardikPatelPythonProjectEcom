import unittest

import mysql
from entity.cart import Cart
from entity.order import Order
from entity.product import Product
import mysql.connector

from myexceptions.exceptions import CustomerNotFoundException, ProductNotFoundException


class TestEcommerceSystem(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.product = Product(1, "Laptop", 1000.0, "Description", 10)
        self.order = Order(1)
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hardik12002",
            database="Ecom"
        )
        self.cursor = self.connection.cursor()

    def test_product_creation(self):
        # product = Product(1, "Laptop", 1000.0, "Description", 10)
        self.assertEqual(self.product.get_product_id(), 1)
        self.assertEqual(self.product.get_name(), "Laptop")
        self.assertEqual(self.product.get_price(), 1000.0)
        self.assertEqual(self.product.get_description(), "Description")
        self.assertEqual(self.product.get_stock_quantity(), 10)

    def test_add_to_cart(self):
        self.cart.add_product(self.product)
        self.assertIn(self.product, self.cart.get_products())

    def test_order_creation(self):
        order_id = self.order.get_order_id()
        self.assertIsNotNone(order_id)

    def test_customer_not_found_exception(self):
        with self.assertRaises(CustomerNotFoundException):
            self.fetchCustomerById(-1)

    def test_product_not_found_exception(self):
        with self.assertRaises(ProductNotFoundException):
            self.fetchProductById(-1)

    def fetchCustomerById(self, customer_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM customers WHERE customer_id = %s', (customer_id,))
            customer = cursor.fetchone()
            if customer:
                return customer
            else:
                raise CustomerNotFoundException(f"Customer not found with ID: {customer_id}")
        finally:
            self.cursor.close()

    def fetchProductById(self, product_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
            product = cursor.fetchone()
            if product:
                return product
            else:
                raise ProductNotFoundException(f"Product not found with ID: {product_id}")
        finally:
            self.cursor.close()


if __name__ == "__main__":
    unittest.main()


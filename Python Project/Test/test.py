import unittest
import mysql.connector
from myexceptions.exceptions import CustomerNotFoundException, ProductNotFoundException
from entity.order import Order
from entity.product import Product
from entity.cart import Cart


class TestEcommerceSystem(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.product = Product("Phone", "Description", 500.0)
        self.order = Order()
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hardik12002",
            database="Ecom"
        )
        self.cursor = self.connection.cursor()

    def test_product_creation(self):
        product = Product("Laptop", "Description", 1000.0)
        self.assertEqual(product.get_name(), "Laptop")
        self.assertEqual(product.get_description(), "Description")
        self.assertEqual(product.get_price(), 1000.0)

    def test_add_to_cart(self):
        cart = Cart()
        cart_id = cart.get_cart_id()
        self.assertIn(self.product, cart_id)

    def test_order_creation(self):
        order_id = self.order.get_order_id()
        self.assertIsNotNone(order_id)

    def test_customer_not_found_exception(self):
        with self.assertRaises(CustomerNotFoundException):
            self.fetchCustomerById(self, -1, self.connection)

    def test_product_not_found_exception(self):
        with self.assertRaises(ProductNotFoundException):
            self.fetchProductById(self, -1, self.connection)

    def fetchCustomerById(self, customer_id, conn):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM customers WHERE id = %s', (customer_id,))
            customer = cursor.fetchone()
            if customer:
                return customer
            else:
                raise CustomerNotFoundException("Customer not found with ID: {}".format(customer_id))
        finally:
            self.cursor.close()

    # Placeholder function
    def fetchProductById(self, product_id, conn):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
            product = cursor.fetchone()
            if product:
                return product
            else:
                raise ProductNotFoundException("Product not found with ID: {}".format(product_id))
        finally:
            self.cursor.close()


if __name__ == "__main__":
    unittest.main()

import mysql.connector
from dao.order_processor_repository import OrderProcessorRepository
from entity.product import Product
from entity.customer import Customer
from typing import List, Dict


class OrderProcessorRepositoryImpl(OrderProcessorRepository):
    def __init__(self, host, user, password, database):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'hardik12002'
        self.database = 'Ecom'

    def _connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def _execute_query(self, query, params=None):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
        except Exception as e:
            print("Error:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def create_product(self, product: Product) -> bool:
        query = "INSERT INTO products (name, price, description, stockQuantity) VALUES (%s, %s, %s, %s)"
        params = (product.get_name(), product.get_price(), product.get_description(), product.get_stock_quantity())
        self._execute_query(query, params)
        return True

    def create_customer(self, customer: Customer) -> bool:
        query = "INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)"
        params = (customer.get_name(), customer.get_email(), customer.get_password())
        self._execute_query(query, params)
        return True

    def delete_product(self, product_id: int) -> bool:
        query = "DELETE FROM products WHERE product_id = %s"
        self._execute_query(query, (product_id,))
        return True

    def delete_customer(self, customer_id: int) -> bool:
        query = "DELETE FROM customers WHERE customer_id = %s"
        self._execute_query(query, (customer_id,))
        return True

    def add_to_cart(self, customer: Customer, product: Product, quantity: int) -> bool:
        query = "INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)"
        params = (customer.get_customer_id(), product.get_product_id(), quantity)
        self._execute_query(query, params)
        return True

    def remove_from_cart(self, customer: Customer, product: Product) -> bool:
        query = "DELETE FROM cart WHERE customer_id = %s AND product_id = %s"
        params = (customer.get_customer_id(), product.get_product_id())
        self._execute_query(query, params)
        return True

    def get_all_from_cart(self, customer: Customer) -> List[Product]:
        query = "SELECT p.* FROM products p INNER JOIN cart c ON p.product_id = c.product_id WHERE c.customer_id = %s"
        params = (customer.get_customer_id(),)
        conn = self._connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        products = [Product(**row) for row in result]
        cursor.close()
        conn.close()
        return products

    def place_order(self, customer: Customer, products_quantity: List[Dict[Product, int]],
                    shipping_address: str) -> bool:
        conn = self._connect()
        cursor = conn.cursor()
        try:
            # Insert order
            query = "INSERT INTO orders (customer_id, total_price, shipping_address) VALUES (%s, %s, %s)"
            total_price = sum(product.get_price() * quantity for product, quantity in products_quantity)
            params = (customer.get_customer_id(), total_price, shipping_address)
            cursor.execute(query, params)
            order_id = cursor.lastrowid

            # Insert order items
            for product, quantity in products_quantity:
                query = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"
                params = (order_id, product.get_product_id(), quantity)
                cursor.execute(query, params)

            conn.commit()
            return True
        except Exception as e:
            print("Error:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_orders_by_customer(self, customer_id: int) -> List[Dict[Product, int]]:
        query = """
            SELECT p.*, oi.quantity
            FROM products p
            INNER JOIN order_items oi ON p.product_id = oi.product_id
            INNER JOIN orders o ON oi.order_id = o.order_id
            WHERE o.customer_id = %s
        """
        params = (customer_id,)
        conn = self._connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        orders = [{Product(**row): row['quantity']} for row in result]
        cursor.close()
        conn.close()
        return orders

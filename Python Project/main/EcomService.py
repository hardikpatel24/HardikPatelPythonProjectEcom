import mysql.connector
from myexceptions.exceptions import CustomerNotFoundException, ProductNotFoundException, OrderNotFoundException


class EcomService:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hardik12002",
            database="Ecom"
        )
        self.cursor = self.connection.cursor()

    def register_customer(self, name, email, password):
        try:
            if self.check_customer_exists(email):
                print("Customer with the same email already exists!")
                return
            sql = "INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)"
            values = (name, email, password)
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("Customer registered successfully!")
        except mysql.connector.Error as err:
            print(f"Error registering customer: {err}")

    def update_customer(self, customer_id, name, email, password):
        try:
            if not self.check_customer_exists_by_id(customer_id):
                raise CustomerNotFoundException("Customer not found with ID: {}".format(customer_id))
            sql = "UPDATE customers SET name = %s, email = %s, password = %s WHERE customer_id = %s"
            values = (name, email, password, customer_id)
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("Customer updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error updating customer: {err}")

    def delete_customer(self, customer_id):
        try:
            if not self.check_customer_exists_by_id(customer_id):
                raise CustomerNotFoundException("Customer not found with ID: {}".format(customer_id))
            sql = "DELETE FROM customers WHERE customer_id = %s"
            self.cursor.execute(sql, (customer_id,))
            self.connection.commit()
            print("Customer deleted successfully!")
        except mysql.connector.Error as err:
            print(f"Error deleting customer: {err}")

    def fetch_customers(self):
        try:
            sql = "SELECT * FROM customers"
            self.cursor.execute(sql)
            customers = self.cursor.fetchall()
            print("All Customers:")
            for customer in customers:
                print(customer)
        except mysql.connector.Error as err:
            print(f"Error fetching customers: {err}")

    def create_product(self, name, price, description, stock_quantity):
        try:
            sql = "INSERT INTO products (name, price, description, stockQuantity) VALUES (%s, %s, %s, %s)"
            values = (name, price, description, stock_quantity)
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("Product created successfully!")
        except mysql.connector.Error as err:
            print(f"Error creating product: {err}")

    def fetch_products(self):
        try:
            sql = "SELECT * FROM products"
            self.cursor.execute(sql)
            products = self.cursor.fetchall()
            print("All Products:")
            for product in products:
                print(product)
        except mysql.connector.Error as err:
            print(f"Error fetching products: {err}")

    def delete_product(self, product_id):
        try:
            if not self.check_product_exists_by_id(product_id):
                raise ProductNotFoundException("Product not found with ID: {}".format(product_id))
            sql = "DELETE FROM products WHERE product_id = %s"
            self.cursor.execute(sql, (product_id,))
            self.connection.commit()
            print("Product deleted successfully!")
        except mysql.connector.Error as err:
            print(f"Error deleting product: {err}")

    def update_stock_quantity(self, product_id, new_quantity):
        try:
            if not self.check_product_exists_by_id(product_id):
                raise ProductNotFoundException("Product not found with ID: {}".format(product_id))
            sql = "UPDATE products SET stockQuantity = %s WHERE product_id = %s"
            values = (new_quantity, product_id)
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("Stock quantity updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error updating stock quantity: {err}")

    def check_stock_availability(self, product_id, quantity):
        try:
            sql = "SELECT stockQuantity FROM products WHERE product_id = %s"
            self.cursor.execute(sql, (product_id,))
            stock_quantity = self.cursor.fetchone()[0]
            return stock_quantity >= quantity
        except mysql.connector.Error as err:
            print(f"Error checking stock availability: {err}")
            return False

    def add_to_cart(self, customer_id, product_id, quantity):
        try:
            if not self.check_product_exists_by_id(product_id):
                raise ProductNotFoundException("Product not found with ID: {}".format(product_id))
            if not self.check_stock_availability(product_id, quantity):
                print("Insufficient stock available!")
                return
            sql = "INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)"
            values = (customer_id, product_id, quantity)
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("Product added to cart successfully!")
        except mysql.connector.Error as err:
            print(f"Error adding product to cart: {err}")

    def remove_from_cart(self, customer_id, product_id):
        try:
            sql = "DELETE FROM cart WHERE customer_id = %s AND product_id = %s"
            self.cursor.execute(sql, (customer_id, product_id))
            self.connection.commit()
            print("Product removed from cart successfully!")
        except mysql.connector.Error as err:
            print(f"Error removing product from cart: {err}")

    def fetch_cart(self, customer_id):
        try:
            sql = "SELECT * FROM cart WHERE customer_id = %s"
            self.cursor.execute(sql, (customer_id,))
            cart_items = self.cursor.fetchall()
            if cart_items:
                print("Cart contents:")
                for item in cart_items:
                    print(f"Product ID: {item[2]}, Quantity: {item[3]}")
            else:
                print("Cart is empty!")
        except mysql.connector.Error as err:
            print(f"Error fetching cart: {err}")

    def cancel_order(self, order_id):
        try:
            sql = "DELETE FROM orders WHERE order_id = %s"
            self.cursor.execute(sql, (order_id,))
            self.connection.commit()
            print("Order cancelled successfully!")
        except mysql.connector.Error as err:
            print(f"Error cancelling order: {err}")

    def fetch_order(self, order_id):
        try:
            sql = "SELECT * FROM orders WHERE order_id = %s"
            self.cursor.execute(sql, (order_id,))
            order = self.cursor.fetchone()
            if order:
                print(f"Order ID: {order[0]}, Total Price: {order[3]}, Shipping Address: {order[4]}")
            else:
                print("Order not found!")
        except mysql.connector.Error as err:
            print(f"Error fetching order: {err}")

    def check_customer_exists_by_id(self, customer_id):
        try:
            sql = "SELECT * FROM customers WHERE customer_id = %s"
            self.cursor.execute(sql, (customer_id,))
            customer = self.cursor.fetchone()
            return customer is not None
        except mysql.connector.Error as err:
            print(f"Error checking customer existence: {err}")
            return False

    def check_customer_exists(self, email):
        try:
            sql = "SELECT * FROM customers WHERE email = %s"
            self.cursor.execute(sql, (email,))
            customer = self.cursor.fetchone()
            return customer is not None
        except mysql.connector.Error as err:
            print(f"Error checking customer existence: {err}")
            return False

    def check_product_exists_by_id(self, product_id):
        try:
            sql = "SELECT * FROM products WHERE product_id = %s"
            self.cursor.execute(sql, (product_id,))
            product = self.cursor.fetchone()
            return product is not None
        except mysql.connector.Error as err:
            print(f"Error checking product existence: {err}")
            return False

    def view_cart(self, customer_id):
        try:
            sql = """
            SELECT c.customer_id, c.name AS customer_name, c.email, p.product_id, p.name AS product_name, 
                   ct.quantity, p.price
            FROM cart ct
            INNER JOIN customers c ON ct.customer_id = c.customer_id
            INNER JOIN products p ON ct.product_id = p.product_id
            WHERE ct.customer_id = %s
            """
            self.cursor.execute(sql, (customer_id,))
            cart_items = self.cursor.fetchall()
            if cart_items:
                print("Cart contents:")
                for item in cart_items:
                    print(f"Customer ID: {item[0]}, Name: {item[1]}, Email: {item[2]}, "
                          f"Product ID: {item[3]}, Product Name: {item[4]}, Quantity: {item[5]}, Price: {item[6]}")
            else:
                print("Cart is empty!")
        except mysql.connector.Error as err:
            print(f"Error viewing cart: {err}")

    def view_customer_order(self, customer_id):
        try:
            sql = """
                SELECT o.order_id, o.total_price, o.shipping_address, c.customer_id, p.name AS product_name, oi.quantity, p.price AS product_price
                FROM orders o
                INNER JOIN customers c ON o.customer_id = c.customer_id
                INNER JOIN order_items oi ON o.order_id = oi.order_id
                INNER JOIN products p ON oi.product_id = p.product_id
                WHERE o.customer_id = %s
            """
            self.cursor.execute(sql, (customer_id,))
            orders = self.cursor.fetchall()
            if orders:
                print("Customer orders:")
                for order in orders:
                    order_id, total_price, shipping_address, customer_id, product_name, quantity, product_price = order
                    print(
                        f"Order ID: {order_id}, Total Price: {total_price}, Shipping Address: {shipping_address}, "
                        f"Customer ID: {customer_id}, Product Name: {product_name}, Quantity: {quantity}, "
                        f"Product Price: {product_price}")
            else:
                print("No orders found for this customer.")
        except mysql.connector.Error as err:
            print(f"Error viewing customer orders: {err}")

    def place_order(self, customer_id, total_price, shipping_address, products):
        try:
            # Check if customer exists
            customer_exists = self.check_customer_exists_by_id(customer_id)
            if not customer_exists:
                raise CustomerNotFoundException(f"Customer not found with ID: {customer_id}")

            # Insert order into orders table
            sql_order = "INSERT INTO orders (customer_id, total_price, shipping_address) VALUES (%s, %s, %s)"
            order_values = (customer_id, total_price, shipping_address)
            self.cursor.execute(sql_order, order_values)
            self.connection.commit()

            # Retrieve order_id
            order_id = self.cursor.lastrowid

            # Insert order items into order_items table
            for product_id, quantity in products.items():
                sql_order_item = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"
                order_item_values = (order_id, product_id, quantity)
                self.cursor.execute(sql_order_item, order_item_values)
                self.connection.commit()

            print("Order placed successfully!")
        except mysql.connector.Error as err:
            print(f"Error placing order: {err}")

    def get_order_and_customer_id(self, order_id):
        try:
            sql = "SELECT o.order_id, o.total_price, o.shipping_address, c.customer_id FROM orders o JOIN customers c " \
                  "ON o.customer_id = c.customer_id WHERE o.order_id = %s "
            self.cursor.execute(sql, (order_id,))
            order_data = self.cursor.fetchone()
            if order_data:
                order_id, total_price, shipping_address, customer_id = order_data
                return order_id, total_price, shipping_address, customer_id
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error retrieving order: {err}")

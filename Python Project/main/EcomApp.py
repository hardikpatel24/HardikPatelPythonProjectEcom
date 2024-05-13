from EcomService import EcomService
from myexceptions.exceptions import CustomerNotFoundException, ProductNotFoundException, OrderNotFoundException, \
    OutOfStockException
import mysql.connector


class EcomApp:
    def __init__(self):
        self.ecom_service = EcomService()

    def main(self):
        while True:
            print("\nE-commerce Application Menu:")
            print("1. Register Customer")
            print("2. Update Customer")
            print("3. Delete Customer")
            print("4. Fetch All Customers")
            print("5. Create Product")
            print("6. Delete Product")
            print("7. Fetch Products")
            print("8. Add to Cart")
            print("9. Remove from Cart")
            print("10. View Cart")
            print("11. Place Order")
            print("12. View Customer Order")
            print("13. Cancel Order")
            print("14. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                try:
                    name = input("Enter customer name: ")
                    email = input("Enter customer email: ")
                    password = input("Enter customer password: ")
                    self.ecom_service.register_customer(name, email, password)
                    self.ecom_service.fetch_customers()
                except CustomerNotFoundException as e:
                    print("Error registering customer:", e)

            elif choice == '2':
                try:
                    customer_id = int(input("Enter customer ID to update: "))
                    name = input("Enter new name: ")
                    email = input("Enter new email: ")
                    password = input("Enter new password: ")
                    self.ecom_service.update_customer(customer_id, name, email, password)
                    self.ecom_service.fetch_customers()
                except CustomerNotFoundException as e:
                    print("Error updating customer:", e)

            elif choice == '3':
                try:
                    customer_id = int(input("Enter customer ID to delete: "))
                    self.ecom_service.delete_customer(customer_id)
                    self.ecom_service.fetch_customers()
                except CustomerNotFoundException as e:
                    print("Error deleting customer:", e)

            elif choice == '4':
                try:
                    self.ecom_service.fetch_customers()
                except CustomerNotFoundException as e:
                    print("Error fetching customers:", e)

            elif choice == '5':
                try:
                    name = input("Enter product name: ")
                    price = float(input("Enter product price: "))
                    description = input("Enter product description: ")
                    stock_quantity = int(input("Enter product stock quantity: "))
                    self.ecom_service.create_product(name, price, description, stock_quantity)
                    self.ecom_service.fetch_products()
                except ProductNotFoundException as e:
                    print("Error creating product:", e)

            elif choice == '6':
                try:
                    product_id = int(input("Enter product ID to delete: "))
                    self.ecom_service.delete_product(product_id)
                    self.ecom_service.fetch_products()
                except ProductNotFoundException as e:
                    print("Error deleting product:", e)

            elif choice == '7':
                try:
                    self.ecom_service.fetch_products()
                except ProductNotFoundException as e:
                    print("Error fetching products:", e)

            elif choice == '8':
                try:
                    customer_id = int(input("Enter customer ID: "))
                    product_id = int(input("Enter product ID to add to cart: "))
                    quantity = int(input("Enter quantity: "))
                    self.ecom_service.add_to_cart(customer_id, product_id, quantity)
                    self.ecom_service.view_cart(customer_id)
                except (ProductNotFoundException, OutOfStockException) as e:
                    print("Error adding product to cart:", e)
                except CustomerNotFoundException as e:
                    print("Error adding product to cart: Customer not found")

            elif choice == '9':
                try:
                    customer_id = int(input("Enter customer ID: "))
                    product_id = int(input("Enter product ID to remove from cart: "))
                    self.ecom_service.remove_from_cart(customer_id, product_id)
                    self.ecom_service.view_cart(customer_id)
                except CustomerNotFoundException as e:
                    print("Error removing product from cart:", e)

            elif choice == '10':
                try:
                    customer_id = int(input("Enter customer ID to view cart: "))
                    self.ecom_service.view_cart(customer_id)
                except CustomerNotFoundException as e:
                    print("Error viewing cart:", e)

            elif choice == '11':
                try:
                    customer_id = int(input("Enter customer ID: "))
                    total_price = float(input("Enter total price: "))
                    shipping_address = input("Enter shipping address: ")
                    products = {}
                    while True:
                        product_id = int(input("Enter product ID (0 to finish): "))
                        if product_id == 0:
                            break
                        quantity = int(input("Enter quantity: "))
                        products[product_id] = quantity
                    self.ecom_service.place_order(customer_id, total_price, shipping_address, products)
                    self.ecom_service.view_customer_order(customer_id)
                except (CustomerNotFoundException, OutOfStockException) as e:
                    print("Error placing order:", e)

            elif choice == '12':
                try:
                    customer_id = int(input("Enter customer ID to view orders: "))
                    self.ecom_service.view_customer_order(customer_id)
                except CustomerNotFoundException as e:
                    print("Error viewing orders:", e)

            elif choice == '13':
                try:
                    order_id = int(input("Enter order ID to cancel: "))
                    order_data = self.ecom_service.get_order_and_customer_id(order_id)
                    if order_data:
                        order_id, total_price, shipping_address, customer_id = order_data
                        self.ecom_service.cancel_order(order_id)
                    else:
                        print("Order not found!")
                except OrderNotFoundException as e:
                    print("Error cancelling order:", e)

            elif choice == '14':
                print("Exiting application.")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    ecom_app = EcomApp()
    ecom_app.main()

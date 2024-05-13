class CustomerNotFoundException(Exception):
    def __init__(self, message="Customer not found"):
        self.message = message
        super().__init__(self.message)


class ProductNotFoundException(Exception):
    def __init__(self, message="Product not found"):
        self.message = message
        super().__init__(self.message)


class OrderNotFoundException(Exception):
    def __init__(self, message="Order not found"):
        self.message = message
        super().__init__(self.message)


class OutOfStockException(Exception):
    def __init__(self, message="Product out of stock"):
        self.message = message
        super().__init__(self.message)



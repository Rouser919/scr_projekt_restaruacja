from datetime import datetime
from typing import Dict


class Person:
    def __init__(self):
        self.table_number = None
        self.order = []
        self.arrive_time_on_queue = datetime.now()

    def get_time_spent_in_queue(self) -> str:
        wait_timestamp = (
            datetime.now().timestamp() - self.arrive_time_on_queue.timestamp()
        )
        return datetime.utcfromtimestamp(wait_timestamp).strftime("%Hh:%Mmin:%Ss")

    def set_table_numer(self, table_number: int):
        self.table_number = table_number

    def append_product(self, product: Dict[str, int]):
        self.order.append(product)

    def calculate_order_value(self) -> int:
        order_value = 0
        for product_price in self.order.values():
            order_value += product_price
        return order_value

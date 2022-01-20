#!/usr/bin/env python3

import argparse
import asyncio
from random import randint
from queue import Queue

import aioconsole

from person import Person
from restaruant_menu import *

MAX_COUNT_OF_PEOPLE_IN_QUEUE = 20
MAX_COUNT_OF_ORDERS_IN_RESTARUANT = 50
SECONDS_IN_MINUTE = 3
REFRESH_TIME = 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--load_count_per_min",
        type=int,
        required=True,
        help="Max count of people that will join the queue to order per min",
    )
    return parser.parse_args()


async def generate_load(queue: Queue, load_count_per_min: int):
    while True:
        count_of_people_join_the_queue = randint(0, load_count_per_min)
        while count_of_people_join_the_queue > 0:
            queue.put(Person())
            count_of_people_join_the_queue -= 1
        await asyncio.sleep(SECONDS_IN_MINUTE)
        
async def print_menu():
    print("Product list")
    print("_____________________________")
    for product,price in RESTAURANT_MENU.items():
        print(f"Product name: {product}, price: {price}")


async def serve_person(person: Person) -> Person:
    print("Hello, what do you want to order?")
    while True:
        print("Enter Exit to end order, Menu for show the menu, Set Number to set table number or enter full name of product for add product to order")
        selection = await aioconsole.ainput("Enter a choice:")
        if selection == "Exit":
            print("Exiting an order....")
            break
        if selection == "Menu":
            print_menu()
            continue
        if selection == "Set Number":
            selection = await aioconsole.ainput("Enter a table number:")
            person.set_table_numer(int(selection))
            print("Successfully sets table number!")
            continue
        if selection in RESTAURANT_MENU.keys():
            person.append_product(product=selection,price=RESTAURANT_MENU[selection])
            print(f"Successfully add {selection} to order!")
            continue
    print(f"Time spent on queue: {person.get_time_spent_in_queue()}")
    print(f"Price of order: {person.calculate_order_value()} ")
    print("Thanks for order! Your order will be delievired soon to your table!")
    print("---------------------------------------------------------------------")
    return person


async def serve_persons(queue: Queue):
    people_orders = Queue(maxsize=MAX_COUNT_OF_PEOPLE_IN_QUEUE)
    while True:
        if not queue.empty():
            print(f"Now in queue {queue.qsize()} persons are waiting to make a order")
            print("---------------------------------------------------------------------")
            person = await serve_person(queue.get())
            people_orders.put(person)
        else:
            print(f"Wait {REFRESH_TIME} seconds for next clients")
            await asyncio.sleep(REFRESH_TIME)


async def main():
    args = parse_args()
    load_count_per_min = args.load_count_per_min
    queue = Queue(maxsize=MAX_COUNT_OF_PEOPLE_IN_QUEUE)
    await asyncio.gather(generate_load(queue, load_count_per_min), serve_persons(queue))


if __name__ == "__main__":
    asyncio.run(main())

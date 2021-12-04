#!/usr/bin/env python3

import argparse
import asyncio
from random import randint
from typing import List

import aioconsole

from person import Person
from restaruant_menu import *

MAX_COUNT_OF_PEOPLE_IN_QUEUE = 20
SECONDS_IN_MINUTE = 3
REFRESH_TIME = 10


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--load_count_per_min",
        type=int,
        required=True,
        help="Max count of people that will join the queue to order per min",
    )
    return parser.parse_args()


async def generate_load(queue: List[Person], load_count_per_min: int):
    while True:
        count_of_people_join_the_queue = randint(0, load_count_per_min)
        while count_of_people_join_the_queue > 0:
            if len(queue) == MAX_COUNT_OF_PEOPLE_IN_QUEUE:
                print(
                    f"Too much people want to join queue, please arrive later. Max count of people in queue is {MAX_COUNT_OF_PEOPLE_IN_QUEUE}"
                )
                break

            queue.append(Person())
            count_of_people_join_the_queue -= 1
        await asyncio.sleep(SECONDS_IN_MINUTE)


async def serve_person(person: Person):
    while True:
        # Dodac funkcje wypisujaca menu wraz z cena
        # Dodać dodawanie potraw wybranych przez uzytkownika do listy productow
        # dodac wybieranie numeru stolika (Zawsze) Nie interesuje nas czy stolik jest zajety przez kogos innego ale mozna to rozwazyc
        # Po wyjsciu  print z petli suma ( cena do zaplaty za wszystkie produkty, juz taka fukcja jest w klasie)
        # Wyprintowac laczny czas oczekiwania
        print("Press X to end order")
        selection = await aioconsole.ainput("Enter a choice:")
        if selection == "X":
            break
    return person


async def serve_persons(queue: List[Person]):
    people_orders = []
    while True:
        if queue:
            person = await serve_person(queue.pop(0))
            people_orders.append(person)
        else:
            print(f"Wait {REFRESH_TIME} second for next clients")
            await asyncio.sleep(REFRESH_TIME)


async def main():
    args = parse_args()
    load_count_per_min = args.load_count_per_min
    queue = []
    await asyncio.gather(generate_load(queue, load_count_per_min), serve_persons(queue))


if __name__ == "__main__":
    asyncio.run(main())

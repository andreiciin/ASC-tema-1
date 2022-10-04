"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2022
"""

import random
from threading import Semaphore
import threading


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor
        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        # lista prin care ne asiguram unicitatea id-urilor
        self.producer_ids = []
        self.cart_ids = []
        # sincronizare
        self.sem_print = Semaphore(value = 1)
        self.sem_cart = Semaphore(value = 1)
        self.cart_succes = 0
        # dictionar id producer - nr. obiecte
        self.prod_id_count = {}
        # dictionar id producer - array obiecte
        self.prod_id_list = {}
        # dictionar produs - id producer
        self.product_id = {}
        # dictionar id cart - array obiecte
        self.cart_id_list = {}
        # auxiliary variables
        self.producer_new_id = 0
        self.cart_new_id = 0
        self.producer_add_id = 0
        self.prod_new_id = 0
        self.crt_new_id = 0

    def generate_producer_random_id(self):
        # create random id
        self.prod_new_id = random.randrange(1, 20000)
        # check if it's not taken (unique)
        while self.prod_new_id in self.producer_ids:
            self.prod_new_id = random.randrange(1, 20000)
        # add to producer id list the new id
        self.producer_ids.append(self.prod_new_id)
        return self.prod_new_id

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # create random id < 20000
        self.producer_new_id = self.generate_producer_random_id()
        # initialize map with key producer id - value 0
        self.prod_id_count[self.producer_new_id] = 0
        self.prod_id_list[self.producer_new_id] = []
        return self.producer_new_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace
        :type producer_id: String
        :param producer_id: producer id
        :type product: Product
        :param product: the Product that will be published in the Marketplace
        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        def add1(sum_variable):
            sum_variable = sum_variable + 1
            return sum_variable
        # add new product to producer_id list and update counter
        self.product_id[product] = producer_id
        self.prod_id_count[producer_id] = add1(self.prod_id_count[producer_id])

        # append new product to producer_id list
        self.prod_id_list[producer_id].append(product)

        return True

    def generate_cart_random_id(self):
        self.crt_new_id = random.randrange(1, 1000000)
        while self.crt_new_id in self.cart_ids:
            self.crt_new_id = random.randrange(1, 1000000)
        self.cart_ids.append(self.crt_new_id)
        return self.crt_new_id

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        # create new random id < 1000000
        self.cart_new_id = self.generate_producer_random_id()
        # initialize map with key cart id - empty list
        self.cart_id_list[self.cart_new_id] = []
        return self.cart_new_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to add to cart
        :returns True or False. If the caller receives False, it should wait and then try again
        """
        def sub1(sum_variable):
            sum_variable = sum_variable - 1
            return sum_variable
        # check if product is available, remove from free_products list
        # and add product into cart list
        self.cart_succes = 0
        self.sem_cart.acquire()
        self.producer_add_id = 0
        # find product in prod_id_list dictionary
        for k in self.prod_id_list:
            for val in self.prod_id_list[k]:
                if val == product:
                    self.producer_add_id = k
                    self.cart_succes = 1
                    break

        if self.cart_succes == 1:
            # update producer_id list and counter
            self.prod_id_count[self.product_id[product]] = sub1(self.prod_id_count[self.product_id[product]])
            if self.producer_add_id in self.prod_id_list:
                self.prod_id_list[self.producer_add_id].remove(product)
        self.sem_cart.release()

        if self.cart_succes == 1:
            self.cart_id_list[cart_id].append(product)

        if self.cart_succes == 1:
            return True
        else:
            return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to remove from cart
        """
        def add1(sum_variable):
            sum_variable = sum_variable + 1
            return sum_variable
        # remove one product from cart list
        self.cart_id_list[cart_id].remove(product)

        # restore product to producer_id list
        for k in list(self.prod_id_list.keys()):
            self.prod_id_list[k].append(product)
            break

        # update producer_id list count
        self.prod_id_count[self.product_id[product]] = add1(self.prod_id_count[self.product_id[product]])

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.
        :type cart_id: Int
        :param cart_id: id cart
        """
        # get list from cart
        self.sem_print.acquire()
        list_p = self.cart_id_list[cart_id]
        # print list
        for prod in list_p:
            string_thread = str(threading.current_thread().name)
            string_product = str(prod)
            print(string_thread + " bought " + string_product)
        self.sem_print.release()

        return list_p

"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2022
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.contor = 0
        self.add_succes = 0
        Thread.__init__(self, **kwargs)

    def run(self):
        # iterate cart list
        for list in self.carts:
            # create id for each cart
            id_new_c = self.marketplace.new_cart()
            # iterate list of add/remove parameters
            for param in list:
                # add/remove product in desired quantity
                # check if add operation is successful
                # when add fails apply wait time
                if param["type"] == "add":
                    self.contor = 0

                    while self.contor < param['quantity']:
                        self.add_succes = 0
                        self.add_succes = self.marketplace.add_to_cart(id_new_c, param["product"])

                        if self.add_succes != 0:
                            self.contor += 1
                        else:
                            sleep(self.retry_wait_time)

                elif param["type"] == "remove":
                    for i in range(param['quantity']):
                        self.marketplace.remove_from_cart(id_new_c, param["product"])

            # place order from marketplace and print
            self.marketplace.place_order(id_new_c)

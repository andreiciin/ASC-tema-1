"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2022
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.product_id = 0
        self.product_quantity = 0
        self.product_time = 0
        self.publish_succes = 0
        Thread.__init__(self, **kwargs)

    def run(self):
        register_id = self.marketplace.register_producer()
        while True:
            # iterate product list
            for product_list in self.products:
                # extract data from product input
                self.product_id = product_list[0]
                self.product_quantity = product_list[1]
                self.product_time = product_list[2]
                # wait for the production itself
                sleep(self.product_time)
                # publish untill limit or wait
                for i in range(self.product_quantity):
                    self.publish_succes = 0
                    self.publish_succes = self.marketplace.publish(register_id, self.product_id)
                    while self.publish_succes == 0:
                        self.publish_succes = 0
                        self.publish_succes = self.marketplace.publish(register_id, self.product_id)
                        sleep(self.republish_wait_time)

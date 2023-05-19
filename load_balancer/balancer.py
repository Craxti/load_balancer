import itertools
import time

import requests
from load_balancer.vps_list import VPSList
from load_balancer.health_checker import HealthChecker
from load_balancer.logger import Logger
from load_balancer.metrics import Metrics
from load_balancer.configuration import Configuration


class LoadBalancer:
    def __init__(self, balancing_algorithm='round_robin'):
        self.vps_list = []
        self.cycle_vps = None
        self.health_checker = HealthChecker()
        self.logger = Logger()
        self.metrics = Metrics()
        self.configuration = Configuration()
        self.balancing_algorithm = balancing_algorithm

    def load_vps_list(self, filename):
        vps_list = VPSList()
        self.vps_list = vps_list.load_from_file(filename)
        self.health_checker.set_vps_list(self.vps_list)

        self.cycle_vps = itertools.cycle(self.vps_list)

        self.metrics.setup()
        self.configuration.load()

    def add_vps(self, vps):
        self.vps_list.append(vps)
        self.health_checker.add_vps(vps)

    def remove_vps(self, vps):
        if vps in self.vps_list:
            self.vps_list.remove(vps)
            self.health_checker.remove_vps(vps)

    def distribute_load(self):
        next_vps = self.get_next_vps()

        try:
            response = self.send_request(next_vps)
            self.logger.log_request_success(next_vps)
            self.metrics.update_metrics(response)
        except requests.exceptions.RequestException as e:
            self.logger.log_request_error(next_vps, str(e))

    def get_next_vps(self):
        if self.balancing_algorithm == 'round_robin':
            return self.health_checker.get_next_available_vps()
        elif self.balancing_algorithm == 'weighted_round_robin':
            return self.health_checker.get_next_weighted_vps()
        elif self.balancing_algorithm == 'least_connections':
            return self.health_checker.get_least_connections_vps()
        elif self.balancing_algorithm == 'least_response_time':
            return self.health_checker.get_least_response_time_vps()
        elif self.balancing_algorithm == 'ip_hashing':
            return self.health_checker.get_ip_hashing_vps()
        elif self.balancing_algorithm == 'random_weighted_probabilities':
            return self.health_checker.get_random_weighted_vps()
        else:
            raise ValueError("Unsupported load balancing algorithm")

    def send_request(self, vps):
        response = requests.get(vps)

        # Add error handling and retry on failed requests
        return response

import itertools
import asyncio
import requests
import aiohttp
from load_balancer.vps_list import VPSList
from load_balancer.health_checker import HealthChecker
from load_balancer.logger import Logger
from load_balancer.metrics import Metrics
from load_balancer.configuration import Configuration


class LoadBalancer:
    def __init__(self, balancing_algorithm='round_robin'):
        self.vps_manager = VPSManager()
        self.health_checker = HealthChecker()
        self.request_handler = RequestHandler()
        self.vps_list = []
        self.cycle_vps = None
        self.metrics = Metrics()
        self.configuration = Configuration()
        self.balancing_algorithm = balancing_algorithm

    def load_vps_list(self, filename):
        vps_list = self.vps_manager.load_from_file(filename)
        self.health_checker.set_vps_list(vps_list)
        self.metrics.setup()
        self.configuration.load()

    def add_vps(self, vps):
        self.vps_manager.add_vps(vps)
        self.health_checker.add_vps(vps)

    def remove_vps(self, vps):
        self.vps_manager.remove_vps(vps)
        self.health_checker.remove_vps(vps)

    async def distribute_load(self):
        next_vps = self.get_next_vps()
        try:
            response = await self.request_handler.send_request(next_vps)
            Logger.log_request_success(next_vps)
            self.metrics.update_metrics(response)
        except requests.exceptions.RequestException as e:
            Logger.log_request_error(next_vps, str(e))

    async def distribute_load_concurrently(self, num_requests):
        tasks = [self.distribute_load() for _ in range(num_requests)]
        await asyncio.gather(*tasks)

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
            client_ip = self.request_handler.get_client_ip()
            return self.health_checker.get_ip_hashing_vps(client_ip)
        elif self.balancing_algorithm == 'random_weighted_probabilities':
            return self.health_checker.get_random_weighted_vps()
        else:
            raise ValueError("Unsupported load balancing algorithm")

    def update_vps_list(self, vps_list):
        self.vps_manager.update_vps_list(vps_list)
        self.health_checker.set_vps_list(vps_list)

    def update_configuration(self, configuration):
        self.configuration = configuration
        self.configuration.load()

    def run(self, num_requests):
        asyncio.run(self.distribute_load_concurrently(num_requests))

class VPSManager:
    def __init__(self):
        self.vps_list = []
        self.cycle_vps = None

    def load_from_file(self, filename):
        vps_list = VPSList()
        self.vps_list = vps_list.load_from_file(filename)
        self.cycle_vps = itertools.cycle(self.vps_list)
        return self.vps_list

    def add_vps(self, vps):
        self.vps_list.append(vps)

    def remove_vps(self, vps):
        if vps in self.vps_list:
            self.vps_list.remove(vps)

    def update_vps_list(self, vps_list):
        self.vps_list = vps_list
        self.cycle_vps = itertools.cycle(vps_list)


class RequestHandler:
    def get_client_ip(self):
        # Get the client's IP address from the request
        # Implement the logic to extract the client IP based on your application's architecture
        # For example, if you are using a web framework like Flask, you can retrieve the client's IP using request.remote_addr
        pass

    async def send_request(self, vps):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(vps, timeout=5) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        raise requests.exceptions.RequestException(
                            f"Request to {vps} failed with status code {response.status}")
        except aiohttp.ClientError as e:
            raise requests.exceptions.RequestException(str(e))

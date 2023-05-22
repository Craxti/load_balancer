import random
import requests
from datetime import datetime
import subprocess
import logging
from functools import lru_cache


class HealthChecker:
    def __init__(self):
        self.vps_list = []
        self.active_connections = {}
        self.cache = {}

    def set_vps_list(self, vps_list):
        self.vps_list = vps_list

    def add_vps(self, vps):
        if vps not in self.vps_list:
            self.vps_list.append(vps)

    def remove_vps(self, vps):
        if vps in self.vps_list:
            self.vps_list.remove(vps)
            if vps in self.active_connections:
                del self.active_connections[vps]
            self.cache.clear()  # Clear the cache when a VPS is removed

    def get_next_available_vps(self):
        available_vps = [vps for vps in self.vps_list if self.check_health(vps)]

        if not available_vps:
            raise Exception("No VPS available for load balancing")

        return random.choice(available_vps)

    def get_least_connections_vps(self):
        min_connections_vps = None
        min_connections = float('inf')

        for vps in self.vps_list:
            connections = self.active_connections.get(vps, 0)
            if connections < min_connections and self.check_health(vps):
                min_connections = connections
                min_connections_vps = vps

        if min_connections_vps is None:
            raise Exception("No VPS available for load balancing")

        return min_connections_vps

    def get_least_response_time_vps(self):
        min_response_time_vps = None
        min_response_time = float('inf')

        for vps in self.vps_list:
            response_time = self.get_response_time(vps)
            if response_time < min_response_time and self.check_health(vps):
                min_response_time = response_time
                min_response_time_vps = vps

        if min_response_time_vps is None:
            raise Exception("No VPS available for load balancing")

        return min_response_time_vps

    def get_next_weighted_vps(self):
        weighted_vps = []

        for vps in self.vps_list:
            weight = self.get_weight(vps)
            if weight > 0 and self.check_health(vps):
                weighted_vps.extend([vps] * weight)

        if not weighted_vps:
            raise Exception("No VPS available for load balancing")

        return random.choice(weighted_vps)

    def get_ip_hashing_vps(self, client_ip):
        # IP Hashing
        ip_hash = hash(client_ip) % len(self.vps_list)
        return self.vps_list[ip_hash]

    def get_random_weighted_vps(self):
        weighted_vps = []

        for vps in self.vps_list:
            weight = self.get_weight(vps)
            if weight > 0 and self.check_health(vps):
                weighted_vps.extend([vps] * weight)

        if not weighted_vps:
            raise Exception("No VPS available for load balancing")

        return random.choice(weighted_vps)

    @lru_cache(maxsize=None)  # Caching the check_health results
    def check_health(self, vps):
        # Checking the status of the VPS, such as checking the availability of ports
        # Return True if VPS is up, False otherwise
        try:
            # Example: ICMP ping to check VPS health
            ping_cmd = ['ping', '-c', '1', '-W', '1', vps]
            result = subprocess.run(ping_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # VPS is up, check if it was previously marked as down
                if vps in self.cache and not self.cache[vps]:
                    # VPS was previously marked as down, enable it for load balancing again
                    self.cache[vps] = True
                    logging.info(f"VPS is available again: {vps}")
                return True
            else:
                self.remove_vps(vps)  # Remove an unhealthy VPS from the list
                self.handle_failure(vps)  # Handling a VPS Issue
                return False
        except subprocess.CalledProcessError:
            self.remove_vps(vps)  # Remove an unhealthy VPS from the list
            self.handle_failure(vps)  # Handling a VPS Issue
            return False

    def get_response_time(self, vps):
        # Get response time from VPS
        # Return response time in milliseconds
        try:
            start_time = datetime.now()
            response = requests.head(vps)
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000
            return response_time
        except requests.exceptions.RequestException:
            return float('inf')

    def get_weight(self, vps):
        # Example: Assigning weights based on VPS attributes or performance metrics
        if vps.cpu_usage < 80 and vps.memory_usage < 80:
            # If CPU usage and memory usage are below 80%, assign weight 2
            return 2
        elif vps.cpu_usage < 90 or vps.memory_usage < 90:
            # If either CPU usage or memory usage is below 90%, assign weight 1
            return 1
        else:
            # If both CPU usage and memory usage are above 90%, assign weight 0
            return 0

    def increase_connection_count(self, vps):
        if vps in self.active_connections:
            self.active_connections[vps] += 1
        else:
            self.active_connections[vps] = 1

    def decrease_connection_count(self, vps):
        if vps in self.active_connections:
            if self.active_connections[vps] > 0:
                self.active_connections[vps] -= 1

    def get_active_connections(self, vps):
        return self.active_connections.get(vps, 0)

    def handle_failure(self, vps):
        # Handling an issue with the VPS, such as a reboot or scaling
        # This example just prints an error message
        logging.error(f"Problem with VPS: {vps}. Error handling in progress...")

        command = f"handle_vps_failure.sh {vps}"
        try:
            subprocess.run(command, shell=True, check=True)
            logging.info(f"VPS error handling done: {vps}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error processing VPS error: {vps}, return code: {e.returncode}")

        # If the VPS is marked as down, update the cache
        if vps not in self.cache or not self.cache[vps]:
            self.cache[vps] = False

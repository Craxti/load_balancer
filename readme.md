**Load Balancer**

Load Balancer is a simple Python package that provides load balancing functionality for distributing incoming network traffic across multiple virtual private servers (VPS).


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

**Features**

Round-robin load balancing algorithm
Health checking of VPS
Automatic distribution of incoming network traffic


**Installation**

Use git clone
    `git clone https://github.com/Craxti/load_balancer.git`

**Usage**

    `from load_balancer.balancer import LoadBalancer

    # Create a LoadBalancer instance
    load_balancer = LoadBalancer()
    
    # Load the list of VPS from a file
    load_balancer.load_vps_list('vps_list.txt')
    
    # Distribute incoming network traffic
    load_balancer.distribute_load()

**VPS List File Format**

The VPS list file should contain one VPS URL per line. For example:
    
     http://vps1.example.com

     http://vps2.example.com

     http://vps3.example.com

**Customization**

Load Balancer provides options for customizing its behavior.


**Balancing Algorithm**

By default, Load Balancer uses the round-robin algorithm for load balancing. You can specify a different balancing algorithm during the initialization of the LoadBalancer instance.

    load_balancer = LoadBalancer(balancing_algorithm='random')
Supported balancing algorithms: 'round_robin', 'random'

**Health Checking**

Load Balancer performs health checks on the VPS to determine their availability for load balancing. By default, it uses a simple TCP connection check. You can customize the health checking behavior by providing your own implementation of the HealthChecker class.

    from load_balancer.health_checker import HealthChecker

    class CustomHealthChecker(HealthChecker):
        def check_health(self, vps_url):
            # Custom health checking logic
            return True
    
    health_checker = CustomHealthChecker()
    load_balancer = LoadBalancer(health_checker=health_checker)

**Contributing**

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


**License**

Copyright © Aleksandr
web - https://craxti.github.io/flask_site/

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the `GNU General Public License`_ for more details.


.. _GNU General Public License: https://www.gnu.org/licenses/gpl-3.0.html

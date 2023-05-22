import random
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, start_http_server
import logging

logger = logging.getLogger(__name__)


class RequestMetrics:
    def __init__(self, registry):
        self.request_counter = Counter('load_balancer_requests_total', 'Total Requests', registry=registry)

    def increment(self):
        self.request_counter.inc()


class ResponseTimeMetrics:
    def __init__(self, registry):
        self.response_time_histogram = Histogram('load_balancer_response_time_seconds', 'Response time per second',
                                                 registry=registry)

    def observe(self, response_time):
        self.response_time_histogram.observe(response_time)


class ConnectionMetrics:
    def __init__(self, registry):
        self.connections_counter = Counter('load_balancer_active_connections_total',
                                           'Total number of active connections', registry=registry)

    def increment(self):
        self.connections_counter.inc()


class ThroughputMetrics:
    def __init__(self, registry):
        self.throughput_gauge = Gauge('load_balancer_throughput_bytes', 'Data transfer bandwidth in bytes',
                                      registry=registry)

    def set(self, data_throughput):
        self.throughput_gauge.set(data_throughput)


class ResourceUsageMetrics:
    def __init__(self, registry):
        self.resource_usage_gauge = Gauge('load_balancer_resource_usage_percent',
                                          'Percentage of System Resource Usage', registry=registry)

    def set(self, resource_usage):
        self.resource_usage_gauge.set(resource_usage)


class AnomalyMetrics:
    def __init__(self, registry):
        self.anomaly_counter = Counter('load_balancer_anomalies_total', 'Total number of detected anomalies',
                                       registry=registry)

    def increment(self):
        self.anomaly_counter.inc()


class Metrics:
    def __init__(self):
        self.registry = CollectorRegistry()
        self.request_metrics = RequestMetrics(self.registry)
        self.response_time_metrics = ResponseTimeMetrics(self.registry)
        self.connection_metrics = ConnectionMetrics(self.registry)
        self.throughput_metrics = ThroughputMetrics(self.registry)
        self.resource_usage_metrics = ResourceUsageMetrics(self.registry)
        self.anomaly_metrics = AnomalyMetrics(self.registry)

    def setup(self):
        # Initializing the metric collection system (for example, connecting to Prometheus or Graphite)
        start_http_server(8000)

    def update_metrics(self, response):
        self._update_request_metrics()
        self._update_response_time_metrics()
        self._update_connection_metrics()
        self._update_throughput_metrics()
        self._update_resource_usage_metrics()
        self.analyze_metrics()

    def _update_request_metrics(self):
        self.request_metrics.increment()

    def _update_response_time_metrics(self):
        response_time = random.uniform(0.1, 0.5)
        self.response_time_metrics.observe(response_time)

    def _update_connection_metrics(self):
        self.connection_metrics.increment()

    def _update_throughput_metrics(self):
        data_throughput = random.uniform(100, 1000)
        self.throughput_metrics.set(data_throughput)

    def _update_resource_usage_metrics(self):
        resource_usage = random.uniform(0, 100)
        self.resource_usage_metrics.set(resource_usage)

    def analyze_metrics(self):
        average_response_time = self.response_time_metrics.observe(0)
        active_connections = self.connection_metrics.connections_counter._value.get()
        data_throughput = self.throughput_metrics.throughput_gauge._value.get()
        resource_usage = self.resource_usage_metrics.resource_usage_gauge._value.get()

        self._analyze_response_time(average_response_time)
        self._analyze_active_connections(active_connections)
        self._analyze_data_throughput(data_throughput)
        self._analyze_resource_usage(resource_usage)

    def _analyze_response_time(self, average_response_time):
        if average_response_time is not None and average_response_time > 1.0:
            self.send_notification("Average response time exceeded!")

    def _analyze_active_connections(self, active_connections):
        if active_connections > 1000:
            self.send_notification("Exceeded allowed number of active connections!")
            self.anomaly_metrics.increment()

    def _analyze_data_throughput(self, data_throughput):
        if data_throughput is not None and (data_throughput < 100 or data_throughput > 10000):
            self.send_notification("Data transfer bandwidth in the invalid range!")
            self.anomaly_metrics.increment()

    def _analyze_resource_usage(self, resource_usage):
        if resource_usage is not None and resource_usage > 80:
            self.send_notification("System resource usage exceeds allowable value!")
            self.anomaly_metrics.increment()

    def send_notification(self, message):
        logger.info(f"Notification: {message}")


metrics = Metrics()
metrics.setup()
metrics.update_metrics(None)

from prometheus_client import CollectorRegistry, Gauge
from . import GitlabCollector


class Projects(GitlabCollector):
    def __init__(self, registry=CollectorRegistry):
        super().__init__(registry=registry)
        self.g = Gauge("gitlab_sample_gauge", "This is sample gauge",
                       registry=registry)

    def collect(self):
        self.g.set(100)

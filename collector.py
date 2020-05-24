from pathlib import Path
from prometheus_client import CollectorRegistry, write_to_textfile, Gauge
import gitlab_collectors


class MetricsCollector(object):
    def __init__(self, output_dir: Path):
        self.gl_path = output_dir.joinpath("gitlab.prom")
        self.gl_registry = CollectorRegistry()
        self.gl_collectors = gitlab_collectors.all(self.gl_registry)

    def collect_all(self):
        for collector in self.gl_collectors:
            collector.collect_wrapper()
        write_to_textfile(self.gl_path, self.gl_registry)


if __name__ == "__main__":
    output_dir = Path("./output")
    collector = MetricsCollector(output_dir)
    collector.collect_all()

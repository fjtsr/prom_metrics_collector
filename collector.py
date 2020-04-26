from pathlib import Path
from prometheus_client import CollectorRegistry, write_to_textfile, Gauge


class MetricsCollector(object):
    def __init__(self, output_dir: Path):
        self.gl_path = output_dir.joinpath("gitlab.prom")
        self.gl_registry = CollectorRegistry()
        self.g = Gauge("sample_gauge", "This is sample gauge",
                       registry=self.gl_registry)

    def collect(self):
        self.g.set(100)
        write_to_textfile(self.gl_path, self.gl_registry)


if __name__ == "__main__":
    output_dir = Path("./output")
    collector = MetricsCollector(output_dir)
    collector.collect()

from pathlib import Path
import sys
from collector import MetricsCollector
import time

if __name__ == "__main__":
    output_dir = Path(sys.argv[1])
    collector = MetricsCollector(output_dir)

    while True:
        collector.collect_all()
        time.sleep(300)

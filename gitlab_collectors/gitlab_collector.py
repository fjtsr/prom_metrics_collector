import traceback
from prometheus_client import CollectorRegistry
from abc import ABCMeta, abstractclassmethod
import gitlab


class GitlabCollector(metaclass=ABCMeta):
    gl = gitlab.Gitlab.from_config('global', ['gitlab.cfg'])

    def __init__(self, registry=CollectorRegistry):
        pass

    @abstractclassmethod
    def collect(self):
        pass

    def collect_wrapper(self):
        try:
            self.collect()
        except:
            traceback.print_exc()

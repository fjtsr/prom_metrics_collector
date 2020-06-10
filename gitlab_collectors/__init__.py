from typing import List
from prometheus_client import CollectorRegistry
from gitlab_collectors.gitlab_collector import *

from gitlab_collectors.projects import *
from gitlab_collectors.backlog import *
from gitlab_collectors.bug_tracker import *
from gitlab_collectors.mr_review import *


def all(registry=CollectorRegistry) -> List[GitlabCollector]:
    return [
        Projects(registry),
        Backlog(registry),
        BugTracker(registry),
        MRReview(registry)
    ]

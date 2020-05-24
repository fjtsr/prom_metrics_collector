from typing import List
import re
from prometheus_client import CollectorRegistry, Gauge
from . import GitlabCollector
from gitlab.v4.objects import Project, ProjectLabel, ProjectIssue
from pandas import DataFrame


class Backlog(GitlabCollector):
    def __init__(self, registry=CollectorRegistry):
        super().__init__(registry=registry)
        self.g1 = Gauge("gitlab_storypoints_by_state", "This is story points of user story.", [
            'state', 'release'], registry=registry)
        self.g2 = Gauge("gitlab_storypoints_by_progress", "This is story points of user story.", [
            'progress', 'release'], registry=registry)

    def collect(self):
        project: Project = self.gl.projects.get(1)
        issues: List[ProjectIssue] = project.issues.list()

        points_list = [{
            'state': i.state,
            'progress': '進行中' in i.labels,
            'release': self.__get_release_from_labels(i.labels),
            'points': self.__get_points_from_labels(i.labels)
        } for i in issues]
        df = DataFrame(points_list)

        for name, group in df.groupby(['state', 'release']):
            self.g1.labels(state=name[0], release=name[1]).set(
                group['points'].sum())
        for name, group in df.groupby(['progress', 'release']):
            self.g2.labels(progress=name[0], release=name[1]).set(
                group['points'].sum())

    def __get_points_from_labels(self, labels: List[str]) -> int:
        points_label = [l for l in labels if "Points: " in l]
        if len(points_label) == 1:
            label = points_label[0]
            points = re.match('Points: (\d+)', label).group(1)
            return int(points)
        else:
            return 0

    def __get_release_from_labels(self, labels: List[str]) -> str:
        release_label = [l for l in labels if "リリース: " in l]
        if len(release_label) == 1:
            label = release_label[0]
            release = re.match('リリース: (.*)', label).group(1)
            return release
        else:
            return '未定'

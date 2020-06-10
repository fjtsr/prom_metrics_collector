import re
import yaml
from . import GitlabCollector
from prometheus_client import CollectorRegistry, Gauge
from gitlab.v4.objects import Project
from pandas import DataFrame, json_normalize

PROJECT_ID_LIST = [
    3
]

DESC_PATTERN = re.compile(r'```yaml\n*((.|\s)*)\n*```')


class MRReview(GitlabCollector):
    def __init__(self, registry=CollectorRegistry):
        super().__init__(registry=registry)
        self.g_time = Gauge('gitlab_review_time', 'Review time', [
                            'project', 'state', 'milestone'], registry=registry)
        self.g_class = Gauge('gitlab_review_classification', 'Review classification', [
                             'project', 'state', 'milestone', 'classification'], registry=registry)
        self.g_cause = Gauge('gitlab_review_cause', 'Review cause', [
                             'project', 'state', 'milestone', 'cause'], registry=registry)

    def collect(self):
        for pid in PROJECT_ID_LIST:
            project: Project = self.gl.projects.get(pid)
            mrs = project.mergerequests.list(all=True)

            df = json_normalize(
                [self.__get_mr_info(project, mr) for mr in mrs])
            group_df = df.groupby(['project', 'state', 'milestone']).sum()

            for key, col in group_df.iteritems():
                key_split = key.split('.')
                if key_split[0] == 'time_spent':
                    for i, v in col.iteritems():
                        self.g_time.labels(i[0], i[1], i[2]).set(v)
                elif key_split[0] == '分類':
                    classification = key_split[1]
                    for i, v in col.iteritems():
                        self.g_class.labels(
                            i[0], i[1], i[2], classification).set(v)
                elif key_split[0] == '原因':
                    cause = key_split[1]
                    for i, v in col.iteritems():
                        self.g_cause.labels(i[0], i[1], i[2], cause).set(v)

    def __get_mr_info(self, project, mr):
        info = {
            'project': project.name_with_namespace,
            'state': mr.state,
            'milestone': mr.milestone['title'] if mr.milestone else '不明',
            'time_spent': mr.time_stats()['total_time_spent']
        }
        match = DESC_PATTERN.search(mr.description)
        if match:
            review = yaml.safe_load(match.group(1))
            if type(review) == dict:
                info.update(review)
        return info

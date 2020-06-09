from prometheus_client import CollectorRegistry, Gauge
from . import GitlabCollector
import pandas as pd


class BugTracker(GitlabCollector):
    def __init__(self, registry=CollectorRegistry):
        super().__init__(registry=registry)
        self.g0 = Gauge("gitlab_bug", "This is sample gauge", [
                        'state', 'milestone', 'vl', 'sp'], registry=registry)
        self.g1 = Gauge("gitlab_bug_label1", "This is sample gauge", [
                        'state', 'milestone', 'vl', 'sp', 'label1'], registry=registry)
        self.g2 = Gauge("gitlab_bug_label2", "This is sample gauge", [
                        'state', 'milestone', 'vl', 'sp', 'label2'], registry=registry)
        self.g3 = Gauge("gitlab_bug_label3", "This is sample gauge", [
                        'state', 'milestone', 'vl', 'sp', 'label3'], registry=registry)

    def collect(self):
        df = self.get_issues_df()

        group0 = df.groupby(
            ['state', 'milestone', 'vl', 'sp']).size()
        group1 = df.groupby(
            ['state', 'milestone', 'vl', 'sp', 'label1']).size()
        group2 = df.groupby(
            ['state', 'milestone', 'vl', 'sp', 'label2']).size()
        group3 = df.groupby(
            ['state', 'milestone', 'vl', 'sp', 'label3']).size()

        for i, v in group0.iteritems():
            self.g0.labels(i[0], i[1], i[2], i[3]).set(v)
        for i, v in group1.iteritems():
            self.g1.labels(i[0], i[1], i[2], i[3], i[4]).set(v)
        for i, v in group2.iteritems():
            self.g2.labels(i[0], i[1], i[2], i[3], i[4]).set(v)
        for i, v in group3.iteritems():
            self.g3.labels(i[0], i[1], i[2], i[3], i[4]).set(v)

    def get_issues_df(self):
        return pd.read_csv("sample.csv")

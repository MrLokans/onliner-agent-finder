import os
import subprocess

import luigi

from agent_spider.finder import get_apartment_urls


class CrawlInitialURLsTask(luigi.Task):
    """
    Collects initial apartment bulletins URLS
    to be later parsed by scrapy.
    """

    def output(self):
        return luigi.LocalTarget('initial-urls.txt')

    def run(self):
        with self.output().open('w') as out_file:
            for url in get_apartment_urls():
                out_file.write('{}\n'.format(url))


class CrawlApartmentURLs(luigi.Task):

    output_path = luigi.Parameter(default='bulletins-pipeline.json')

    def requires(self):
        return CrawlInitialURLsTask()

    def input(self):
        return luigi.LocalTarget('initial-urls.txt')

    def output(self):
        return luigi.LocalTarget(self.output_path)

    def run(self):
        temp_file = '{}_tmp.json'.format(self.output_path)
        subprocess.check_output(['python', '-m', 'agent_spider.run',
                                 '-o', temp_file,
                                 '-u', self.input().path])
        os.rename(temp_file, self.output().path)

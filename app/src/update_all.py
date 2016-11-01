#!/usr/bin/env python
import re
import sys
import json
import logging
import urllib2
import argparse
import contextlib
from datetime import datetime
import update_package


class Update(object):
    """ Update docs
    """
    def __init__(self, github=None, blacklist=None, timeout=15,
                 loglevel=logging.INFO, logfile=None):

        if not github:
            github = "https://api.github.com/orgs/eea/repos?per_page=100&page=%s"
        self.github = github

        if not blacklist:
            blacklist = ()
        if isinstance(blacklist, (str, unicode)):
            blacklist = blacklist.split()
        self.blacklist = blacklist

        self.timeout = timeout
        self.repos = []

        self.logfile = logfile
        self.loglevel = loglevel
        self._logger = None


    @property
    def logger(self):
        """ Logger
        """
        if self._logger:
            return self._logger

        # Setup logger
        self._logger = logging.getLogger('githubdocs')
        self._logger.setLevel(self.loglevel)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(lineno)3d - %(levelname)7s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

        # Also log to file
        if self.logfile:
            fh = logging.FileHandler(self.logfile)
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

        return self._logger

    def update_repo(self, name):
        """ Update one repo
        """
        for skip in self.blacklist:
            if re.search(skip, name):
                self.logger("Skipping blacklisted repo %s", name)
                return

        try:
            update_package.update(name, logger=self.logger)
        except Exception, err:
            self.logger.exception(err)

    def update(self):
        """ Sync all repos
        """
        count = len(self.repos)
        self.logger.info('Syncing %s repositories', count)
        start = datetime.now()

        for repo in self.repos:
            name = repo.get('html_url', '')
            if not name:
                continue

            fork = repo.get("fork", "")
            if fork:
                self.logger.info("Skipping forked repo %s", name)
                continue

            self.update_repo(name)

        end = datetime.now()
        self.logger.info('DONE Syncing %s repositories in %s seconds',
                         count, (end - start).seconds)

    def __call__(self):
        """ Start syncing
        """
        self.repos = []
        links = [self.github % count for count in range(1,100)]
        try:
            for link in links:
                with contextlib.closing(urllib2.urlopen(
                        link, timeout=self.timeout)) as conn:
                    repos = json.loads(conn.read())
                    if not repos:
                        break
                    self.logger.info('Adding repositories from %s',  link)
                    self.repos.extend(repos)
            self.update()
        except Exception, err:
            self.logger.exception(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip", help=(
        "Blacklisted repo names space separeted, regexp enabled: "
        "e.g.: bise githubdocs eea.docker"))
    parser.add_argument("--repo", help=(
        "Github API link: e.g. https://api.github.com/orgs/eea"),
                        default="https://api.github.com/orgs/eea")

    args = parser.parse_args()
    repo = args.repo
    if repo:
        repo += '/repos?per_page=100&page=%s'

    skip = args.skip
    update = Update(github=repo, blacklist=skip)
    update()

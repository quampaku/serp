#!/usr/bin/env python

import requests
import json
from urllib.parse import urljoin


class GitLabScrapper():
    def __init__(self):
        self.host = 'http://192.168.6.29'
        self.session = requests.Session()
        self.session.headers.update({'PRIVATE-TOKEN': 'DtFnPvPNJPkExpVu3Gx6'})

    def get_issues_stats(self, page=1, per_page=20, scope='all'):
        payload = {
            'page': page,
            'per_page': per_page,
            'scope': scope
        }
        response = self.session.get(
            urljoin(self.host, '/api/v4/issues'),
            data=payload)
        return response

    def get_all_issues(self, page=1, per_page=20, scope='all'):
        payload = {
            'page': page,
            'per_page': per_page,
            'scope': scope
        }
        response = self.session.get(
            urljoin(self.host, '/api/v4/issues'),
            data=payload)
        return response

    def get_gitlab_stats(self):
        response = self.session.get(
            urljoin(self.host, '/api/v4/application/statistics'))
        return response

    def get_user_memberships(self, id):
        response = self.session.get(
            urljoin(self.host, '/api/v4/users/{0}/memberships'.format(id)))
        return response

    def get_project_languages(self, id):
        response = self.session.get(
            urljoin(self.host, '/api/v4/projects/{0}/languages'.format(id)))
        return response

    def get_all_projects(self, page=1, per_page=20,
                         order_by='created_at', sort='desc'):
        payload = {
            'statistics': 'yes',
            'page': page,
            'per_page': per_page,
            'order_by': order_by,
            'sort': sort
        }
        response = self.session.get(
            urljoin(self.host, '/api/v4/projects'),
            data=payload)
        return response

    def get_all_users(self, page=1, per_page=20,
                      order_by='id', sort='desc'):
        payload = {
            'page': page,
            'per_page': per_page,
            'order_by': order_by,
            'sort': sort
        }
        response = self.session.get(
            urljoin(self.host, '/api/v4/users'),
            data=payload)
        return response


scrapper = GitLabScrapper()

projects = scrapper.get_all_projects(page=1)
print(projects.headers)
# for project in projects:
#     laguages = scrapper.get_project_languages(project.get('id'))
#     print(laguages)
# print("""{id}, {name}, {description}, {name_with_namespace},
#          {owner}({state}), {created_at}, {last_activity_at},
#          {commit_count}""".format(
#     id=project.get('id'),
#     name=project.get('name'),
#     description=project.get('description'),
#     name_with_namespace=project.get('name_with_namespace'),
#     owner=project.get('owner', {}).get('name'),
#     state=project.get('owner', {}).get('state'),
#     created_at=project.get('created_at'),
#     last_activity_at=project.get('last_activity_at'),
#     commit_count=project.get('statistics', {}).get('commit_count')
#     )
# )

# users = scrapper.get_all_users()

# for user in users:
#     memberships = scrapper.get_user_memberships(user.get('id'))
#     print(memberships)
# stats = scrapper.get_gitlab_stats()
# print(stats)

# issues = scrapper.get_all_issues()
# print(json.dumps(issues, indent=4, sort_keys=True))

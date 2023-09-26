import argparse
from http import HTTPStatus
import requests
import json
import yaml

BASE_URL = 'https://gitlab.ics.muni.cz/api/v4'
TOKEN = '<TOKEN_HERE>'


def get_request(url, allowed_status_code=None):
    response = requests.get(url)
    # allowed status code is used when a request fails with a specific status code and the fail is accepted/expected
    if response.status_code == allowed_status_code:
        return None

    response.raise_for_status()
    return response.json()


def get_all_projects():
    projects = []
    url = BASE_URL + '/projects?pagination=keyset&per_page=100&order_by=id&sort=asc'

    while url:
        response = requests.get(url)
        response.raise_for_status()

        projects.extend(response.json())
        next = response.links.get('next', None)
        if next:
            url = next['url']
        else:
            url = None

    return projects


def get_last_commit(project_id):
    url = f'{BASE_URL}/projects/{project_id}/repository/commits'
    commits = get_request(url, HTTPStatus.NOT_FOUND)

    if not commits:
        return None

    last_commit = commits[0]
    return {
        'date': last_commit['committed_date'],
        'author': last_commit['committer_name'],
        'message': last_commit['message']
    }


def get_open_issues_count(project_id):
    url = f'{BASE_URL}/projects/{project_id}/issues_statistics'
    statistics = get_request(url)

    return statistics['statistics']['counts']['opened']


def get_pipeline_metadata(project_id):
    url = f'{BASE_URL}/projects/{project_id}/pipelines/latest?private_token={TOKEN}'
    # if project has no pipeline, request will return Forbidden
    pipeline = get_request(url, HTTPStatus.FORBIDDEN)

    if not pipeline:
        return None

    return {
        'source': pipeline['source'],
        'status': pipeline['status']
    }


def get_project_metadata(project_id):
    url = f'{BASE_URL}/projects/{project_id}?private_token={TOKEN}&simple=false'
    project = get_request(url)

    return project


def main():
    parser = argparse.ArgumentParser(prog='Extractor')
    parser.add_argument('--output', choices=['yaml', 'json'])
    args = parser.parse_args()

    output_format = args.output
    if not output_format:
        parser.error('Invalid output format')

    projects = get_all_projects()
    print(f'Got {len(projects)} projects\r', end='')
    parsed_projects = []
    statistics = {
        'number_of_porjects': len(projects),
        'owner_of_most_repos': {

        },
        'most_forked_repo': {
            'count': 0
        },
        'most_starred_repo': {
            'count': 0
        },
        'most_open_issues': {
            'count': 0
        }
    }

    repo_owners = {}

    for project in projects:
        pipeline_metadata = get_pipeline_metadata(project['id'])
        last_commit_metadata = get_last_commit(project['id'])
        open_issues_count = get_open_issues_count(project['id'])
        project_metadata = get_project_metadata(project['id'])

        parsed_projects.append({
            'name': project['name'],
            'description': project['description'],
            'open_issues': open_issues_count,
            'last_commit_metadata': last_commit_metadata,
            'owned_by_kind': project['namespace']['kind'],
            'pipeline_metadata': pipeline_metadata
        })

        if open_issues_count > statistics['most_open_issues']['count']:
            statistics.update({
                'most_open_issues': {
                    'name': project['name'],
                    'count': open_issues_count
                }
            })

        stars = project_metadata['star_count']
        if stars > statistics['most_starred_repo']['count']:
            statistics.update({
                'most_starred_repo': {
                    'name': project['name'],
                    'count': stars
                }
            })

        if 'forks_count' in project_metadata:  # if forking is disallowed by permissions, or project is archived, forks_count won't appear in metadata
            forks = project_metadata['forks_count']
            if forks > statistics['most_forked_repo']['count']:
                statistics.update({
                    'most_forked_repo': {
                        'name': project['name'],
                        'count': forks
                    }
                })

        owner = project_metadata['namespace']['name']
        if owner in repo_owners:
            repo_owners[owner] = repo_owners[owner] + 1
        else:
            repo_owners[owner] = 1

        print(f'\rParsed {len(parsed_projects)} out of {len(projects)}', end='')

    most_repos_owner = max(repo_owners, key=repo_owners.get)
    statistics.update({
        'owner_of_most_repos': most_repos_owner,
        'count': repo_owners[most_repos_owner]
    })
    output = {
        'projects': parsed_projects,
        'statistics': statistics
    }
    if output_format == 'json':
        print(json.dumps(output, ensure_ascii=False, indent=1))
    elif output_format == 'yaml':
        print(yaml.dump(output, allow_unicode=True, indent=1))


if __name__ == '__main__':
    main()

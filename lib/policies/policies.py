import requests
from pyramda import map, contains

from common import environments
from common.handlers import handle_rest_response, handle_rest_response_with_body
from templates.templates import load_template


def is_present(env: str, vhost: str, name: str) -> bool:
    return contains(name, get_policies(env=env, vhost=vhost))


# noinspection PyDeepBugsSwappedArgs
def get_policies(env: str, vhost: str) -> dict:
    broker = environments.get_broker_info(env)
    url = 'https://{}/api/policies/{}'.format(broker['host'], vhost)
    response = requests.get(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
    return map(lambda i: i['name'], response.json())


# noinspection PyDeepBugsSwappedArgs
def create_policy(env: str, vhost: str, name: str, policy: dict) -> None:
    broker = environments.get_broker_info(env)
    url = 'https://{}/api/policies/{}/{}'.format(broker['host'], vhost, name)
    response = requests.put(url=url, auth=(broker['user'], broker['passwd']), json=policy)
    handle_rest_response_with_body(response=response, body=policy, url=url)


def delete_policy(env: str, vhost: str, name: str) -> None:
    broker = environments.get_broker_info(env)
    url = 'https://{}/api/policies/{}/{}'.format(broker['host'], vhost, name)
    response = requests.delete(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)


def create_policy_from_template(env: str, vhost: str, name: str, template: str) -> None:
    policy = load_template(template)
    create_policy(env=env, vhost=vhost, name=name, policy=policy)

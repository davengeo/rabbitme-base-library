from typing import List

import requests
from pyramda import map

from common.handlers import handle_rest_response, handle_rest_response_with_body


class Binding(object):

    def __init__(self, obj: dict):
        self.source = obj.get('source')
        self.destination = obj.get('destination')
        self.destination_type = obj.get('destination_type')
        self.routing_key = obj.get('routing_key')
        self.arguments = obj.get('arguments')
        self.properties_key = obj.get('properties_key')

    def to_dict(self) -> dict:
        return {
            'source': self.source,
            'destination': self.destination,
            'destination_type': self.destination_type,
            'routing_key': self.routing_key,
            'arguments': self.arguments
        }

    def body(self) -> dict:
        return {
            'routing_key': self.routing_key,
            'arguments': self.arguments
        }

    def path(self) -> str:
        binding_type = 'e' if self.destination_type == 'exchange' else 'q'
        return 'e/{}/{}/{}'.format(self.source, binding_type, self.destination)

    def equals(self, other: object) -> bool:
        if not isinstance(other, Binding):
            return NotImplemented
        return self.source == other.source and self.destination == other.destination \
               and self.routing_key == other.routing_key and self.destination_type == other.destination_type \
               and self.arguments == other.arguments    # noqa: E127


def create_binding(broker: dict, vhost: str, binding: Binding) -> None:
    url = 'https://{}/api/bindings/{}/{}'.format(broker['host'], vhost, binding.path())
    body = binding.body()
    response = requests.post(url=url, auth=(broker['user'], broker['passwd']), json=body)
    handle_rest_response_with_body(response=response, url=url, body=body)


def delete_binding(broker: dict, vhost: str, binding: Binding) -> None:
    url = 'https://{}/api/bindings/{}/{}/{}'.format(broker['host'],
                                                    vhost, binding.path(), binding.properties_key)
    response = requests.delete(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)


def get_bindings_from_source(broker: dict, vhost: str, source: str) -> List[Binding]:
    url = 'https://{}/api/exchanges/{}/{}/bindings/source'.format(broker['host'], vhost, source)
    response = requests.get(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
    return map(lambda i: Binding(i), response.json())


# noinspection PyDeepBugsSwappedArgs
def get_bindings(broker: dict, vhost: str) -> List[Binding]:
    url = 'https://{}/api/bindings/{}'.format(broker['host'], vhost)
    response = requests.get(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
    return map(lambda i: Binding(i), response.json())

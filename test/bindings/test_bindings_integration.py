import os

import pytest
from assertpy import assert_that

from bindings.bindings import Binding, create_binding, get_bindings_from_source, delete_binding
from common.config import Config
from common.environments import Environments
from common.templates import Template
from exchanges import exchanges
from exchanges.exchanges import create_exchange, delete_exchange
from queues import queues

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
envs = Environments(path_file=config.get_file_path('config_files', 'tme_environments.json'))
template: Template = Template(config.get_path('template_files'))


@pytest.mark.integration
def test_should_create_bindings_between_exchange_and_queue() -> None:
    test_env: dict = envs.get_env(env='test')
    exchange = template.load_template(name='exchanges/fanout')
    create_exchange(broker=test_env, vhost='EA', name='origin-sample', exchange=exchange)
    queue = template.load_template(name='queues/sample-queue')
    queues.create_queue(broker=test_env, vhost='EA', name='destination-sample', queue=queue)
    binding = Binding(
        {
            'source': 'origin-sample',
            'destination': 'destination-sample',
            'destination_type': 'queue',
            'routing_key': '', 'arguments': {}
        })
    create_binding(broker=test_env, vhost='EA', binding=binding)
    result = get_bindings_from_source(broker=test_env, vhost='EA', source='origin-sample')
    assert_that(result[0].to_dict()).is_equal_to(binding.to_dict())
    delete_binding(broker=test_env, vhost='EA', binding=result[0])
    result = get_bindings_from_source(broker=test_env, vhost='EA', source='origin-sample')
    assert_that(result).is_empty()
    queues.delete_queue(broker=test_env, vhost='EA', name='destination-sample')
    result = queues.is_present(broker=test_env, vhost='EA', name='destination-sample')
    assert_that(result).is_false()
    delete_exchange(broker=test_env, vhost='EA', name='origin-sample')
    result = exchanges.is_present(broker=test_env, vhost='EA', name='origin-sample')
    assert_that(result).is_false()

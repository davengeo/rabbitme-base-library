import os

import pytest
from assertpy import assert_that

from common.config import Config
from common.environments import Environments
from messages.messages import build_conn_string, AmqpSenderConsumer
from ..common.integration_credentials import Credentials

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
envs = Environments(path_file=config.get_file_path('config_files', 'tme_environments.json'))
sender_account = Credentials(path_file=config.get_file_path('config_files', 'accounts.json')).get_account('sender-test')
consumer_account = Credentials(path_file=config.get_file_path('config_files', 'accounts.json')).get_account(
    'consumer-test')


@pytest.mark.debug
def test_should_get_definitions_from_env() -> None:
    host: str = envs.get_env('test').get('host')
    conn_string = build_conn_string(host=host, name=sender_account.get('user'),
                                    passwd=sender_account.get('passwd'), vhost=sender_account.get('vhost'))
    sender = AmqpSenderConsumer(conn_string=conn_string)
    sender.publish_message(exchange=sender_account.get('artefact'), routing_key='MARKET.TGB',
                           message={'message': 'you are a prick'})
    conn_string = build_conn_string(host=host, name=consumer_account.get('user'),
                                    passwd=consumer_account.get('passwd'),
                                    vhost=consumer_account.get('vhost'))
    consumer = AmqpSenderConsumer(conn_string=conn_string)
    message = consumer.receive_message(consumer_account.get('artefact'))
    assert_that(message).is_equal_to({'message': 'you are a prick'})

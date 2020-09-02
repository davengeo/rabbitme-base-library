import os

import pytest
from assertpy import assert_that

from common.config import Config
from common.environments import Environments
from messages.messages import build_conn_string, AmqpSenderConsumer

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
envs = Environments(path_file=config.get_file_path('config_files', 'tme_environments.json'))


@pytest.mark.debug
def test_should_get_definitions_from_env() -> None:
    host: str = envs.get_env('test').get('host')
    conn_string = build_conn_string(host=host, name='b2b-sharing_test',
                                    passwd='SoiWUZcQ+A', vhost='connected_technologies_B2B')
    sender = AmqpSenderConsumer(conn_string=conn_string)
    sender.publish_message(exchange='mileage.pub.b2b-sharing', routing_key='MARKET.TGB',
                           message={'message': 'you are a prick'})
    conn_string = build_conn_string(host=host, name='mileage-tgb-pilot_test',
                                    passwd='test123', vhost='connected_technologies_B2B')
    consumer = AmqpSenderConsumer(conn_string=conn_string)
    message = consumer.receive_message('mileage.MARKET.TGB.sub.mileage-tgb-pilot')
    assert_that(message).is_equal_to({'message': 'you are a prick'})

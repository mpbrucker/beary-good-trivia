import os
from collections import namedtuple
from urllib.parse import urlparse

# Try all of these. We use MQTT_URL locally; different RabbitMQ hosting
# providers configure Heroku with different environment variables, and we want
# to be able to work with all of them.
MQTT_ENV_VARS = ['MQTT_URL', 'CLOUDMQTT_URL', 'CLOUDAMQP_URL']
MQTT_URL = next((value for value in (os.environ.get(name) for name in MQTT_ENV_VARS) if value),
                "mqtt://localhost")

MQTTConfig = namedtuple(
    'MQTTConfig',
    ['hostname', 'port', 'username', 'password', 'auth'])


def parse_url(url):
    url = urlparse(MQTT_URL)

    hostname = url.hostname
    username = url.username
    password = url.password
    port = url.port or 1883

    if url.path:
        username = url.path[1:] + ':' + username

    auth = dict(username=username, password=password) if username else None

    return MQTTConfig(hostname, port, username, password, auth)


if MQTT_URL:
    config = parse_url(MQTT_URL)

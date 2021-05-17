"""
Collection of utilities until we find a better place to put them.
"""
import copy

import arrow
import base64
import hashlib
import json
import logging
import os

from addict import Dict
from dotenv import find_dotenv, load_dotenv
from time import time

from ddd.domain.building_block import BuildingBlock
from ddd.domain.entity import Entity

logger = logging.getLogger(__file__)

# Variables

TRUTHY = ["True", "true", "1", 1, True]

# Functions

def read_config():
    """
    Read config (from environment variables).

    Returns:
        dict - the config dict
    """
    config = Dict({
        'env': os.getenv("ENV"),
        'debug': os.getenv("DEBUG"),
        'max_concurrent_actions':
            int(os.getenv("MAX_CONCURRENT_ACTIONS", "10")),
        'top_level_package_name': os.getenv("TOP_LEVEL_PACKAGE_NAME"),
        'http': {
            'debug': os.getenv("HTTP_DEBUG") in TRUTHY,
            'port': os.getenv("HTTP_PORT"),
        },
        'database': {
            'type': os.getenv("DATABASE_TYPE"),
            'postgres': {
                'dsn': os.getenv("POSTGRES_DSN"),
            },
        },
        'auth': {
            'full_access_token': os.getenv("AUTH_FULL_ACCESS_TOKEN"),
        },
        'pubsub': {
            'domain': {
                'provider': os.getenv("DOMAIN_PUBSUB_PROVIDER"),
                'topic': os.getenv("DOMAIN_PUBSUB_TOPIC"),
                'group': os.getenv("DOMAIN_PUBSUB_GROUP"),
            },
            'interchange': {
                'provider': os.getenv("INTERCHANGE_PUBSUB_PROVIDER"),
                'topic': os.getenv("INTERCHANGE_PUBSUB_TOPIC"),
                'group': os.getenv("INTERCHANGE_PUBSUB_GROUP"),
            },
            'kafka': {
                'bootstrap_servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            },
            'azure': {
                'namespace': os.getenv("AZURE_EVENT_HUBS_NAMESPACE"),
                'namespace_conn_string':
                    os.getenv("AZURE_EVENT_HUBS_NAMESPACE_CONN_STRING"),
                'checkpoint_store_conn_string':
                    os.getenv("AZURE_EVENT_HUBS_CHECKPOINT_STORE_CONN_STRING"),
                'blob_container_name':
                    os.getenv("AZURE_EVENT_HUBS_BLOB_CONTAINER_NAME"),
            },
        },
        'jobs': {
            'scheduler': {
                'type': os.getenv("JOBS_SCHEDULER_TYPE"),
                'dsn': os.getenv("JOBS_SCHEDULER_DSN"),
            },
        },
        'slack': {
            'token': os.getenv("SLACK_TOKEN"),
        },
        'log': {
            'enabled': True,
            'slack': {
                'enabled': os.getenv("LOG_SLACK_ENABLED") in TRUTHY,
                'errors': {
                    'channel': os.getenv("LOG_SLACK_CHANNEL_ERRORS"),
                }
            },
            'kibana': {
                'enabled': os.getenv("LOG_KIBANA_ENABLED") in TRUTHY,
                'url': os.getenv("LOG_KIBANA_URL"),
                'username': os.getenv("LOG_KIBANA_USERNAME"),
                'password': os.getenv("LOG_KIBANA_PASSWORD"),
            }
        },
        'base_url': os.getenv('BASE_URL', 'empty-base-url'),
        'api': {

        },
        'tasks': {
            'username': os.getenv('TASK_USERNAME'),
            'password': os.getenv('TASK_PASSWORD'),
        }
    })

    return config

def load_env_file():
    """
    Load environment variables from env file.
    """
    filename = os.getenv("ENV_FILE", "env")

    loaded = \
        load_dotenv(
            find_dotenv(filename=filename)
        )

    if not loaded:
        raise Exception(f"Couldn't load env file with name: '{filename}'")

def sri(path):
    """
    Calculate the SRI checksum of a file at 'path'.
    """
    with open(path, "r") as f:
        input = f.read()

        if isinstance(input, str):
            # This is so we can handle strings as input in Python 3
            input = input.encode()

        hash = hashlib.sha256(input).digest()
        hash_base64 = base64.b64encode(hash).decode()

        return 'sha256-{}'.format(hash_base64)

def dot_pop(the_dict, path):
    """
    Like native dict.pop(), but supports dot-based paths.
    Ex. dot_pop(obj, 'my.dot.path.to.field')
    """
    keys = path.split('.')
    if the_dict != None and keys[0] in the_dict:
        if len(keys) == 1:
            the_dict.pop(keys[0])
        else:
            dot_pop(the_dict[keys[0]], ".".join(keys[1:]))

def flatten(the_dict):
    """
    Flatten 'the_dict' by replacing any Entity with it's
    __dict__ version.

    TODO: Recurse..
    """
    for key, value in the_dict.items():
        if isinstance(the_dict[key], Entity):
            the_dict[key] = the_dict[key].__dict__
    return the_dict

def get_for_compare(obj, ignore_fields=None):
    """
    Get representation for comparision.

    - Deep copy
    - Flatten entities
    - Pop 'ignore_fields'
    """
    ignore_fields = ignore_fields if ignore_fields is not None else []

    if type(obj) in [str, int, float]:
        return obj
    elif type(obj) == list:
        return [get_for_compare(i) for i in obj]

    obj = copy.deepcopy(obj.__dict__)

    for key, value in obj.items():
        if isinstance(value, BuildingBlock):
            obj[key] = get_for_compare(value)
        elif isinstance(value, list):
            for n, i in enumerate(value):
                value[n] = get_for_compare(i)

    obj = flatten(obj)

    for field in ignore_fields:
        dot_pop(obj, field)

    return obj

# Dates

def date_or_none(string):
    if string is None:
        return None
    return arrow.get(string)

def iso_or_none(date):
    if date is None:
        return None
    return date.isoformat()

def str_or_none(string):
    if string is None:
        return None
    return str(string)

def dates_intersection(
    first_start,
    first_end,
    second_start,
    second_end,
    timezone,
):
    if None in [first_start, first_end, second_start, second_end]:
        return None

    first_start.to(timezone)
    first_end.to(timezone)
    second_start.to(timezone)
    second_end.to(timezone)

    start = None
    end = None

    if first_start > second_start:
        start = first_start
    else:
        start = second_start

    if first_end < second_end:
        end = first_end
    else:
        end = second_end

    if start > end:
        return None

    return [start, end]

# Lists

def first_or_none(list_):
    return list_[0] if len(list_) > 0 else None

# Logic

def is_true(value):
    return value in TRUTHY

# Parameters in http adapter

def read_string_from_query(request, param):
    return request.args.get(param)

def read_string_from_body(request, param):
    return request.json.get(param)

def read_integer_from_query(request, param):
    return int(request.args.get(param, 0))

def read_integer_from_body(request, param):
    return int(request.json.get(param, 0))

def read_boolean_from_query(request, param):
    value = request.args.get(param, None)
    if value is not None:
        return value in TRUTHY
    return None

def read_boolean_from_body(request, param):
    value = request.json.get(param, None)
    if value is not None:
        return value in TRUTHY
    return None

def read_list_from_query(request, param):
    """
    Read argument from request query as list.
    """
    if f"{param}[]" in request.args:
        value = request.args.getlist(f"{param}[]", [])
    else:
        value = request.args.getlist(param, [])
    return value

def read_list_from_body(request, param):
    """
    Read argument from request body as list.
    """
    if f"{param}[]" in request.json:
        value = request.json.get(f"{param}[]", [])
    else:
        value = request.json.get(param, [])
    return value

def read_entity_id_from_query(request, param, entity_class):
    """
    Read argument from query as entity ID.
    """
    value = request.args.get(param)

    if value:
        value = entity_class(value)

    return value

def read_entity_id_from_body(request, param, entity_class):
    """
    Read argument from body json as entity ID.
    """
    value = request.json.get(param)

    if value:
        value = entity_class(value)

    return value

def read_entity_ids_from_query(request, param, entity_class):
    """
    Read argument from query as list of entity IDs.
    """
    values = []

    if f"{param}[]" in request.args:
        values = request.args.getlist(f"{param}[]", [])
    else:
        values = request.args.getlist(param, [])

    values = [entity_class(v) for v in values]

    return values

def read_entity_ids_from_body(request, param, entity_class):
    """
    Read argument from body json as list of entity IDs.
    """
    values = []

    if f"{param}[]" in request.json:
        values = request.json.get(f"{param}[]", [])
    else:
        values = request.json.get(param, [])

    values = [entity_class(v) for v in values]

    return values

# Classes

class catch_time(object):
    """
    Context manager that measures the execution time.
    """
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.execution_time = time() - self.start


class MockResponse(object):
    """
    Used to mock responses returned from a requests package request.
    """
    def __init__(
        self,
        status_code,
        content,
        content_type,
        headers=None,
        url="mock-url"
    ):
        headers = headers if headers is not None else {}

        self.status_code = status_code
        self.content_type = content_type
        self.headers = headers
        self.url = url

        # Make sure content is a byte string
        if type(content) is not str:
            content = json.dumps(content)

        self._content = content.encode('utf-8')

    async def content(self):
        return self._content

    async def json(self):
        return json.loads(self._content)

    async def text(self):
        return self._content

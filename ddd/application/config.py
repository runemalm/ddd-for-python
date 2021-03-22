import asyncio
import os
import uvloop

from addict import Dict
from dotenv import find_dotenv, load_dotenv


class Config(object):
    """
    A class for holding the settings as defined by env file.

    Extend 'Config' if you want to add config settings for your context.

    We use 'addict' to be able to use dot-notation
    for referencing dict values.
    """
    TRUTHY = ["True", "true", "1", 1, True]

    def __init__(self, env_file_path=None):
        super().__init__()

        self._declare_settings()
        self._find_env_file(env_file_path)
        self._load_env_file()
        self._read_config()
        self._get_loop()

    def _declare_settings(self):
        """
        Declare all settings as 'None'.
        """
        self.env = None
        self.debug = None
        self.max_concurrent_actions = None
        self.top_level_package_name = None

        self.loop = Dict({
            'type': None,
            'instance': None,
        })

        self.http = Dict({
            'debug': None,
            'port': None,
        })
        self.database = Dict({
            'type': None,
            'postgres': Dict({
                'dsn': None,
            }),
        })
        self.auth = Dict({
            'full_access_token': None,
        })
        self.pubsub = Dict({
            'domain': Dict({
                'provider': None,
                'topic': None,
                'group': None,
            }),
            'interchange': Dict({
                'provider': None,
                'topic': None,
                'group': None,
            }),
            'kafka': Dict({
                'bootstrap_servers': None,
            }),
            'azure': Dict({
                'namespace': None,
                'namespace_conn_string': None,
                'checkpoint_store_conn_string': None,
                'blob_container_name': None,
            }),
        })
        self.jobs = Dict({
            'scheduler': Dict({
                'type': None,
                'dsn': None,
            })
        })
        self.slack = Dict({
            'token': None,
        })
        self.log = Dict({
            'enabled': None,
            'slack': Dict({
                'enabled': None,
                'errors': Dict({
                    'channel': None,
                })
            }),
            'kibana': Dict({
                'enabled': None,
                'url': None,
                'username': None,
                'password': None,
            }),
        })
        self.base_url = None
        self.tasks = Dict({
            'runner': Dict({
                'username': None,
                'password': None,
            }),
        })

    def _find_env_file(self, env_file_path):
        """
        Tries to find the env file path.

        Either as defined by 'env_file_path' or by searching recursively
        upwards from current workding dir.

        Throws error if no env file could be found, since it's required
        to launch the app.
        """
        if env_file_path in [None, ""]:
            env_file_path = \
                find_dotenv(
                    filename=os.getenv('ENV_FILE'),
                    raise_error_if_not_found=True,
                    usecwd=True,
                )
        self.env_file_path = env_file_path

    def _load_env_file(self):
        """
        Loads the environment file by loading the env vars defined in it
        so that they become accessible using 'os.getenv()'.
        """
        load_dotenv(
            dotenv_path=self.env_file_path,
        )

    def _read_config(self):
        """
        Read settings from env vars into this object's member variables.
        """
        self.env = os.getenv('ENV')
        self.debug = os.getenv("DEBUG")
        self.max_concurrent_actions = \
            int(os.getenv("MAX_CONCURRENT_ACTIONS", "10"))
        self.top_level_package_name = \
            os.getenv("TOP_LEVEL_PACKAGE_NAME")

        self.loop.type = os.getenv("LOOP_TYPE")

        self.http.debug = os.getenv("HTTP_DEBUG") in self.TRUTHY
        self.http.port = os.getenv("HTTP_PORT")

        self.database.type = os.getenv("DATABASE_TYPE")
        self.database.postgres.dsn = os.getenv("POSTGRES_DSN")

        self.auth.full_access_token = os.getenv("AUTH_FULL_ACCESS_TOKEN")

        self.pubsub.domain.provider = os.getenv("DOMAIN_PUBSUB_PROVIDER")
        self.pubsub.domain.topic = os.getenv("DOMAIN_PUBSUB_TOPIC")
        self.pubsub.domain.group = os.getenv("DOMAIN_PUBSUB_GROUP")

        self.pubsub.interchange.provider = \
            os.getenv("INTERCHANGE_PUBSUB_PROVIDER")
        self.pubsub.interchange.topic = \
            os.getenv("INTERCHANGE_PUBSUB_TOPIC")
        self.pubsub.interchange.group = \
            os.getenv("INTERCHANGE_PUBSUB_GROUP")

        self.pubsub.kafka.bootstrap_servers = \
            os.getenv("KAFKA_BOOTSTRAP_SERVERS")

        self.pubsub.azure.namespace = \
            os.getenv("AZURE_EVENT_HUBS_NAMESPACE")
        self.pubsub.azure.namespace_conn_string = \
            os.getenv("AZURE_EVENT_HUBS_NAMESPACE_CONN_STRING")
        self.pubsub.azure.checkpoint_store_conn_string = \
            os.getenv("AZURE_EVENT_HUBS_CHECKPOINT_STORE_CONN_STRING")
        self.pubsub.azure.blob_container_name = \
            os.getenv("AZURE_EVENT_HUBS_BLOB_CONTAINER_NAME")

        self.jobs.scheduler.type = os.getenv("JOBS_SCHEDULER_TYPE")
        self.jobs.scheduler.dsn = os.getenv("JOBS_SCHEDULER_DSN")

        self.slack.token = os.getenv("SLACK_TOKEN")

        self.log.enabled = os.getenv("LOG_ENABLED") in self.TRUTHY

        self.log.slack.enabled = \
            os.getenv("LOG_SLACK_ENABLED") in self.TRUTHY
        self.log.slack.errors.channel = \
            os.getenv("LOG_SLACK_CHANNEL_ERRORS")

        self.log.kibana.enabled = \
            os.getenv("LOG_KIBANA_ENABLED") in self.TRUTHY
        self.log.kibana.url = os.getenv("LOG_KIBANA_URL")
        self.log.kibana.username = os.getenv("LOG_KIBANA_USERNAME")
        self.log.kibana.password = os.getenv("LOG_KIBANA_PASSWORD")

        self.base_url = os.getenv('BASE_URL', 'empty-base-url')

        self.tasks.runner.username = os.getenv('TASK_RUNNER_USERNAME')
        self.tasks.runner.password = os.getenv('TASK_RUNNER_PASSWORD')

    def _get_loop(self):
        """
        Create the loop,
        add it to asyncio and this config.
        """
        loop = None

        if self.loop.type == "uvloop":
            loop = uvloop.new_event_loop()
        else:
            loop = asyncio.get_event_loop()

        asyncio.set_event_loop(loop)

        self.loop.instance = loop

import copy
import json
import logging
import sys

from addict import Dict

from ddd.infrastructure.infrastructure_service import InfrastructureService

from logging.config import dictConfig

from cmreslogging.handlers import CMRESHandler


class LogService(InfrastructureService):
    """
    A log service for logging.
    """
    def __init__(
        self,
        kibana_config,
        slack_config,
        enabled=True,
    ):
        super().__init__(log_service="dummy")

        self.kibana_config = Dict(kibana_config)
        self.slack_config = Dict(slack_config)
        self.enabled = enabled

        # Create the logger
        self._set_modules_logger_levels()
        self._create_logger()

    async def start(self):
        pass

    async def stop(self):
        pass

    def _set_modules_logger_levels(self):
        """
        Sets log level of used modules.

        Effectively remove/add unwanted/wanted logs of third-party packages
        from/to console output.
        """
        logging.getLogger("aiokafka").setLevel(logging.WARNING)
        logging.getLogger("azure").setLevel(logging.WARNING)
        logging.getLogger("elasticsearch").setLevel(logging.WARNING)
        logging.getLogger("uamqp").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def info(self, message, extra=None, exc_info=False):
        """
        Log an info level message.
        """
        if self.enabled:
            LogService._do_log(
                logger=self.logger,
                level="info",
                message=message,
                extra=extra,
                exc_info=exc_info,
            )

    def warning(self, message, extra=None, exc_info=False):
        """
        Log an warning level message.
        """
        if self.enabled:
            LogService._do_log(
                logger=self.logger,
                level="warning",
                message=message,
                extra=extra,
                exc_info=exc_info,
            )

    def error(self, message, extra=None, exc_info=False):
        """
        Log an error level message.
        """
        if self.enabled:
            LogService._do_log(
                logger=self.logger,
                level="error",
                message=message,
                extra=extra,
                exc_info=exc_info,
            )

    def debug(self, message, extra=None, exc_info=False):
        """
        Log an debug level message.
        """
        if self.enabled:
            LogService._do_log(
                logger=self.logger,
                level="debug",
                message=message,
                extra=extra,
                exc_info=exc_info,
            )

    async def log_request(self, message, method, url, params):
        """
        Convenience method to log the request to an api.
        """
        if self.enabled:

            params = copy.deepcopy(params)

            if 'token' in params:
                params['token'] = "(hidden)"

            if 'password' in params:
                params['password'] = "(hidden)"

            self.debug(
                message,
                extra={
                    'method': method,
                    'url': url,
                    'params': params,
                }
            )

    async def log_response(self, message, method, url, params, response):
        """
        Convenience method to log the response of an api request.
        """
        if self.enabled:
            content = response.content
            params = copy.deepcopy(params)

            if response.headers.get('content-type') == 'application/json':
                content = json.loads(await response.content())
            else:
                content = await response.content()

            if 'token' in params:
                params['token'] = "(hidden)"

            if 'password' in params:
                params['password'] = "(hidden)"

            self.debug(
                message,
                extra={
                    'method': method,
                    'url': url,
                    'params': params,
                    'status_code': response.status_code,
                    'content_type': response.headers.get('content-type'),
                    'response': content,
                }
            )

    # Helpers

    @classmethod
    def _do_log(
        cls,
        logger,
        level,
        message,
        extra,
        exc_info,
    ):
        """
        Helper to do the actual logging.

        Returns:
            Nothing if logging succeeds.

        Raises:
            Exception if logging fails.
        """
        e = None

        if extra is not None and extra != {}:
            e = {'extra': extra}

        getattr(logger, level)(
            message,
            extra=e,
            exc_info=exc_info,
        )

    def _create_logger(self):

        # TODO: Merge this into logging_config below:
        logging.basicConfig(
            format=
            "[%(asctime)s] [%(levelname)8s] --- "
            "%(message)s (%(filename)s:%(lineno)s)",
            stream=sys.stdout,
            level=logging.DEBUG
        )

        logging_config = dict(
            disable_existing_loggers=False,
            version=1,
            formatters={
                'f': {
                    'format': (
                        "%(asctime)s %(name)-12s %(levelname)-8s "
                        "%(message)s"
                    )
                }
            },
            handlers={
                'console': {
                    'class': "logging.StreamHandler",
                    'formatter': None,
                    'level': logging.INFO,
                    'stream': "ext://sys.stdout"
                },
                'kibana': {
                    'class': "cmreslogging.handlers.CMRESHandler",
                    'formatter': None,
                    'level': logging.DEBUG,
                    'hosts': f"{self.kibana_config.url}",
                    'auth_type': CMRESHandler.AuthType.BASIC_AUTH,
                    'auth_details': (
                        self.kibana_config.username,
                        self.kibana_config.password,
                    ),
                    'use_ssl': "443" in self.kibana_config.url
                    if self.kibana_config.url else False,
                    'verify_ssl': "443" in self.kibana_config.url
                    if self.kibana_config.url else False,
                    'es_index_name': "logstash",
                    'es_additional_fields': {
                        'source': self.kibana_config.source,
                    },
                    'raise_on_indexing_exceptions': False
                },
                'slack-error': {
                    'level': 'ERROR',
                    'api_key': self.slack_config.token,
                    'username': self.slack_config.bot_username,
                    'class': 'slacker_log_handler.SlackerLogHandler',
                    'channel': f"#{self.slack_config.errors.channel}",
                },
            },
            loggers={
                'ddd-for-python': {
                    'level': logging.DEBUG,
                    'propagate': True,
                    'filters': [],
                    'handlers': [],
                }
            }
        )

        # Add handlers
        handlers = ['console']

        if self.kibana_config.enabled:
            handlers.append('kibana')

        if self.slack_config.enabled:
            handlers.append('slack-error')

        logging_config['loggers']['ddd-for-python']['handlers'] = handlers

        dictConfig(logging_config)

        self.logger = logging.getLogger("ddd-for-python")

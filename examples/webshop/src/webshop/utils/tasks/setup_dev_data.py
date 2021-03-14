import arrow

from ddd.utils.tasks.task import Task as BaseTask


class Task(BaseTask):

    def __init__(self, config, deps_mgr, args_str):
        super().__init__(
            config=config,
            deps_mgr=deps_mgr,
            args_str=args_str,
            makes_requests=False,
        )

    def add_args(self, parser):
        parser.add_argument(
            "--dummy",
            help="a dummy argument, ignored",
            type=str,
        )

    async def run(self):
        raise NotImplementedError()

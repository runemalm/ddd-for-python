import argparse
import asyncio
import importlib
import os

from ddd.utils.utils import load_env_file


def _parse_args():
    """
    Parse the CLI arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("task", help="the filename of the task", type=str)
    parser.add_argument("--args", help="the task arguments", type=str)

    args = parser.parse_args()

    return args.task, args.args

def read_config():
    """
    Read config dict using 'read_config()' in utils.

    NOTE:
        'TOP_LEVEL_PACKAGE_NAME' needs to be defined in the env file.
    """
    path = f"{os.getenv('TOP_LEVEL_PACKAGE_NAME')}.utils.utils"

    module = importlib.import_module(path, package=None)

    func = getattr(module, "read_config")

    config = func()

    return config

def find_task_class(config, task_name):

    # Search in project's 'tasks' folder
    try:
        path = f"{config.top_level_package_name}.utils.tasks.{task_name}"
        module = importlib.import_module(path, package=None)
        task_class = getattr(module, "Task")
    except ModuleNotFoundError:

        # Search in ddd lib's 'tasks' folder
        module = importlib.import_module(f"ddd.utils.tasks.{task_name}", package=None)
        task_class = getattr(module, "Task")

    return task_class


if __name__ == "__main__":
    """
    Run the task.
    """
    # Config
    load_env_file()
    config = read_config()

    # Get dependency manager
    path = f"{config.top_level_package_name}.utils.dep_mgr"

    module = importlib.import_module(path, package=None)

    mgr_class = getattr(module, "DependencyManager")

    deps_mgr = \
        mgr_class(
            config=config,
        )

    # Args
    task, args = _parse_args()

    # Get task
    task_class = find_task_class(config=config, task_name=task)

    # Run
    task = \
        task_class(
            config=config,
            deps_mgr=deps_mgr,
            args_str=args,
        )

    asyncio.get_event_loop().run_until_complete(
        task._run()
    )

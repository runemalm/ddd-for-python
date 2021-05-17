import importlib
import inspect
from pathlib import Path
import pkgutil

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
        pass

    async def run(self):

        # Migrate
        results = {}

        repositories = self._get_repositories()

        for repository in repositories:

            name = self._get_name_of_root(repository)

            if name not in results:
                results[name] = {
                    'count': 0,
                }

            aggregates = await repository.get_all_not_on_latest_version()

            for aggregate in aggregates:
                await repository.save(aggregate)
                results[name]['count'] += 1

        # Print results
        rows = []

        for name, data in results.items():
            rows.append(
                f"* Migrated '{data['count']}' {name.lower()}s"
            )

        self.log_service.info(
            "---------------------------------------\nRESULT:\n\n"
            "{}\n"
            "---------------------------------------".
            format(
                "\n".join(rows)
            )
        )

    def _get_repositories(self):
        """
        Get all repositories.
        """
        repositories = []

        modules = self._get_modules()

        for module, path in modules.items():

            spec = importlib.util.spec_from_file_location(module, f"{path}.py")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            module_classes = inspect.getmembers(mod, inspect.isclass)

            ignored_classes = [
                "MemoryRepository", "PostgresRepository",
                "MemoryEventRepository", "PostgresEventRepository",
                "Repository",
            ]

            for name, cls in module_classes:
                if self._camel_to_snake(name) == cls.__module__:
                    if "Repository" in name:
                        if name not in ignored_classes:
                            _type = self.config.database.type
                            if _type.capitalize() in name:
                                func_name = name
                                func_name = \
                                    func_name.replace(_type.capitalize(), "")
                                func_name = self._camel_to_snake(func_name)
                                func_name = f"get_{func_name}"
                                repository = getattr(self.deps_mgr, func_name)()
                                repositories.append(repository)

        return repositories

    def _get_modules(self, path=None):
        """
        Get all modules under the '<package_name>/repositories' folder.
        """
        if path is None:
            path = \
                Path(__file__).parents[3] / \
                f"{self.config.top_level_package_name}/repositories"

        modules = {}

        for loader, module_name, is_pkg in pkgutil.walk_packages([path]):

            if is_pkg:
                modules.update(
                    self._get_modules(
                        path=path / module_name
                    )
                )
            else:
                modules[module_name] = str(path / module_name)

        return modules

    def _get_name_of_root(self, repository):
        return repository.aggregate_cls.__name__

    def _camel_to_snake(self, string):
        """
        Get camel case version of snake case 'string'
        """
        return ''.join(
            ['_' + c.lower() if c.isupper() else c for c in string]
        ).lstrip('_')

import os

from unittest.async_case import IsolatedAsyncioTestCase

from abc import abstractmethod

from dotenv import find_dotenv, load_dotenv


class BaseTestCase(IsolatedAsyncioTestCase):

    def __init__(self, env_file_path=None, methodName='runTest'):
        super().__init__(
            methodName=methodName
        )

        if env_file_path in [None, ""]:
            env_file_path = \
                find_dotenv(
                    filename=os.getenv('ENV_FILE'),
                    raise_error_if_not_found=True,
                    usecwd=True,
                )

        self.env_file_path = env_file_path

    async def asyncSetUp(self):
        await super().asyncSetUp()

        # Vars
        self.config = None
        self.deps = None
        self.loop = None

        # Load env vars
        load_dotenv(
            dotenv_path=self.env_file_path
        )

        # Read config
        self.read_config()

    async def asyncTearDown(self):
        await super().asyncTearDown()

    @abstractmethod
    def read_config(self):
        """
        Read the config into 'self.config'.
        """
        pass

    # Assert

    def assertEqualIgnoringId(self, id_field, a, b):
        """
        Convenience method for 'assertEqualIgnoringIds'.
        """
        self.assertEqualIgnoringIds(
            id_fields=[id_field],
            a=a,
            b=b,
        )

    def assertEqualIgnoringIds(self, id_fields, a, b):
        """
        This is an assertion method used to assert two entities
        are equal, disregarding some entitiy IDs.
        """
        self.assertEqualIgnoringFields(
            ignore_fields=id_fields,
            a=a,
            b=b,
        )

    def assertEqualIgnoringFields(self, a, b, ignore_fields=None):
        """
        This is an assertion method used to assert two entities
        are equal, disregarding some entitiy IDs.
        """
        ignore_fields = ignore_fields if ignore_fields is not None else []

        if type(a) == list:
            self.assertListsEqualIgnoringFields(a, b, ignore_fields)
        else:
            if not a.equals(b, ignore_fields=ignore_fields):
                self.assertEqual(
                    a.serialize(ignore_fields=ignore_fields),
                    b.serialize(ignore_fields=ignore_fields),
                    "The two building blocks didn't match.",
                )

    def assertListsEqualIgnoringFields(self, a, b, ignore_fields=None):
        """
        The lists equals.
        """
        ignore_fields = ignore_fields if ignore_fields is not None else []

        from ddd.utils.utils import get_for_compare

        a = get_for_compare(a, ignore_fields)
        b = get_for_compare(b, ignore_fields)

        if not a == b:
            self.assertEqual(
                a,
                b,
                "The two lists didn't match.",
            )

    # Helpers

    @classmethod
    def Any(cls, type_=None):
        """
        Returns an object that can be used to compare with other objects.

        Example:
            Any(str) == some_var
            Any(float) == some_var
        """

        class Any(cls):
            def __eq__(self, other):
                if type_ is None:
                    return other is not None
                return type(other) == type_

        return Any()

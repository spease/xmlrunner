# -*- coding: utf-8 -*-

"""
Custom Django test runner that runs the tests using the
XMLTestRunner class.

Usage of this class requires Django to be installed and is intended as a test
suite runner for Django projects. To learn how to configure a custom TestRunner
in a Django project, please read the Django docs website.
"""
from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner
from django.test.utils import setup_test_environment, teardown_test_environment
import xmlrunner


class XMLTestRunner(DjangoTestSuiteRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.
        Labels must be of the form:
         - app.TestClass.test_method
            Run a single specific test method
         - app.TestClass
            Run all the test methods in a given class
         - app
            Search for doctests and unittests in the named application.

        When looking for tests, the test runner will look in the models and
        tests modules for the application.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        Returns the number of tests that failed.
        """
        self.setup_test_environment()
        settings.DEBUG = False

        verbosity = getattr(settings, 'TEST_OUTPUT_VERBOSE', 1)
        if isinstance(verbosity, bool):
            verbosity = (1, 2)[verbosity]
        descriptions = getattr(settings, 'TEST_OUTPUT_DESCRIPTIONS', False)
        output = getattr(settings, 'TEST_OUTPUT_DIR', '.')

        suite = self.build_suite(test_labels, extra_tests)

        old_config = self.setup_databases()

        result = xmlrunner.XMLTestRunner(
            verbosity=verbosity, descriptions=descriptions,
            output=output).run(suite)

        self.teardown_databases(old_config)
        self.teardown_test_environment()

        return len(result.failures) + len(result.errors)

    def setup_test_environment(self, **kwargs):
        setup_test_environment()

    def teardown_test_environment(self, **kwargs):
        teardown_test_environment()

import pytest

import pysatModels

from pysat.tests.test_instruments import generate_instrument_list
from pysat.tests.test_instruments import TestInstrumentQualifier as TestClass

instruments = generate_instrument_list(pysatModels.models.__all__,
                                       package='pysatModels.models')

TestClass.__test__ = False
method_list = [func for func in dir(TestClass) if callable(getattr(TestClass,
                                                                   func))]
# Search tests for iteration via pytestmark, update instrument list
for method in method_list:
    if hasattr(getattr(TestClass, method), 'pytestmark'):
        Nargs =  len(getattr(TestClass, method).pytestmark)
        names = [getattr(TestClass, method).pytestmark[j].name
                 for j in range(0, Nargs)]
        getattr(TestClass, method).pytestmark.clear()
        # Look for custom pytestmarks to identify which instrument set is used
        if "all" in names:
            mark = pytest.mark.parametrize("name", instruments['names'])
            getattr(TestClass, method).pytestmark.append(mark)
        elif "download" in names:
            mark = pytest.mark.parametrize("inst", instruments['download'])
            getattr(TestClass, method).pytestmark.append(mark)
        elif "no_download" in names:
            mark = pytest.mark.parametrize("inst", instruments['no_download'])
            getattr(TestClass, method).pytestmark.append(mark)


class TestModelQualifier(TestClass):

    __test__ = True

    def setup(self):
        """Runs before every method to create a clean testing setup."""
        self.package = 'pysatModels.models'
        pass

    def teardown(self):
        """Runs after every method to clean up previous testing."""
        pass

import unittest

from src.suite_run_provider import SuiteRunProvider, TestProfile


class SuiteRunProviderMock(SuiteRunProvider):
    def run_suite_slice(self, suite: str, host: str) -> str:
        return "<PhoronixTestSuite><Result></Result></PhoronixTestSuite>"

    def setup_new_suite(self, host: str, slice_name: str, suite_slice: str):
        pass


class TestSuiteRunProvider(unittest.TestCase):
    def test_mock(self):
        """Test Description.

        Given a SuiteRunProviderMock
        When a profile with 2 hosts is run
        Then the whole suite is returned
        """
        runner = SuiteRunProviderMock("ubuntu", ".")
        text = """
<PhoronixTestSuite>
  <SuiteInformation>
    <Title>alltests</Title>
    <Version>1.0.0</Version>
    <TestType>System</TestType>
    <Description>Description</Description>
    <Maintainer>Maintainer</Maintainer>
  </SuiteInformation>
  <Execute>
    <Test>local/sqlite-2.2.0</Test>
    <Description>SQLite </Description>
  </Execute>
  <Execute>
    <Test>system/gnuradio-1.0.0</Test>
    <Description>Test: Five Back to Back FIR Filters</Description>
  </Execute>
  <Execute>
    <Test>system/gnuradio-1.0.0</Test>
    <Description>Test: Signal Source (Cosine)</Description>
  </Execute>
</PhoronixTestSuite>
        """
        profile = TestProfile("test", ["test", "test"])
        result = runner.run_suite(text, profile)
        expected = """<PhoronixTestSuite><Result/><Result/></PhoronixTestSuite>"""
        self.assertEqual(expected, result.replace("\n", "").replace(" ", ""))

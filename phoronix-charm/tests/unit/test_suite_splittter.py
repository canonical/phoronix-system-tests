import unittest

from src.suite_splitter import split_suite
from src.suite_splitter import merge_suite

class TestSplitSuite(unittest.TestCase):

    def test_merge(self):
        text = "<TestResult><Result/></TestResult>"
        input = [ text, text ]
        ret = merge_suite(input)
        self.assertEqual("<TestResult><Result /><Result /></TestResult>", ret)

    def test_split(self):
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
        expected = """<PhoronixTestSuite>
    <Execute>
    <Test>local/sqlite-2.2.0</Test>
    <Description>SQLite </Description>
  </Execute>
  <SuiteInformation>
    <Title>alltests</Title>
    <Version>1.0.0</Version>
    <TestType>System</TestType>
    <Description>Description</Description>
    <Maintainer>Maintainer</Maintainer>
  </SuiteInformation>
  </PhoronixTestSuite>
  """.replace(
            "\n", ""
        ).replace(
            " ", ""
        )

        suits = split_suite(text, 4)
        actual = suits[0].replace("\n", "").replace(" ", "")
        self.assertEqual(actual, expected)
        self.assertEqual(len(suits), 3)

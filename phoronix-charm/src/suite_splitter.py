"""Split existing test suite into parts."""

import copy
import xml.etree.ElementTree as ElementTree
from itertools import zip_longest
from typing import Generator


def split_suite(suite_text: str, chunk_size: int) -> Generator[str, None, None]:
    """Split Phoronix test suite into chunks.

    Args:
        suite_text (str): test suite xml
        chunk_size (int): desired chunk size

    Yields:
        Generator[str, None, None]: chunk xml string
    """
    suite = ElementTree.fromstring(suite_text)
    executions = [x for x in suite if x.tag == "Execute"]
    suite_info = [x for x in suite if x.tag == "SuiteInformation"][0]
    chunks = list(zip_longest(*[iter(executions)] * chunk_size, fillvalue=None))
    for chunk in chunks:
        suite_chunk = ElementTree.Element("PhoronixTestSuite")
        suite_chunk.append(copy.deepcopy(suite_info))
        for execution in chunk:
            suite_chunk.append(copy.deepcopy(execution))
        yield ElementTree.tostring(suite_chunk, encoding="utf-8").decode("utf-8")

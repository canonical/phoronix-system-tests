"""Split existing test suite into parts."""

import copy
import xml.etree.ElementTree as ElementTree
from itertools import zip_longest


def split_suite(suite_text: str, chunk_size: int) -> list[str]:
    """Split Phoronix test suite into chunks.

    Args:
        suite_text (str): test suite xml
        chunk_size (int): desired chunk size

    Yields:
        Generator[str, None, None]: chunk xml string
    """
    suite = ElementTree.fromstring(suite_text)
    for x in suite:
        print("tag " + x.tag)
    executions = [x for x in suite if x.tag == "Execute"]
    suite_info = [x for x in suite if x.tag == "SuiteInformation"][0]
    chunks = list(zip_longest(*[iter(executions)] * chunk_size, fillvalue=None))
    ret = []
    for chunk in chunks:
        suite_chunk = ElementTree.Element("PhoronixTestSuite")
        for execution in chunk:
            if execution is None:
                continue
            suite_chunk.append(copy.deepcopy(execution))
        if len(suite_chunk) > 0:
            suite_chunk.append(copy.deepcopy(suite_info))
            ret.append(ElementTree.tostring(suite_chunk, encoding="utf-8").decode("utf-8"))
    return ret

"""Split existing test suite into parts."""

import copy
import xml.etree.ElementTree as ElementTree
from itertools import zip_longest


def merge_suite(results: list[str]) -> str:
    """Merge phoronix test results.

    Args:
        results (list[str]): list of xml strings

    Returns:
        str: merged xml
    """
    if len(results) == 0:
        return str("")
    main = ElementTree.fromstring(results[0])
    for next in results[1:]:
        parsed = ElementTree.fromstring(next)
        result_elements = [x for x in parsed if x.tag == "Result"]
        for el in result_elements:
            main.append(copy.deepcopy(el))
    return ElementTree.tostring(main, encoding="utf-8").decode("utf-8")


def split_suite(suite_text: str, chunks: int) -> list[str]:
    """Split Phoronix test suite into chunks.

    Args:
        suite_text (str): test suite xml
        chunks (int): number of chunks

    Returns:
        list[str, None, None]: chunk xml string
    """
    suite = ElementTree.fromstring(suite_text)
    executions = [x for x in suite if x.tag == "Execute"]
    chunk_size = int(len(executions) / chunks) + 1
    suite_info = [x for x in suite if x.tag == "SuiteInformation"][0]
    execution_chunks = list(zip_longest(*[iter(executions)] * chunk_size, fillvalue=None))
    ret = []
    for chunk in execution_chunks:
        suite_chunk = ElementTree.Element("PhoronixTestSuite")
        for execution in chunk:
            if execution is None:
                continue
            suite_chunk.append(copy.deepcopy(execution))
        if len(suite_chunk) > 0:
            suite_chunk.append(copy.deepcopy(suite_info))
            ret.append(ElementTree.tostring(suite_chunk, encoding="utf-8").decode("utf-8"))
    return ret

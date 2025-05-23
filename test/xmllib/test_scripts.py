import filecmp
import os
import shutil
import warnings
from pathlib import Path

import pytest
from dsp_tools.error.xmllib_warnings import XmllibInputInfo

from src.xmllib.main import main

ORIG_XML_FILE = Path("daschland_data.xml")
ENV_VARS = ["XMLLIB_SORT_RESOURCES", "XMLLIB_SORT_PROPERTIES", "XMLLIB_AUTHORSHIP_ID_WITH_INTEGERS"]
LIST_SEP = "\n - "


@pytest.fixture
def stashed_original_xml(tmp_path: Path) -> Path:
    dst = tmp_path / ORIG_XML_FILE.name
    shutil.copy(ORIG_XML_FILE, dst)
    return dst


@pytest.fixture
def regenerate_xml_file(stashed_original_xml: Path) -> None:  # noqa: ARG001 (unused argument)
    for env_var in ENV_VARS:
        os.environ[env_var] = "true"
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=XmllibInputInfo)
        main()


@pytest.mark.usefixtures("regenerate_xml_file")
def test_xml_has_not_changed(stashed_original_xml: Path) -> None:
    fail_msg = (
        "The XML file freshly generated with xmllib is not identical to the original. "
        "To fix this, run the xmllib scripts and commit the resulting XML file. "
        "Make sure that your .env file contains the following environment variables:\n"
        + "\n".join([f"{x}=true" for x in ENV_VARS])
    )
    if not filecmp.cmp(ORIG_XML_FILE, stashed_original_xml, shallow=False):
        pytest.fail(fail_msg)
    print(f"Just to test: The message would be: {fail_msg}")

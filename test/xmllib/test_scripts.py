import os

import pytest

from src.xmllib.main import main


@pytest.mark.filterwarnings("ignore::dsp_tools.error.xmllib_warnings.XmllibInputInfo")
def test_scripts() -> None:
    os.environ["XMLLIB_SORT_RESOURCES"] = "true"
    os.environ["XMLLIB_SORT_PROPERTIES"] = "true"
    os.environ["XMLLIB_AUTHORSHIP_ID_WITH_INTEGERS"] = "true"
    main()

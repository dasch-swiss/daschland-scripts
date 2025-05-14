import pytest

from src.xmllib.main import main


@pytest.mark.filterwarnings("ignore::dsp_tools.error.xmllib_warnings.XmllibInputInfo")
def test_scripts() -> None:
    main()

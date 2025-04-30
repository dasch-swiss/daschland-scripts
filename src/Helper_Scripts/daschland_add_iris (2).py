import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from lxml import etree


def main() -> None:
    root = _read_xml_file_to_root_remove_comments(Path("daschland_data.xml"))
    id_dict = _read_json_to_dic(Path("daschland_id2iri.json"))
    replaced = _add_iris(root, id_dict)
    _write_file(replaced)


def _add_iris(original_root: etree._Element, id_dict: dict[str, str]) -> etree._Element:
    root = deepcopy(original_root)
    for child in root.iterchildren(tag="{https://dasch.swiss/schema}resource"):
        if child.attrib.get("label"):
            child.attrib["iri"] = id_dict[child.attrib["id"]]
    return root


def _write_file(root: etree._Element) -> None:
    xml_string = etree.tostring(root, encoding="unicode", pretty_print=True)
    with open("daschland_data_with_iri.xml", "w", encoding="utf-8") as f:
        f.write(xml_string)


def _read_json_to_dic(inpath: Path) -> dict[str, Any]:
    with open(inpath) as json_file:
        return json.load(json_file)  # type: ignore[no-any-return]


def _read_xml_file_to_root_remove_comments(in_filepath_name: Path) -> etree._Element:
    parser = etree.XMLParser(remove_comments=True, remove_blank_text=True)
    read_xml = etree.parse(in_filepath_name, parser=parser)
    return read_xml.getroot()


main()

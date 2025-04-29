from dsp_tools import excel2xml
from lxml import etree
from lxml.builder import E

xml_namespace_map = {
    None: "https://dasch.swiss/schema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


def make_root(default_ontology: str = "daschland", shortcode: str = "0854") -> etree._Element:
    # create the root element dsp-tools
    root = excel2xml.make_root(shortcode=shortcode, default_ontology=default_ontology)

    # append the permissions
    root = _append_permissions(root)

    return root


def _append_permissions(root_element: etree._Element) -> etree._Element:
    """
    After having created a root element, call this method to append the four permissions "res-default",
    "res-restricted", "prop-default", and "prop-restricted" to it. These four permissions are a good basis to
    start with, but remember that they can be adapted, and that other permissions can be defined instead of these.

    Args:
        root_element: The XML root element <knora> created by make_root()

    Returns:
        The root element with the four permission blocks appended

    Examples:
        >>> root = excel2xml.make_root(shortcode=shortcode, default_ontology=default_ontology)
        >>> root = excel2xml.append_permissions(root)

    See https://docs.dasch.swiss/latest/DSP-TOOLS/file-formats/xml-data-file/#describing-permissions-with-permissions-elements
    """

    PERMISSIONS = E.permissions
    ALLOW = E.allow
    # lxml.builder.E is a more sophisticated element factory than etree.Element.
    # E.tag is equivalent to E("tag") and results in <tag>

    res_default = etree.Element("{%s}permissions" % xml_namespace_map[None], id="res-default")
    res_default.append(ALLOW("V", group="UnknownUser"))
    res_default.append(ALLOW("V", group="KnownUser"))
    res_default.append(ALLOW("D", group="ProjectMember"))
    res_default.append(ALLOW("CR", group="ProjectAdmin"))
    root_element.append(res_default)

    res_restricted = etree.Element("{%s}permissions" % xml_namespace_map[None], id="res-restricted")
    res_restricted.append(ALLOW("D", group="ProjectMember"))
    res_restricted.append(ALLOW("CR", group="ProjectAdmin"))
    root_element.append(res_restricted)

    prop_default = PERMISSIONS(id="prop-default")
    prop_default.append(ALLOW("V", group="UnknownUser"))
    prop_default.append(ALLOW("V", group="KnownUser"))
    prop_default.append(ALLOW("D", group="ProjectMember"))
    prop_default.append(ALLOW("CR", group="ProjectAdmin"))
    root_element.append(prop_default)

    prop_restricted = PERMISSIONS(id="prop-restricted")
    prop_restricted.append(ALLOW("M", group="ProjectMember"))
    prop_restricted.append(ALLOW("CR", group="ProjectAdmin"))

    root_element.append(prop_restricted)

    bitstream_prop_restricted = PERMISSIONS(id="bitstream-prop-restricted")
    bitstream_prop_restricted.append(ALLOW("M", group="ProjectMember"))
    bitstream_prop_restricted.append(ALLOW("CR", group="ProjectAdmin"))
    bitstream_prop_restricted.append(ALLOW("RV", group="UnknownUser"))
    bitstream_prop_restricted.append(ALLOW("RV", group="KnownUser"))
    root_element.append(bitstream_prop_restricted)

    return root_element

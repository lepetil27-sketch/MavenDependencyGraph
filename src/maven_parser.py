import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass
class MavenDependency:
    group_id: str
    artifact_id: str
    version: str

    def __str__(self) -> str:
        return (f"{self.group_id}:"
                f"{self.artifact_id}:"
                f"{self.version}")


def parse_pom(pom_content: str
              ) -> list[MavenDependency]:
    try:
        root = ET.fromstring(pom_content)
    except ET.ParseError as exc:
        print(f"Ошибка парсинга XML: {exc}")
        return []

    ns = {
        "m": "http://maven.apache.org/POM/4.0.0"
    }

    properties = _extract_properties(
        root, ns
    )

    dependencies = []
    for dep in root.findall(
        ".//m:dependency", ns
    ):
        gid = _get_text(dep, "m:groupId", ns)
        aid = _get_text(dep, "m:artifactId", ns)
        ver = _get_text(dep, "m:version", ns)

        if gid and aid:
            resolved = _resolve_property(
                ver or "unknown", properties
            )
            dependencies.append(
                MavenDependency(
                    gid, aid, resolved
                )
            )

    return dependencies


def _extract_properties(
    root: ET.Element, ns: dict
) -> dict:
    props = {}
    props_elem = root.find("m:properties", ns)
    if props_elem is None:
        return props

    for prop in props_elem:
        tag = prop.tag
        if "}" in tag:
            tag = tag.split("}", 1)[1]
        if prop.text:
            props[tag] = prop.text.strip()

    return props


def _resolve_property(
    value: str, properties: dict
) -> str:
    def replacer(match):
        return properties.get(
            match.group(1), match.group(0)
        )

    pattern = r'\$\{([^}]+)\}'
    return re.sub(pattern, replacer, value)


def _get_text(element: ET.Element,
              tag: str,
              ns: dict) -> str | None:
    child = element.find(tag, ns)
    if child is not None and child.text:
        return child.text.strip()
    return None
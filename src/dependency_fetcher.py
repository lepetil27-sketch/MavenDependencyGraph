import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

from src.maven_parser import (
    parse_pom,
    MavenDependency,
)


def fetch_direct_dependencies(
    package: str,
    repo_url: str,
) -> list[MavenDependency]:
    group_id, artifact_id = package.split(
        ":", 1
    )
    group_path = group_id.replace(".", "/")

    metadata_url = (
        f"{repo_url}/{group_path}/"
        f"{artifact_id}/"
        f"maven-metadata.xml"
    )

    metadata_xml = _fetch_url(metadata_url)
    if not metadata_xml:
        return []

    version = _extract_latest_version(
        metadata_xml
    )
    if not version:
        print(f"Не удалось определить "
              f"версию для {package}")
        return []

    pom_url = (
        f"{repo_url}/{group_path}/"
        f"{artifact_id}/{version}/"
        f"{artifact_id}-{version}.pom"
    )

    pom_xml = _fetch_url(pom_url)
    if not pom_xml:
        return []

    return parse_pom(pom_xml)


def _fetch_url(url: str) -> str | None:
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.URLError as exc:
        print(f"Ошибка сети при запросе "
              f"{url}: {exc}")
        return None


def _extract_latest_version(
    metadata_xml: str
) -> str | None:
    try:
        root = ET.fromstring(metadata_xml)
        versioning = root.find("versioning")
        if versioning is not None:
            latest = versioning.find("latest")
            if latest is not None and latest.text:
                return latest.text.strip()
    except ET.ParseError:
        pass

    return None
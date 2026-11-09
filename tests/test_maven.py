import unittest

from src.maven_parser import (
    parse_pom,
    MavenDependency,
)


SAMPLE_POM = """<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <properties>
        <spring.version>5.3.20</spring.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.example</groupId>
            <artifactId>lib-a</artifactId>
            <version>1.0</version>
        </dependency>
        <dependency>
            <groupId>org.example</groupId>
            <artifactId>lib-b</artifactId>
            <version>${spring.version}</version>
        </dependency>
    </dependencies>
</project>"""


class TestParsePom(unittest.TestCase):
    """Тесты парсинга POM."""

    def test_parse_dependencies(self):
        """Проверка извлечения зависимостей."""
        deps = parse_pom(SAMPLE_POM)
        self.assertEqual(len(deps), 2)
        self.assertEqual(
            deps[0].artifact_id, "lib-a"
        )

    def test_resolve_properties(self):
        """Проверка резолвинга properties."""
        deps = parse_pom(SAMPLE_POM)
        self.assertEqual(
            deps[1].version, "5.3.20"
        )

    def test_parse_empty_pom(self):
        """Проверка пустого POM."""
        empty = (
            '<?xml version="1.0"?>'
            '<project xmlns="http://maven.'
            'apache.org/POM/4.0.0">'
            '</project>'
        )
        deps = parse_pom(empty)
        self.assertEqual(len(deps), 0)

    def test_parse_invalid_xml(self):
        """Проверка невалидного XML."""
        deps = parse_pom("not xml")
        self.assertEqual(len(deps), 0)


if __name__ == "__main__":
    unittest.main()
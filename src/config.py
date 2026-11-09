import argparse
import os
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Визуализатор графа "
                    "зависимостей Maven"
    )

    parser.add_argument(
        "--package",
        type=str,
        required=True,
        help="Имя пакета в формате "
             "groupId:artifactId"
    )

    parser.add_argument(
        "--repo-url",
        type=str,
        default="https://repo1.maven.org/maven2",
        help="URL Maven-репозитория"
    )

    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Режим работы с тестовым "
             "репозиторием"
    )

    parser.add_argument(
        "--test-file",
        type=str,
        default=None,
        help="Путь к файлу тестового "
             "репозитория"
    )

    parser.add_argument(
        "--output-file",
        type=str,
        default="graph.png",
        help="Имя файла с изображением "
             "графа"
    )

    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="Вывод в формате ASCII-дерева"
    )

    parser.add_argument(
        "--filter",
        type=str,
        default=None,
        help="Подстрока для фильтрации "
             "пакетов"
    )

    return parser.parse_args()


def validate_config(args: argparse.Namespace
                    ) -> None:
    if ":" not in args.package:
        raise ValueError(
            "Параметр --package должен быть "
            "в формате groupId:artifactId"
        )

    if args.test_mode and not args.test_file:
        raise ValueError(
            "В режиме --test-mode нужно "
            "указать --test-file"
        )

    if args.test_file and not os.path.exists(
        args.test_file
    ):
        raise FileNotFoundError(
            f"Тестовый файл не найден: "
            f"{args.test_file}"
        )

    if args.output_file and not args.output_file.endswith(
        (".png", ".svg")
    ):
        raise ValueError(
            "Файл изображения должен иметь "
            "расширение .png или .svg"
        )


def print_config(args: argparse.Namespace
                 ) -> None:
    print("=== Конфигурация ===")
    print(f"package: {args.package}")
    print(f"repo_url: {args.repo_url}")
    print(f"test_mode: {args.test_mode}")
    print(f"test_file: "
          f"{args.test_file or '(не указан)'}")
    print(f"output_file: {args.output_file}")
    print(f"ascii_tree: {args.ascii_tree}")
    print(f"filter: "
          f"{args.filter or '(не указана)'}")
    print("======================")
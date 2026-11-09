import sys

from src.config import (
    parse_args,
    validate_config,
    print_config,
)
from src.dependency_fetcher import (
    fetch_direct_dependencies,
)


def main() -> None:
    args = parse_args()

    try:
        validate_config(args)
    except (ValueError, FileNotFoundError
            ) as exc:
        print(f"Ошибка конфигурации: {exc}")
        sys.exit(1)

    print_config(args)

    print("\n[Этап 2] Сбор прямых "
          "зависимостей...")

    deps = fetch_direct_dependencies(
        package=args.package,
        repo_url=args.repo_url,
    )

    if not deps:
        print("Прямые зависимости не "
              "найдены.")
        return

    print(f"\nНайдено прямых зависимостей: "
          f"{len(deps)}\n")

    if args.ascii_tree:
        print(f"{args.package}")
        for i, dep in enumerate(deps):
            is_last = (i == len(deps) - 1)
            prefix = "└── " if is_last else "├── "
            print(f"{prefix}{dep}")
    else:
        print("Прямые зависимости:")
        for dep in deps:
            print(f"  - {dep}")


if __name__ == "__main__":
    main()
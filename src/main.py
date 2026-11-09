import sys

from src.config import (
    parse_args,
    validate_config,
    print_config,
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


if __name__ == "__main__":
    main()
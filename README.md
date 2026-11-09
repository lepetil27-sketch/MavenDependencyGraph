# Maven Dependency Graph

Инструмент визуализации графа зависимостей для пакетов Maven (Java).

## Требования

- Python 3.10+

## Запуск

### Интерактивный режим

```bash
python -m src.main --package org.springframework:spring-core
```

### С параметрами
```bash
python -m src.main \
  --package org.springframework:spring-core \
  --repo-url https://repo1.maven.org/maven2 \
  --ascii-tree \
  --output-file graph.png
```

### В тестовом режиме
```bash
python -m src.main \
  --package com.example:my-app \
  --test-mode \
  --test-file test_data/test_pom.xml \
  --ascii-tree
```

### С фильтрацией
```bash
python -m src.main \
  --package org.springframework:spring-core \
  --filter test
```

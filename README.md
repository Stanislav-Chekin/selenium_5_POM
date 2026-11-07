# 🚀 Selenium Python Automation Framework

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-9.2+-green.svg)](https://docs.pytest.org/)
[![Selenium](https://img.shields.io/badge/selenium-4.x+-orange.svg)](https://selenium-python.readthedocs.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Данный репозиторий содержит фреймворк для автоматизированного тестирования веб-приложений, разработанный в рамках курса **AQA (Python + Selenium)** от **QA.GURU**. Проект демонстрирует владение современными практиками и паттернами проектирования, применяемыми в реальной коммерческой разработке.

## 🎯 Цели проекта

*   Освоение и практическое применение паттерна **Page Object Model (POM)**.
*   Изучение библиотеки **Selenium Page Factory** для более чистого и поддерживаемого кода.
*   Внедрение принципов **Fluent Interface** для построения цепочек вызовов.
*   Написание надежных и стабильных тестов с использованием явных ожиданий (`WebDriverWait`).
*   Практика параметризации тестов и обработки негативных сценариев (включая маркировку `xfail`).

## 🛠️ Технологический стек

*   **Язык программирования:** Python 3.14+
*   **Фреймворк для тестов:** Pytest
*   **Библиотека для автоматизации браузера:** Selenium WebDriver
*   **Паттерны проектирования:** Page Object Model (POM), Page Factory, Fluent Interface

## 📂 Структура проекта

```text
selenium_5_POM/
├── TextBoxPageObject/                # Реализация классического POM
│   ├── conftest.py                   # Фикстуры Pytest (инициализация драйвера)
│   ├── requirements.txt              # Зависимости для этого модуля
│   ├── test_text_box.py              # Тестовые сценарии для формы Text Box
│   └── text_box_page.py              # Page Object класс для страницы
├── TextBoxPageObjectWithPageFactory/ # Реализация POM с использованием библиотеки Page Factory
│   ├── conftest.py
│   ├── requirements.txt
│   ├── test_text_box.py
│   └── text_box_page_pf.py
├── page_factory_extended_example/    # Расширенный пример с Page Factory
│   ├── requirements.txt
│   └── test_student_registration_form_with_pf.py
├── add_remove_elements.py            # Примеры работы с динамическими элементами
├── drag_and_drop.py                  # Примеры Drag & Drop
├── relative_locator.py               # Примеры использования Relative Locators
├── Fluent Interface Description.py   # Пример реализации Fluent Interface
└── README.md                         # Этот файл
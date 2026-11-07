import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Инициализация браузера
driver = webdriver.Chrome()

try:
    # Открытие тестового сайта
    driver.get("https://the-internet.herokuapp.com/drag_and_drop")
    time.sleep(3)

    # Находим элементы для перемещения
    source_element = driver.find_element(By.ID, "column-a")
    target_element = driver.find_element(By.ID, "column-b")

    # --- ИЗМЕНЕНИЕ (Микро TODO) ---
    # Вместо стандартного (и часто нерабочего) actions.drag_and_drop,
    # используем JavaScript для надежного перетаскивания.
    # Это лучший workaround для сайтов с HTML5 Drag and Drop.
    driver.execute_script("""
        function createEvent(typeOfEvent) {
            var event = document.createEvent("CustomEvent");
            event.initCustomEvent(typeOfEvent, true, true, null);
            event.dataTransfer = {
                data: {},
                setData: function (key, value) { this.data[key] = value; },
                getData: function (key) { return this.data[key]; }
            };
            return event;
        }
        function dispatchEvent(element, event, transferData) {
            if (transferData !== undefined) {
                event.dataTransfer = transferData;
            }
            if (element.dispatchEvent) {
                element.dispatchEvent(event);
            } else if (element.fireEvent) {
                element.fireEvent("on" + event.type, event);
            }
        }
        function simulateHTML5DragAndDrop(element, destination) {
            var dragStartEvent = createEvent('dragstart');
            dispatchEvent(element, dragStartEvent);
            var dropEvent = createEvent('drop');
            dispatchEvent(destination, dropEvent, dragStartEvent.dataTransfer);
            var dragEndEvent = createEvent('dragend');
            dispatchEvent(element, dragEndEvent, dropEvent.dataTransfer);
        }
        var source = arguments[0];
        var destination = arguments[1];
        simulateHTML5DragAndDrop(source, destination);
    """, source_element, target_element)
    # -------------------------------

    # Задержка для наглядности
    time.sleep(3)

    # --- ПРОВЕРКА (Assert) ---
    # Проверяем, что заголовок первой колонки изменился с A на B
    header_a = driver.find_element(By.CSS_SELECTOR, "#column-a header").text
    assert header_a == "B", f"Drag and Drop не сработал! В колонке A до сих пор: {header_a}"
    print("✅ Drag and Drop успешно выполнен и проверен!")

finally:
    # Закрытие браузера
    driver.quit()

# Запустить python drag_and_drop.py

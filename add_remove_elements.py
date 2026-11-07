import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1. Инициализация драйвера (открывается браузер Chrome)
driver = webdriver.Chrome()

try:
    # 2. Переход на целевую страницу
    url = "https://the-internet.herokuapp.com/add_remove_elements/"
    driver.get(url)
    print("Страница успешно открыта.")
    time.sleep(2)  # Пауза для визуального контроля

    # 3. Поиск главной кнопки "Add Element"
    # Используем поиск по тексту кнопки через XPath
    add_button = driver.find_element(By.XPATH, "//button[text()='Add Element']")

    # 4. Демонстрация добавления элементов
    print("Добавляем 5 элементов...")
    for i in range(5):  # <-- ИЗМЕНЕНО: теперь добавляем 5
        add_button.click()
        time.sleep(0.5)

    # 5. Подсчет и проверка созданных элементов
    delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")

    # <-- ИЗМЕНЕНО: вместо print делаем проверку
    assert len(delete_buttons) == 5, f"Ожидали 5 кнопок, а нашли {len(delete_buttons)}"
    print(f"✅ Проверка пройдена: создано ровно 5 кнопок.")

    # 6. Демонстрация удаления элементов
    print("Удаляем созданные элементы по очереди...")
    for button in delete_buttons:
        button.click()
        time.sleep(0.5)

    # Повторная проверка количества элементов после удаления
    remaining_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")

    # <-- ИЗМЕНЕНО: проверяем, что удалили ВСЕ
    assert len(remaining_buttons) == 0, f"Ожидали 0 кнопок, а осталось {len(remaining_buttons)}"
    print(f"✅ Проверка пройдена: все кнопки удалены (0 штук).")

finally:
    # 7. Закрытие браузера и завершение сессии (ВОТ ЭТОГО НЕ ХВАТАЛО!)
    driver.quit()
    print("Браузер закрыт. Тест завершен.")

# Запустить python add_remove_elements.py

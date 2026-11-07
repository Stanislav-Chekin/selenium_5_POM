import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

driver = webdriver.Chrome()
driver.maximize_window()

# =======================================================
# ЧАСТЬ 1: Тестируем на странице text-box.html
# =======================================================
driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
time.sleep(2)

# 1. Ищем поле ввода, которое находится ПОД текстом "Full Name"
full_name_label = driver.find_element(By.XPATH, "//label[text()='Full Name']")
# Ищем input, который ниже (below) этого лейбла
full_name_input = driver.find_element(locate_with(By.TAG_NAME, "input").below(full_name_label))
full_name_input.send_keys("Ivan Ivanov")

# 2. Ищем поле ввода, которое находится НАД кнопкой Submit
submit_btn = driver.find_element(By.ID, "submit")
# Ищем input, который выше (above) кнопки
input_above_submit = driver.find_element(locate_with(By.TAG_NAME, "input").above(submit_btn))
input_above_submit.send_keys("ivan@example.com") # Вводим email

# 3. Ищем поле ввода, которое находится РЯДОМ с текстом "Current Address"
current_address_label = driver.find_element(By.XPATH, "//label[text()='Current Address']")
# Ищем textarea, которая рядом (near) с лейблом
address_textarea = driver.find_element(locate_with(By.TAG_NAME, "textarea").near(current_address_label))
address_textarea.send_keys("г. Минск, ул. Академическая")

time.sleep(2)

# =======================================================
# ЧАСТЬ 2: Тестируем радиокнопки на automation-practice-form.html
# =======================================================
driver.get("https://qa-guru.github.io/one-page-form/automation-practice-form.html")
time.sleep(2)

# 4. Ищем радиокнопку СЛЕВА от кнопки "Female" (gender-radio-2)
second_radio = driver.find_element(By.ID, "gender-radio-2")
# Ищем input, который слева (toLeftOf) от Female
first_radio = driver.find_element(locate_with(By.TAG_NAME, "input").to_left_of(second_radio))
first_radio.click() # Кликаем на Male

# 5. Ищем радиокнопку СПРАВА от кнопки "Male" (gender-radio-1)
first_radio = driver.find_element(By.ID, "gender-radio-1")
# Ищем input, который справа (toRightOf) от Male
second_radio = driver.find_element(locate_with(By.TAG_NAME, "input").to_right_of(first_radio))
second_radio.click() # Кликаем на Female

time.sleep(3)
driver.quit()
print("✅ Все относительные локаторы успешно отработали!")

# Запустить python relative_locator.py

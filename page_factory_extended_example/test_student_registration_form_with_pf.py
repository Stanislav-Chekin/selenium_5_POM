import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==============================================================================
# 1. КОНФИГУРАЦИЯ ТЕСТОВОЙ СРЕДЫ (pytest fixture)
# ==============================================================================
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# ==============================================================================
# 2. БАЗОВЫЙ КЛАСС СТРАНИЦЫ
# ==============================================================================
class BasePage(PageFactory):
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def open_url(self, url: str):
        self.driver.get(url)


# ==============================================================================
# 3. КЛАСС СТРАНИЦЫ ФОРМЫ
# ==============================================================================
class AutomationPracticeFormPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    locators = {
        'first_name': ('ID', 'firstName'),
        'last_name': ('ID', 'lastName'),
        'user_email': ('ID', 'userEmail'),
        'banner_button': ('XPATH', "//div[@id='fixedban']//button[@aria-label='Close']"),
        'gender_male': ('XPATH', "//label[@for='gender-radio-1']"),
        'gender_female': ('XPATH', "//label[@for='gender-radio-2']"),
        'gender_other': ('XPATH', "//label[@for='gender-radio-3']"),
        'user_number': ('ID', 'userNumber'),
        'date_of_birth_input': ('ID', 'dateOfBirthInput'),
        'calendar_month_select': ('CLASS_NAME', 'react-datepicker__month-select'),
        'calendar_year_select': ('CLASS_NAME', 'react-datepicker__year-select'),
        'subjects_input': ('ID', 'subjectsInput'),
        'hobby_sports': ('XPATH', "//label[@for='hobbies-checkbox-1']"),
        'hobby_reading': ('XPATH', "//label[@for='hobbies-checkbox-2']"),
        'hobby_music': ('XPATH', "//label[@for='hobbies-checkbox-3']"),
        'upload_picture_btn': ('ID', 'uploadPicture'),
        'current_address': ('ID', 'currentAddress'),
        'submit_button': ('ID', 'submit'),
        'state_dropdown': ('ID', 'state'),
        'city_dropdown': ('ID', 'city'),
        'modal_title': ('ID', 'example-modal-sizes-title-lg'),
        'modal_table_rows': ('XPATH', "//div[@class='modal-body']//tbody/tr")
    }

    def _close_commercial_banner(self):
        try:
            # Ждем до 3 секунд появления кнопки закрытия баннера
            banner_close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='fixedban']//button[@aria-label='Close']"))
            )
            banner_close_btn.click()
        except Exception:
            pass  # Если баннера нет или он не кликается, просто идем дальше

    # --------------------------------------------------------------------------
    # Бизнес-методы (Действия на странице)
    # --------------------------------------------------------------------------
    def fill_personal_info(self, first_name: str, last_name: str, email: str, gender: str, mobile: str):
        self._close_commercial_banner()

        self.first_name.set_text(first_name)
        self.last_name.set_text(last_name)
        self.user_email.set_text(email)

        # УЛУЧШЕНИЕ: Убрали if/else, используем словарь для выбора пола
        gender_map = {
            'male': self.gender_male,
            'female': self.gender_female,
            'other': self.gender_other
        }
        # Если ключ не найден, по умолчанию кликаем на 'other'
        gender_map.get(gender.lower(), self.gender_other).click_button()

        self.user_number.set_text(mobile)

    def select_date_of_birth(self, year: str, month: str, day: str):
        self.date_of_birth_input.click_button()

        # УЛУЧШЕНИЕ: Вместо time.sleep(1) ждем, пока календарь реально откроется
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'react-datepicker__month-select'))
        )

        self.calendar_year_select.select_element_by_value(year)
        self.calendar_month_select.select_element_by_text(month)

        day_padded = f"{int(day):03d}"
        day_locator = (By.CSS_SELECTOR,
                       f".react-datepicker__day--{day_padded}:not(.react-datepicker__day--outside-month)")

        day_element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(day_locator)
        )
        day_element.click()

    def enter_subjects(self, subjects: list):
        for subject in subjects:
            self.subjects_input.set_text(subject)

            # УЛУЧШЕНИЕ: Вместо time.sleep(0.5) ждем появления выпадающего меню подсказок
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'subjects-auto-complete__menu'))
            )
            self.subjects_input.send_keys(Keys.ENTER)

    def select_hobbies(self, hobbies: list):
        hobbies_map = {
            'sports': self.hobby_sports,
            'reading': self.hobby_reading,
            'music': self.hobby_music
        }
        for hobby in hobbies:
            hobby_lower = hobby.lower()
            if hobby_lower in hobbies_map:
                hobbies_map[hobby_lower].click_button()

    def upload_file(self, file_path: str):
        self.upload_picture_btn.send_keys(file_path)

    def fill_address_and_location(self, address: str, state: str, city: str):
        self.current_address.set_text(address)

        # ---------- STATE ----------
        state_trigger = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'state'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", state_trigger)
        state_trigger.click()

        # УЛУЧШЕНИЕ: Ждем, пока выпадающий список штатов появится в DOM
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'state-city-dropdown'))
        )

        state_option_xpath = f"//div[contains(@class, 'state-city-option') and text()='{state}']"
        state_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, state_option_xpath))
        )
        self.driver.execute_script("arguments[0].click();", state_option)

        # ---------- CITY ----------
        city_trigger = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'city'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", city_trigger)
        city_trigger.click()

        city_option_xpath = f"//div[contains(@class, 'state-city-option') and text()='{city}']"
        city_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, city_option_xpath))
        )
        self.driver.execute_script("arguments[0].click();", city_option)

    def submit_form(self):
        submit_btn = self.driver.find_element(By.ID, "submit")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        self.driver.execute_script("arguments[0].click();", submit_btn)

    def get_modal_results(self) -> dict:
        # УЛУЧШЕНИЕ: Убрали time.sleep(1.5) после сабмита.
        # Просто ждем появления заголовка модального окна.
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'example-modal-sizes-title-lg'))
        )

        result_data = {}
        rows = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table//tbody/tr"))
        )

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()
                result_data[label] = value

        # Закрываем модальное окно
        try:
            close_btn = self.driver.find_element(
                By.XPATH, "//button[contains(text(), 'Close') or @aria-label='Close']"
            )
            self.driver.execute_script("arguments[0].click();", close_btn)
        except Exception as e:
            print(f"Кнопка Close не найдена или не кликнулась: {e}")

        return result_data

    # ==========================================================================
    # Фасад (высокоуровневый метод)
    # ==========================================================================
    def fill_form(self, first_name, last_name, email, gender, mobile, year, month, day, subjects, hobbies, file_path,
                  address, state, city):
        self.fill_personal_info(first_name, last_name, email, gender, mobile)
        self.select_date_of_birth(year, month, day)
        self.enter_subjects(subjects)
        self.select_hobbies(hobbies)
        self.upload_file(file_path)
        self.fill_address_and_location(address, state, city)
        self.submit_form()


# ==============================================================================
# 4. ПАРАМЕТРИЗОВАННЫЙ ТЕСТОВЫЙ СЦЕНАРИЙ
# ==============================================================================
@pytest.mark.parametrize(
    "first_name, last_name, email, gender, mobile, year, month, day, subjects, hobbies, address, state, city, expected_date",
    [
        ("Ivan", "Ivanov", "ivan@edu.ru", "Male", "1234567890", "2000", "January", "15", ["Maths"], ["Sports"], "Tomsk",
         "NCR", "Delhi", "15 Jan 2000"),
        ("Anna", "Petrova", "anna@mail.com", "Female", "9876543210", "1995", "May", "10", ["Physics"],
         ["Reading", "Music"], "Moscow", "Uttar Pradesh", "Agra", "10 May 1995")
    ])
def test_student_registration_form_max_capabilities(driver, first_name, last_name, email, gender, mobile, year, month,
                                                    day, subjects, hobbies, address, state, city, expected_date):
    test_filename = "demo_upload.txt"
    with open(test_filename, "w") as f:
        f.write("QA Guru PageFactory Demo")
    abs_file_path = os.path.abspath(test_filename)

    try:
        page = AutomationPracticeFormPage(driver)
        page.open_url("https://qa-guru.github.io/one-page-form/automation-practice-form.html")

        page.fill_form(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            mobile=mobile,
            year=year,
            month=month,
            day=day,
            subjects=subjects,
            hobbies=hobbies,
            file_path=abs_file_path,
            address=address,
            state=state,
            city=city
        )

        actual_results = page.get_modal_results()

        assert actual_results.get(
            "Student Name") == f"{first_name} {last_name}", f"Не совпало имя: {actual_results.get('Student Name')}"
        assert actual_results.get("Student Email") == email
        assert actual_results.get("Gender") == gender
        assert actual_results.get("Mobile") == mobile
        assert actual_results.get("Date of Birth") == expected_date
        assert actual_results.get("Address") == address
        assert actual_results.get("State and City") == f"{state} {city}"
        assert actual_results.get("Picture") == test_filename

    finally:
        if os.path.exists(abs_file_path):
            os.remove(abs_file_path)

# Запустить python -m pytest page_factory_extended_example/test_student_registration_form_with_pf.py -v

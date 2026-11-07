import pytest
from text_box_page import TextBoxPage


# --- 1. Позитивные сценарии (Валидные данные) ---
@pytest.mark.parametrize("name, email, cur_addr, perm_addr", [
    ("John Doe", "john@example.com", "123 Elm St", "456 Oak St"),
    ("Иван Иванов", "ivan@mail.ru", "ул. Ленина, д. 1", "ул. Пушкина, д. 2"),
    ("A", "a@b.cc", "B", "C"),
    ("Name-With Dash", "dash@email.co.uk", "Addr 1/2", "Addr 3 & 4"),
    ("   John   ", "spaces@test.com", "  Street 1  ", "  Street 2  "),
])
def test_positive_form_submission(driver, name, email, cur_addr, perm_addr):
    page = TextBoxPage(driver)
    output = page.open().fill_form(name, email, cur_addr, perm_addr).submit().get_output_data()

    assert output is not None, "Блок с результатами не отобразился"
    assert output["name"] == name.strip()
    assert output["email"] == email.strip()
    assert output["cur_addr"] == cur_addr.strip()
    assert output["perm_addr"] == perm_addr.strip()


# --- 2. Частичное заполнение обязательных/необязательных полей ---
@pytest.mark.parametrize("name, email, cur_addr, perm_addr", [
    ("Only Name", "", "", ""),
    ("", "only@email.com", "", ""),
    ("", "", "Only Current Address", ""),
    ("", "", "", "Only Permanent Address"),
    ("Name & Email", "name_email@test.com", "", ""),
])
def test_partial_form_submission(driver, name, email, cur_addr, perm_addr):
    page = TextBoxPage(driver)
    output = page.open().fill_form(name, email, cur_addr, perm_addr).submit().get_output_data()

    assert output is not None, "Форма должна отправляться при частичном заполнении"
    if name: assert output["name"] == name
    if email: assert output["email"] == email
    if cur_addr: assert output["cur_addr"] == cur_addr
    if perm_addr: assert output["perm_addr"] == perm_addr


# --- 3. Негативные сценарии (Невалидный Email) ---
@pytest.mark.parametrize("invalid_email", [
    "plainaddress",
    "@no-local-part.com",
    pytest.param("john.doe@com", marks=pytest.mark.xfail(reason="Браузер считает этот email валидным")),
    pytest.param("john@missing-dot", marks=pytest.mark.xfail(reason="Браузер считает этот email валидным")),
    "john@@example.com",
    "john@example..com",
])
def test_invalid_email_validation(driver, invalid_email):
    page = TextBoxPage(driver)
    page.open().fill_form(name="Test", email=invalid_email).submit()

    output = page.get_output_data()
    assert output is None or page.is_email_error_present(), f"Email '{invalid_email}' не должен быть принят системой"


# --- 4. Граничные значения и нагрузка на длину полей (Длинные строки) ---
@pytest.mark.parametrize("field_type, long_string", [
    ("name", "A" * 1000),
    ("email", f"{'b' * 64}@example.com"),
    ("cur_addr", "Current " * 200),
    ("perm_addr", "Permanent " * 200)
])
def test_long_input_fields(driver, field_type, long_string):
    page = TextBoxPage(driver)
    kwargs = {field_type: long_string}
    page.open().fill_form(**kwargs).submit()

    output = page.get_output_data()
    assert output is not None, f"Форма не справилась с длинной строкой в поле {field_type}"


# --- 5. Безопасность и спец-инъекции (XSS, SQLi, Эмодзи) ---
@pytest.mark.parametrize("security_payload", [
    pytest.param("<script>alert('xss')</script>", marks=pytest.mark.xfail(reason="Сайт защищен от XSS, текст не выводится")),
    "1' OR '1'='1",
    ":):):):))))::;)",
    pytest.param("<div>HTML injection</div>", marks=pytest.mark.xfail(reason="Сайт защищен от HTML-инъекций, текст не выводится")),
])
def test_security_and_special_inputs(driver, security_payload):
    page = TextBoxPage(driver)
    output = page.open().fill_form(
        name=security_payload,
        cur_addr=security_payload,
        perm_addr=security_payload
    ).submit().get_output_data()

    assert output is not None, "Форма упала при вводе спецсимволов/инъекций"
    assert output["name"] == security_payload


# --- 6. Пустая форма ---
def test_empty_form_submission(driver):
    page = TextBoxPage(driver)
    output = page.open().submit().get_output_data()

    if output is not None:
        assert output["name"] == ""
        assert output["email"] == ""

# Запустить python -m pytest TextBoxPageObject/test_text_box.py -v

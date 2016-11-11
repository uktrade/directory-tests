from tests import get_absolute_url, get_random_email_address


BAD_SIGNUP_MESSAGE = (
    'This field is required.'
)


def test_signup_bad_form(selenium):
    selenium.get(get_absolute_url('sso:signup'))
    (selenium
        .find_element_by_css_selector('[name="email"]')
        .send_keys(get_random_email_address()))
    (selenium
        .find_element_by_css_selector('[name="password1"]')
        .send_keys('some_password'))

    selenium.find_element_by_css_selector('[type="submit"]').click()
    assert BAD_SIGNUP_MESSAGE in selenium.page_source

from tests import get_url, get_random_email_address


GOOD_SIGNUP_MESSAGE = (
    'Verify your email address'
)


def test_signup_good_form(selenium):
    selenium.get(get_url('sso:signup'))
    (selenium
        .find_element_by_css_selector('[name="email"]')
        .send_keys(get_random_email_address()))
    (selenium
        .find_element_by_css_selector('[name="password1"]')
        .send_keys('some_password'))
    (selenium
        .find_element_by_css_selector('[name="password2"]')
        .send_keys('some_password'))
    selenium.find_element_by_css_selector('[type="submit"]').click()

    assert GOOD_SIGNUP_MESSAGE in selenium.page_source

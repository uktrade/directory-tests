from tests import get_url, get_random_email_address


BAD_PASSWORD_MESSAGE = (
    'The e-mail address and/or password you specified are not correct.'
)


def test_login_bad_credentials(selenium):
    url = get_url('sso:login')
    selenium.get(url)
    (selenium
        .find_element_by_css_selector('[name="login"]')
        .send_keys(get_random_email_address()))
    (selenium
        .find_element_by_css_selector('[name="password"]')
        .send_keys('some_password'))

    selenium.find_element_by_css_selector('[type="submit"]').click()

    assert BAD_PASSWORD_MESSAGE in selenium.page_source

import pytest

from tests import get_absolute_url, get_random_email_address, users

BAD_PASSWORD_MESSAGE = (
    'The e-mail address and/or password you specified are not correct.'
)


@pytest.fixture
def submit_login_form(selenium):
    def submit(username, password):
        selenium.get(get_absolute_url('sso:login'))
        (selenium
            .find_element_by_css_selector('[name="login"]')
            .send_keys(username))
        (selenium
            .find_element_by_css_selector('[name="password"]')
            .send_keys(password))
        selenium.find_element_by_css_selector('[type="submit"]').click()
    return submit


def test_login_good_credentials(selenium, submit_login_form):
    user = users['verified']
    submit_login_form(user['username'], user['password'])

    # the login cookie is shared with directory ui
    selenium.get(get_absolute_url('ui-buyer:landing'))
    assert '>Logout<' in selenium.page_source

    # and the user see they are logged in on sso
    selenium.get(get_absolute_url('sso:login'))
    assert '>Logout<' in selenium.page_source


def test_login_bad_credentials(selenium, submit_login_form):
    submit_login_form(get_random_email_address(), 'some_password')
    assert BAD_PASSWORD_MESSAGE in selenium.page_source

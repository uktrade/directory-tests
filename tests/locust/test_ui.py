import logging
import random

from locust import HttpLocust, TaskSet, task
from bs4 import BeautifulSoup

from tests import get_relative_url, get_absolute_url, settings
from tests.locust import USER_CREDENTIALS
from tests.locust.helpers import extract_main_error


class PublicPagesBuyerUI(TaskSet):
    @task
    def landing_page(self):
        self.client.get(get_relative_url('ui-buyer:landing'))

    @task
    def start_registration(self):
        self.client.get(get_relative_url('ui-buyer:register'))

    @task
    def companies_house_search(self):
        term = random.choice(
                ["food", "sweets", "road", "limited", "solutions", "house", 
                 "finance", "transport", "delivery", "robot"
                 ])
        params = {"term": term}
        self.client.get(
                get_relative_url("internal-api:companies-house-search"), 
                params=params,
                name="api/internal/companies-house-search/?term=[term]")


class AuthenticatedPagesBuyerUI(TaskSet):

    account_id = "NOT_FOUND"
    email = "NOT_FOUND"
    password = "NOT_FOUND"
    headers = {}

    def _login(self, data: dict):
        login_url = get_absolute_url('sso:login')
        with self.client.get(login_url) as response:
            soup = BeautifulSoup(response.content, 'html.parser')
            csrf_token = soup.find(
                'input', {'name': 'csrfmiddlewaretoken'}
            ).get('value')
        data["csrfmiddlewaretoken"] = csrf_token

        with self.client.post(login_url, data=data) as response:
            cookie = response.history[0].headers['Set-Cookie']
        self.headers = {'Cookie': cookie}

        logging.info(f"Successfully logged-in as: {self.email}")

    def on_start(self):
        if len(USER_CREDENTIALS) > 0:
            self.account_id, self.email, self.password = USER_CREDENTIALS.pop()
        data = {"login": self.email, "password": self.password}
        self._login(data)

    def _get_csrf_token(self, url):
        response = self.client.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        if response.status_code == 500:
            error = extract_main_error(response.content.decode("utf-8"))
            print(error)
        csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        token = csrf_input.get('value')
        return token

    @task
    def company_profile(self):
        self.client.get(
            get_relative_url('ui-buyer:company-profile'),
            headers=self.headers
        )

    def _upload_logo(self, path_to_img):
        url = get_relative_url('ui-buyer:upload-logo')
        img = open(path_to_img, 'rb')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'company_profile_logo_edit_view-current_step': 'logo'
        }
        self.client.post(
            url, data=data, files={'logo-logo': img}, headers=self.headers)

    @task
    def upload_logo(self):
        self._upload_logo('tests/functional/files/Wikipedia-logo-v2-en-alpa-channel.png')

    @task
    def upload_large_logo(self):
        self._upload_logo('tests/functional/files/Nagoya_Castle_Feb_2011_27.jpg')

    @task
    def edit_company_address(self):
        url = get_relative_url('ui-buyer:company-edit-address')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'address-address_confirmed': 'on',
            'supplier_address_edit_view-current_step': 'address',
            'address-postal_full_name': 'load tests',
        }
        self.client.post(url, data=data, headers=self.headers)

    @task
    def edit_company_address_invalid_data(self):
        url = get_relative_url('ui-buyer:company-edit-address')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'address-address_confirmed': '',  # Invalid
            'supplier_address_edit_view-current_step': 'address',
            'address-postal_full_name': 'DO NOT DELETE - LOAD TESTS',
        }
        self.client.post(url, data=data, headers=self.headers)

    @task
    def edit_company_description(self):
        url = get_relative_url('ui-buyer:company-edit-description')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'company_description_edit_view-current_step': 'description',
            'description-summary': 'DO NOT DELETE - LOAD TESTS',
            'description-description': 'DO NOT DELETE - LOAD TESTS',
        }
        self.client.post(url, data=data, headers=self.headers)

    @task
    def edit_company_description_invalid_data(self):
        url = get_relative_url('ui-buyer:company-edit-description')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'company_description_edit_view-current_step': 'description',
            'description-summary': '',  # Invalid
            'description-description': '',  # Invalid
        }
        self.client.post(url, data=data, headers=self.headers)

    @task
    def edit_company_key_facts(self):
        url = get_relative_url('ui-buyer:company-edit-key-facts')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'supplier_basic_info_edit_view-current_step': 'basic',
            'basic-name': f'DO NOT DELETE - LOAD TESTS {self.account_id}',
            'basic-website': f'https://load.test.{self.account_id}.com',
            'basic-keywords': 'load testing',
            'basic-employees': '51-200',
        }
        self.client.post(url, data=data, headers=self.headers)

    @task
    def edit_company_key_facts_invalid_data(self):
        url = get_relative_url('ui-buyer:company-edit-key-facts')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'supplier_basic_info_edit_view-current_step': 'basic',
            'basic-name': '',  # Invalid
            'basic-website': '',  # Invalid
            'basic-keywords': '',  # Invalid
            'basic-employees': '',  # Invalid
        }
        self.client.post(url, data=data, headers=self.headers)

    @task
    def edit_company_sectors(self):
        url = get_relative_url('ui-buyer:company-edit-sectors')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'supplier_classification_edit_view-current_step': 'classification',
            'classification-sectors': 'COMMUNICATIONS',
            'classification-has_exported_before': True,
            'classification-export_destinations': ['IN', 'US'],
            'classification-export_destinations_other': ''
        }
        self.client.post(url, data=data, headers=self.headers)

    @task
    def edit_company_contact(self):
        url = get_relative_url('ui-buyer:company-edit-contact')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'supplier_contact_edit_view-current_step': 'contact',
            'contact-email_full_name': f'DO NOT DELETE - LOAD TESTS {self.account_id}',
            'contact-email_address': self.email,
            'contact-website': f'http://load.test.{self.account_id}.com'
        }
        self.client.post(url, data=data, headers=self.headers)

    @task
    def edit_company_contact_invalid_data(self):
        url = get_relative_url('ui-buyer:company-edit-contact')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'supplier_contact_edit_view-current_step': 'contact',
            'contact-email_full_name': '',  # Invalid
            'contact-email_address': 'contactme@example.com',
        }
        self.client.post(url, data=data, headers=self.headers)

    @task
    def edit_company_social_media(self):
        url = get_relative_url('ui-buyer:company-edit-social-media')
        data = {
            'csrfmiddlewaretoken': self._get_csrf_token(url),
            'company_social_links_edit_view-current_step': 'social',
            'social-linkedin_url': 'http://linkedin.com',
            'social-twitter_url': 'http://twitter.com',
            'social-facebook_url': 'http://facebook.com',
        }
        self.client.post(url, data=data, headers=self.headers)


class RegularUserBuyerUI(HttpLocust):
    host = settings.DIRECTORY_UI_BUYER_URL
    task_set = PublicPagesBuyerUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT


class AuthenticatedUserBuyerUI(HttpLocust):
    host = settings.DIRECTORY_UI_BUYER_URL
    task_set = AuthenticatedPagesBuyerUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT


class PublicPagesSupplierUI(TaskSet):
    @task
    def landing_page(self):
        self.client.get(get_relative_url('ui-supplier:landing'))

    @task
    def register_interest(self):
        data = {
            'email_address': 'load@tests.com',
            'full_name': 'Mr Load Test',
            'sector': 'BIOTECHNOLOGY_AND_PHARMACEUTICALS',
            'terms': True,
            'company_name': 'load tests',
            'country': 'load tests',
        }
        self.client.post(
            get_relative_url('ui-supplier:subscribe'),
            data=data
        )

    @task
    def search(self):
        self.client.get(get_relative_url('ui-supplier:search'))

    @task
    def suppliers_detail(self):
        suppliers = [
            "suppliers/02793489/richmond-design-marketing-limited/",
            "suppliers/03267051/collinson-plc/",
            "suppliers/03452628/rs-hydro-limited/",
            "suppliers/04423574/in2connect-uk-ltd/",
            "suppliers/05403316/lightrhythm-visuals-ltd/",
            "suppliers/06057717/cantronik-ltd/",
            "suppliers/06719513/callidus-transport-engineering-ltd/",
            "suppliers/07253343/ed-fagan-europe-limited/",
            "suppliers/07396568/bridwell-company-limited/",
            "suppliers/07399608/joe-sephs/",
            "suppliers/07672659/knights-of-old-group-limited/",
            "suppliers/08191652/flora-harrison-limited/",
            "suppliers/08415302/fever-tree-drinks/",
            "suppliers/09314985/anvil-strength-and-conditioning-limited/",
            "suppliers/09400148/atlantic-pumps-limited/",
            "suppliers/09609186/outbenz-ltd/",
            "suppliers/09666195/evade-limited/",
            "suppliers/SC463767/quantum-aviation-limited/",
        ]
        self.client.get(random.choice(suppliers), name="/suppliers/[id]/[slug]/")

    @task
    def case_study(self):
        case_studies = [
            "case-study/12/water-usage-at-an-oil-refinery/",
            "case-study/13/royal-united-hospital-bath/",
            "case-study/14/large-residential-development-land-east-of-coldhar/",
            "case-study/17/cradle-bridge-retail-park/",
            "case-study/20/recently-developed-alloy-for-precision-tools-and-d/",
            "case-study/21/collaboration-with-local-university/",
            "case-study/22/scorpion-tooling-and-ed-fagan-working-to-produce/",
            "case-study/55/radio-2-hyde-park/",
            "case-study/61/baja-rally-mexico-consolidation-logistics/",
            "case-study/66/naiad-dynamics-inc-full-colour-displays/",
            "case-study/89/atlas-silo-range/",
            "case-study/93/to-export-high-end-shoes-and-handbags-exhibition-a/",
            "case-study/163/crimp-contacts-in-m12-connectors-save-time-and-mon/",
        ]
        self.client.get(random.choice(case_studies), name="/case-study/[id]/[slug]/")

    @task
    def industries(self):
        self.client.get(get_relative_url('ui-supplier:industries'))

    @task
    def industries_health(self):
        self.client.get(get_relative_url('ui-supplier:industries-health'))

    @task
    def industries_tech(self):
        self.client.get(get_relative_url('ui-supplier:industries-tech'))

    @task
    def industries_creative(self):
        self.client.get(get_relative_url('ui-supplier:industries-creative'))

    @task
    def industries_food(self):
        self.client.get(get_relative_url('ui-supplier:industries-food'))


class RegularUserSupplierUI(HttpLocust):
    host = settings.DIRECTORY_UI_SUPPLIER_URL
    task_set = PublicPagesSupplierUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT

import random
from uuid import uuid4

from locust import HttpLocust, TaskSet, task

from directory_client_core.authentication import SessionSSOAuthenticator

from tests import get_relative_url, settings, get_absolute_url
from tests.locust.helpers import (
    AuthedClientMixin,
    authenticate_with_sso,
    get_two_valid_sso_sessions,
    get_valid_sso_session_id,
)
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN
from tests.settings import DIRECTORY_API_CSV_DUMP_AUTH_TOKEN as CSV_TOKEN


class PublicPagesAPI(TaskSet):

    @task
    def api_health_check_ping(self):
        params = {'token': TOKEN}
        self.client.get(
            get_relative_url('api:healthcheck-ping'), params=params,
            name="/healthcheck/ping/?token=[token]"
        )

    @task
    def api_health_check_database(self):
        params = {'token': TOKEN}
        self.client.get(
            get_relative_url('api:healthcheck-database'), params=params,
            name="/healthcheck/database/?token=[token]"
        )

    @task
    def api_health_check_cache(self):
        params = {'token': TOKEN}
        self.client.get(
            get_relative_url('api:healthcheck-cache'), params=params,
            name="/healthcheck/cache/?token=[token]"
        )

    @task
    def api_health_check_elasticsearch(self):
        params = {'token': TOKEN}
        self.client.get(
            get_relative_url('api:healthcheck-elasticsearch'), params=params,
            name="/healthcheck/elasticsearch/?token=[token]"
        )

    @task
    def api_health_check_single_sign_on(self):
        params = {'token': TOKEN}
        self.client.get(
            get_relative_url('api:healthcheck-single-sign-on'), params=params,
            name="/healthcheck/single-sign-on/?token=[token]"
        )


class BuyerAPITests(TaskSet):

    @task
    def create_buyer(self):
        """
        There's no method to delete buyers from /admin/buyer/buyer/
        """
        url = get_relative_url('api:buyer')
        rid = f"{random.randint(1, 99999999):08d}"
        form_data = {
            'company_name': f'DELETE ME - LOAD TESTS {rid}',
            'country': 'DIT',
            'email': f'delete.me+{rid}@load.tests.com',
            'name': f'DELETE ME - LOAD TESTS {rid}',
            'sector': 'FOOD_AND_DRINK',
        }
        self.client.post(url=url, data=form_data, name=url, expected_codes=[201])

    @task
    def get_csv_dump(self):
        """
        This endpoint doesn't work due to this bug:
        https://uktrade.atlassian.net/browse/TT-399
        """
        url = get_relative_url('api:buyer-csv-dump')
        params = {'token': CSV_TOKEN}
        self.client.get(url=url, params=params, name=url, expected_codes=[200])


class CompanyAPITests(TaskSet):

    industries = [
        'AEROSPACE', 'AIRPORTS', 'AUTOMOTIVE', 'CHEMICALS',
        'COMMUNICATIONS', 'CONSTRUCTION', 'ENVIRONMENT', 'MARINE',
        'MINING', 'OIL_AND_GAS', 'POWER', 'RAILWAYS', 'SECURITY'
    ]
    ids = [
        'CS000957', '06361746', '10569028', '11207586', '11059126',
        '08900453', '10186328', '10990165', '08836305', '11170686',
        '11160954', '09500711', 'SC433069', '01717696', 'SC537145',
        '11195103', '09177818', '08070404', '04361671', '07646615',
    ]

    @task
    def validate_company_number(self):
        rid = f"{random.randint(1, 99999999):08d}"
        url = get_relative_url('api:validate-company-number')
        self.client.get(f'{url}?number={rid}', name=url, expected_codes=[200])

    @task
    def list_company_profiles(self):
        url = get_relative_url('api:public-company')
        self.client.get(url, name=url, expected_codes=[200])

    @task
    def companies_house_existing_profile(self):
        cid = random.choice(self.ids)
        url = get_relative_url('api:public-company-profile')
        self.client.get(url.format(companies_house_number=cid), name='/public/company/{existing_ch_id/', expected_codes=[200])

    @task
    def companies_house_non_existing_profile(self):
        cid = f"{random.randint(1, 99999999):08d}"
        url = get_relative_url('api:public-company-profile')
        self.client.get(url.format(companies_house_number=cid), name='/public/company/{non_existing_ch_id/', expected_codes=[200, 404])

    @task
    def get_company_by_authenticated_sso_session(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:supplier-company')
        self.client.get(url, name='supplier/company/', expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def patch_company_update_profile(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:supplier-company')
        data = {
            'has_exported_before': random.choice([True, False]),
            'description': f'DELETE ME - Load Test Company',
        }
        self.client.patch(url, data=data, name=url, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def add_update_get_case_study(self):
        url = get_relative_url('api:supplier-company-case-study')
        url_by_id = get_relative_url('api:supplier-company-case-study-by-id')
        url_public = get_relative_url('api:public-case-study')
        rid = f"{random.randint(1, 99999999):08d}"
        sso_session_id = get_valid_sso_session_id()
        data = {
            'description': 'delete me - load test case study',
            'title': f'delete me - load test case study {rid}',
            'keywords': 'load tests, case study',
            'sector': random.choice(self.industries),
        }
        r = self.client.post(url, data=data, name=url, expected_codes=[201], authenticator=SessionSSOAuthenticator(sso_session_id))
        pk = r.json()['pk']
        data = {'description': f'delete me - updated load test case study {rid}'}
        self.client.patch(url_by_id.format(id=pk), data=data, name=url_by_id, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))
        self.client.get(url_by_id.format(id=pk), name=url_by_id, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))
        self.client.get(url_public.format(id=pk), name=url_public, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def verify_with_code(self):
        url = get_relative_url('api:supplier-company-verify')
        sso_session_id = get_valid_sso_session_id()
        data = {'code': f"{random.randint(1, 999999999):08d}"}
        self.client.post(url, data=data, name=url, expected_codes=[200, 400], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def verify_with_companies_house(self):
        url = get_relative_url('api:supplier-company-verify-companies-house')
        sso_session_id = get_valid_sso_session_id()
        data = {'access_token': f"{random.randint(1, 999999999):08d}"}
        self.client.post(url, data=data, name=url, expected_codes=[200, 400], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def contact_supplier(self):
        url = get_relative_url('api:contact-supplier')
        rid = f"{random.randint(1, 99999999):08d}"
        data = {
            'sender_company_name': f'delete.me+{rid}@load.tests.com',
            'sender_name': f'delete.me+{rid}@load.tests.com',
            'sender_country': 'dit',
            'recipient_company_number': random.choice(self.ids),
            'sender_email': f'delete.me+{rid}@load.tests.com',
            'subject': f'DELETE ME - LOAD TESTS {rid}',
            'body': f'DELETE ME - LOAD TESTS {rid}',
            'sector': random.choice(self.industries),
        }
        self.client.post(url, data=data, name=url, expected_codes=[202])

    @task
    def search_company(self):
        url = get_relative_url('api:company-search')
        params = {
            'size': 10,
            'page': 1,
            'no_description': random.choice([True, False]),
            'has_description': random.choice([True, False]),
            'no_case_study': random.choice([True, False]),
            'one_case_study': random.choice([True, False]),
            'multiple_case_studies': random.choice([True, False]),
            'term': 'test',
            'sectors': [random.choice(self.industries)],
            'is_showcase_company': random.choice([True, False]),
        }
        self.client.get(url, params=params, name=url, expected_codes=[200])

    @task
    def search_for_case_studies(self):
        url = get_relative_url('api:case-study-search')
        params = {
            'size': random.randint(1, 50),
            'page': random.randint(1, 3),
            'term': 'test',
            'sectors': [random.choice(self.industries)],
            'campaign_tag': 'food-is-great',
        }
        self.client.get(url, params=params, name=url, expected_codes=[200])

    @task
    def get_collaborators(self):
        url = get_relative_url('api:supplier-company-collaborators')
        sso_session_id = get_valid_sso_session_id()
        self.client.get(url, name=url, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    #TODO finish off this only when it won't required too much time
    #@task
    def create_get_and_accept_collaboration_invitation(self):
        url_remove = get_relative_url('api:supplier-company-remove-collaborators')
        url_collabs = get_relative_url('api:supplier-company-collaborators')

        inviter, invitee = get_two_valid_sso_sessions()

        url_supplier = get_relative_url('api:supplier')
        r = self.client.get(url_supplier, name=url_supplier, expected_codes=[200], authenticator=SessionSSOAuthenticator(invitee))
        print(f'get Invitee\'s email and sso_id {r.json()}')
        invitee_sso_id = r.json()['sso_id']
        invitee_email = r.json()['company_email']

        url = get_relative_url('api:supplier-company-collaboration-invite')
        data = {'collaborator_email': invitee_email}
        r = self.client.post(url, name=url, data=data, expected_codes=[201], authenticator=SessionSSOAuthenticator(inviter))
        print(f'create invitation for invitee: {r.content}')
        uuid = r.json()['uuid']

        url_by_uuid = get_relative_url('api:supplier-company-collaboration-invite-by-uuid')
        r = self.client.get(url_by_uuid.format(uuid=uuid), name=url_by_uuid, expected_codes=[200], authenticator=SessionSSOAuthenticator(inviter))
        print(f'get invitation by uuid: {r.content}')

        data = {'accepted': True}
        r = self.client.patch(url_by_uuid.format(uuid=uuid), data=data, name=url_by_uuid, expected_codes=[200], authenticator=SessionSSOAuthenticator(invitee))
        print(f'Invitee accepts the invitation: {r.content}')

        r = self.client.get(url_collabs, name=url_collabs, expected_codes=[200], authenticator=SessionSSOAuthenticator(inviter))
        print(f'get list of collaborators: {r.content}')

        data = {'sso_ids': [invitee_sso_id]}
        r = self.client.post(url_remove, data=data, name=url_remove, expected_codes=[200], authenticator=SessionSSOAuthenticator(inviter))
        print(f'remove collaborator: {r.content}')


class EnrolmentAPITests(TaskSet):

    @task
    def enroll_company(self):
        """
        A random company number has to be generated for every request in order
        to avoid 500 ISE caused by https://uktrade.atlassian.net/browse/TT-395

        TestAPI endpoint is used to delete created profile.
        """
        url = get_relative_url('api:enrolment')
        rid = f"{random.randint(1, 99999999):08d}"
        form_data = {
            'contact_email_address': f'delete.me+{rid}@load.tests.com',
            'company_name': f'DELETE ME - DIT LOAD TESTS {rid}',
            'company_email': f'delete.me+{rid}@load.tests.com',
            'company_number': rid,
            'sso_id': random.randint(1, 99999)
        }
        self.client.post(url=url, data=form_data, name=url, expected_codes=[201])
        self.client.delete(url=f'testapi/company/{rid}/', name='testapi/company/', expected_codes=[204, 404])


class ExportReadinessAPITests(TaskSet):

    article_uuids = [
        '0a0ef172-5505-40d6-b665-9fcc06b56c26',
        '0a2c0a83-ebcd-4b8c-88cd-dca71507521e',
        '12b13d60-973f-4e1c-beec-04fdec81195b',
        '15cedd6c-ad4b-4b88-9ddc-08ebb0b37a9b',
        '2782e417-c29e-4a19-937f-5f28cd6c8709',
        '29dd97ad-28a9-4347-81d8-da167a849e9e',
        '2e58592d-5812-4d48-82fc-0d665f55e567',
        '339edd4c-73a5-4b83-86a2-72121f1ecb6f',
        '454ff6ad-5318-4f1b-8d8e-0a6b83bb0c81',
        '489700dd-4c0c-44b2-be1c-7560c06dd2df',
        '4fd7f118-6337-453c-a6f6-7d9c3a1db1b0',
        '55f80943-8a97-448b-8d1d-e2179d5194a4',
        '597abb09-a426-4d8d-9478-801317aed3ab',
        '5b3dde4b-ccc6-4d5f-80f7-a1cd08f11a0a',
        '87f09be7-bbb7-45a7-a171-1961ea5d6448',
        '88b4947d-de73-4423-bd39-6fca14022825',
        '8b3f0454-5821-4635-a755-9e5a0214c594',
        '8e543771-4403-4cfb-b453-e8dfeef9cfbc',
        '91c59adc-6437-479f-a8f1-e895dd2d915a',
        '98ef1246-4e23-4d3d-a0ee-4917bc72859e',
        '9c5f5ce1-2e1b-44cc-9c4f-b1484df4abf1',
        '9ea1eafc-42d9-4f77-977f-21f1c43e15d8',
        '9f7475e1-e36b-4859-8f4b-36709182169e',
        'a06593fc-4bc5-4f78-bc1c-5a6b955eaea9',
        'a2a86b93-7956-40ff-b588-5f14822f4476',
        'a7260a14-b12c-497b-af78-1414095f87ac',
        'b49ed59b-5681-4745-a43d-c830b67bbc30',
        'b654a138-5a79-403f-85ac-7656b2a9b25b',
        'b8634084-9056-43bf-80b5-bb9dd35478f0',
        'bc36cb37-0bca-49f8-bbb5-6e8de8e7a59c',
        'be68740b-7b7e-4fbb-9289-0f077c607345',
        'bf2ff3d6-6d10-446a-8115-54de1958a196',
        'bf5c2e58-aecf-40a8-a0c8-6a6ae109687e',
        'c36b6bf5-5595-42ed-9ef8-0c9418c6e81c',
        'c5711570-1414-4d72-a45f-a5a22dc211fb',
        'c7cfec0b-9bb1-415b-a5ca-689cf35966d5',
        'cba2106a-abc0-40d0-9807-e5ff627a5d18',
        'd15a71ce-e071-4bcd-8af8-7a6cb079ce97',
        'd20c0036-f8f9-4ff2-b289-2a10ae2ace32',
        'db9b6493-6f4d-4bc7-bdc6-f91f3431fa97',
        'e18013b4-da94-4ef4-bc8b-702edd414003',
        'eeea2324-f4fe-4d72-b221-5fbb078c4800',
        'f42400fd-8301-4cda-93a7-b6f51f1b4b30',
        'f846d5f3-8e19-49ca-8592-53b060a0f244',
        'f9d2f878-7675-49a8-8db4-e9805d78ee22',
    ]

    @task
    def submit_triage_results(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:export-readiness-triage')
        form_data = {
            'exported_before': random.choice([True, False]),
            'company_name': 'DELETE ME - LOAD TESTS',
        }
        r = self.client.get(url=url, name=url, expected_codes=[200, 404], authenticator=SessionSSOAuthenticator(sso_session_id))
        if r.status_code == 404:
            self.client.post(url=url, name=url, data=form_data, expected_codes=[201], authenticator=SessionSSOAuthenticator(sso_session_id))
        else:
            self.client.patch(url=url, name=url, data=form_data, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def submit_article_read(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:export-readiness-article-read')
        data = {'article_uuid': random.choice(self.article_uuids)},
        self.client.post(url=url, data=data, name=url, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def submit_article_read_in_bulk(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:export-readiness-article-read')
        article_uuids = random.sample(self.article_uuids, random.randint(1, len(self.article_uuids)))
        data = [
            {'article_uuid': uuid} for uuid in article_uuids
        ]
        self.client.post(url=url, data=data, name=url, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def get_article_read(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:export-readiness-article-read')
        self.client.get(url=url, name=url, expected_codes=[200, 404], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def submit_completed_tasks(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:export-readiness-task-completed')
        data = {'task_uuid': str(uuid4())}
        self.client.post(url=url, data=data, name=url, expected_codes=[201], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def get_completed_tasks(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:export-readiness-task-completed')
        self.client.get(url=url, name=url, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))


class ExportOpportunityAPITests(TaskSet):

    @task
    def create_food_opportunity(self):
        url = get_relative_url('api:export-opportunity-food')
        rid = random.randint(1, 9999999)
        data = {
            'full_name': f'DELETE ME - LOAD TESTS {rid}',
            'job_title': f'DELETE ME - LOAD TESTS {rid}',
            'email_address': f'delete.me+{rid}@load.tests.com',
            'company_name': f'DELETE ME - LOAD TESTS {rid}',
            'company_website': f'https://load.tests.com/{rid}',
            'phone_number': f'0044730{rid:07d}',
            'contact_preference': [random.choice(['EMAIL', 'PHONE'])],
            'campaign': f'food-is-great',
            'country': random.choice(['france', 'singapore']),
            'business_model': [random.choice(['distribution', 'wholesale', 'retail'])],
            'business_model_other': '',
            'target_sectors': [random.choice(['retail', 'hospitality', 'catering', 'manufacturing'])],
            'target_sectors_other': '',
            'products': [random.choice(['DISCOUNT', 'PREMIUM'])],
            'products_other': '',
            'order_size': random.choice(['1-1000', '1000-10000', '10000-100000', '100000+']),
            'order_deadline': random.choice(['1-3 MONTHS', '3-6 MONTHS', '6-12 MONTHS', 'NA']),
            'additional_requirements': '',
        }
        self.client.post(url=url, data=data, name=url, expected_codes=[201])

    @task
    def create_legal_opportunity(self):
        url = get_relative_url('api:export-opportunity-legal')
        rid = random.randint(1, 9999999)
        data = {
            'full_name': f'DELETE ME - LOAD TESTS {rid}',
            'job_title': f'DELETE ME - LOAD TESTS {rid}',
            'email_address': f'delete.me+{rid}@load.tests.com',
            'company_name': f'DELETE ME - LOAD TESTS {rid}',
            'company_website': f'https://load.tests.com/{rid}',
            'phone_number': f'0044730{rid:07d}',
            'contact_preference': [random.choice(['EMAIL', 'PHONE'])],
            'campaign': f'food-is-great',
            'country': random.choice(['france', 'singapore']),
            'advice_type': [random.choice(['General-business-advice-and-partnership', 'Business-start-up-advice', 'Drafting-of-contracts',
                                           'Mergers-and-acquisitions', 'Immigration', 'Dispute-resolution'])],
            'advice_type_other': '',  # blank=True
            'business_model': [random.choice(['distribution', 'wholesale', 'retail'])],
            'business_model_other': '',
            'target_sectors': [random.choice(['TECHNOLOGY', 'FOOD_AND_DRINK', 'FINANCIAL_AND_PROFESSIONAL_SERVICES', 'MARINE', 'ENERGY'])],
            'target_sectors_other': '',
            'order_deadline': random.choice(['1-3 MONTHS', '3-6 MONTHS', '6-12 MONTHS', 'NA']),
            'additional_requirements': '',
        }
        self.client.post(url=url, data=data, name=url, expected_codes=[201])


class NotificationAPITests(TaskSet):

    @task
    def unsubscribe_from_notifications(self):
        url = get_relative_url('api:notifications-anonymous-unsubscribe')
        data = {
            'email': 'delete.me@load.tests.com',
        }
        self.client.post(url=url, data=data, name=url, expected_codes=[200])


class SupplierAPITests(TaskSet):

    @task
    def update_supplier_details(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:supplier')
        data = {
            'is_company_owner': random.choice([True, False]),
        }
        self.client.patch(url, name=url, data=data, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def get_supplier_details(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:supplier')
        self.client.get(url, name=url, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def unsubscribe_supplier(self):
        sso_session_id = get_valid_sso_session_id()
        url = get_relative_url('api:supplier-unsubscribe')
        self.client.post(url, name=url, expected_codes=[200], authenticator=SessionSSOAuthenticator(sso_session_id))

    @task
    def get_csv_dump(self):
        """
        This endpoint doesn't work due to this bug:
        https://uktrade.atlassian.net/browse/TT-399
        """
        url = get_relative_url('api:supplier-csv-dump')
        params = {'token': CSV_TOKEN}
        self.client.get(url=url, params=params, name=url, expected_codes=[200])


class AllAPITestsWithAuthenticatedUser(
        BuyerAPITests,
        CompanyAPITests, 
        EnrolmentAPITests,
        ExportOpportunityAPITests,
        ExportReadinessAPITests,
        NotificationAPITests, 
        SupplierAPITests):
    pass


class RegularUserAPI(HttpLocust):
    host = settings.DIRECTORY_API_URL
    task_set = PublicPagesAPI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT


class AuthenticatedUserAPI(AuthedClientMixin, HttpLocust):
    host = settings.DIRECTORY_API_URL
    task_set = AllAPITestsWithAuthenticatedUser
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT

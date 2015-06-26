import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact
from gaiatest.apps.contacts.app import Contacts
from utilities.measures import Helpers


class TestPerformance(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(self.__class__, self).__init__(*args, **kwargs)

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.contacts_num = self.testvars['performance']['contacts_num']
        self.RUNS = self.testvars['performance']['runs']
        self.helpers = Helpers(self)

    def tearDown(self):
        if self.testvars['performance']['verbose']:
            print "Measures: {}".format(self.helpers.measures)
        self.helpers.print_measures()
        GaiaTestCase.tearDown(self)

    def _insert_contacts(self):
        self.contacts = [MockContact() for i in range(self.contacts_num)]
        map(self.data_layer.insert_contact, self.contacts)

    def test_get_performance_measures(self):
        self._insert_contacts()
        if self.testvars['performance']['verbose']:
            print "Number of runs: {}".format(self.RUNS)

        for i in range(self.RUNS):
            if self.testvars['performance']['verbose']:
                print "Run #{}\n".format(i + 1)
            contacts_app = Contacts(self.marionette)
            contacts_app.launch()
            contacts_app.wait_for_contacts(number_to_wait_for=self.contacts_num)

            # Tap on the first contact, to see its details
            contact_details = contacts_app.contact(self.contacts[0]['givenName']).tap()
            map(self.helpers.store_measures,
                ['list_first_contact_rendered', 'list_chunk_contact_rendered',
                 'list_all_contacts_rendered', 'details_contact_rendered'])

            if i + 1 < self.RUNS:
                GaiaTestCase.setUp(self)
                self._insert_contacts()
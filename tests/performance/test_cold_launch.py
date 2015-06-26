from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact
from gaiatest.apps.contacts.app import Contacts
from utilities.measures import Helpers
import numpy

class TestPerformance(GaiaTestCase):
    measures = {}

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(self.__class__, self).__init__(*args, **kwargs)

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.contacts_num = self.testvars['performance']['contacts_num']
        self.RUNS = self.testvars['performance']['runs']

        self.contacts = [MockContact() for i in range(self.contacts_num)]
        map(self.data_layer.insert_contact, self.contacts)

    def tearDown(self):
        if self.testvars['performance']['verbose']:
            print "Measures: {}".format(self.measures)
        self.print_measures()
        GaiaTestCase.tearDown(self)

    def test_get_performance_measures(self):
        if self.testvars['performance']['verbose']:
            print "Number of runs: {}".format(self.RUNS)

        for i in range(self.RUNS):
            contacts_app = Contacts(self.marionette)
            contacts_app.launch()
            contacts_app.wait_for_contacts(number_to_wait_for=self.contacts_num)

            contact_details = contacts_app.contact(self.contacts[0]['givenName']).tap()
            map(self.store_measures, 
                ['list_first_contact_rendered', 'list_chunk_contact_rendered', 'list_all_contacts_rendered', 'details_contact_rendered'])

            self.setUp()

    def print_measures(self):
        print "\nMeasure\t\t\t\t\t\tMean\t\t\tMedian\t\t\tMin\t\t\tMax\t\t\tStdDev"
        print "----------------------------------------------------------------------------------------------------------------------------------"
        for k,v in self.measures.items():
            print "{}\t\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(k, numpy.mean(v), numpy.median(v), min(v), max(v), numpy.std(v))
        print "-----------------------------------------------------------------\n"

    def store_measures(self, measure_name):
        if self.testvars['performance']['verbose']:
            print "Storing measure -> {}".format(measure_name)

        duration = self.marionette.execute_script(
            '''return window.wrappedJSObject.utils.PerformanceHelper.common.getLastMeasure(arguments[0]).duration;''', 
            script_args=[measure_name])
        if measure_name not in self.measures:
            self.measures[measure_name] = [duration]
        else:
            self.measures.get(measure_name).append(duration)

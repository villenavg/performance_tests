import numpy


class Helpers(object):

    def __init__(self, parent):
        print "Init Helpers"
        self.parent = parent
        self.measures = {}

    def print_measures(self):
        print "\nMeasure\t\t\t\t\t\tMean\t\t\tMedian\t\t\tMin\t\t\tMax\t\t\tStdDev"
        print "----------------------------------------------------------------------------------------------------------------------------------"
        for k, v in self.measures.items():
            print "{}\t\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(k, numpy.mean(v), numpy.median(v), min(v), max(v), numpy.std(v))
        print "-----------------------------------------------------------------\n"

    def store_measures(self, measure_name):
        if self.parent.testvars['performance']['verbose']:
            print "Storing measure -> {}".format(measure_name)

        duration = self.parent.marionette.execute_script(
            '''return window.wrappedJSObject.utils.PerformanceHelper.common.getLastMeasure(arguments[0]).duration;''',
            script_args=[measure_name])
        if measure_name not in self.measures:
            self.measures[measure_name] = [duration]
        else:
            self.measures.get(measure_name).append(duration)

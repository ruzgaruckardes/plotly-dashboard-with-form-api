from jotform import *

class JotFormClient:

    def __init__(self, apikey):
        self.__apiKey = apikey
        self.__myClient = JotformAPIClient(self.__apiKey)

    def getting_forms(self, filter_array=None, limit=None):
        allforms = self.__myClient.get_forms(self, filterArray=filter_array, limit=limit)
        return allforms

    def getting_answer(self, filter_array=None, limit=None):
        allsubmissions = self.__myClient.get_submissions(self, filterArray=filter_array, limit=limit)
        return allsubmissions



from .browser import Browser


class StatefulBrowser(Browser):
    def __init__(self, session=None, soup_config=None, requests_adapters=None):
        super(StatefulBrowser, self).__init__(
            session, soup_config, requests_adapters)
        self.__debug = False
        self.__verbose = 0
        self.__current_page = None
        self.__current_url = None
        self.__current_form = None

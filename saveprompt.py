import gedit

WINDOW_DATA_KEY = "SavePromptKey"

class WindowHelper:
    def __init__(self, window):
        self._window = window

        self.signals = {window: [self._window.connect('tab-added', self.on_tab_added),
                                 self._window.connect('tab-removed', self.on_tab_removed)]}

        for doc in self._window.get_documents():
            self.monitor_document(doc)

    def monitor_document(self, doc):
        self.signals[doc] = [doc.connect_after('changed', self.on_doc_changed)]

    def deactivate(self):
        for obj in self.signals:
            for signal in self.signals[obj]:
                obj.disconnect(signal)

        self._window = None

    def on_tab_added(self, window, tab):
        self.monitor_document(tab.get_document())

    def on_tab_removed(self, window, tab):
        doc = tab.get_document()

        for signal in self.signals[doc]:
            doc.disconnect(signal)

        del self.signals[doc]

    def on_doc_changed(self, doc):
        bounds = doc.get_bounds()

        if bounds[0].equal(bounds[1]):
            doc.set_modified(False)

class Plugin(gedit.Plugin):
    def activate(self, window):
        window.set_data(WINDOW_DATA_KEY, WindowHelper(window))

    def deactivate(self, window):
        helper = window.get_data(WINDOW_DATA_KEY)

        if helper:
            helper.deactivate()
            window.set_data(WINDOW_DATA_KEY, None)

# vi:ex:ts=4:et

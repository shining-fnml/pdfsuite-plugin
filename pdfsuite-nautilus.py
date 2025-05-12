from gi.repository import Nautilus, GObject
import pdfsuite.pdfsuite as pdfsuite

class NautilusPdfSuitePlugin(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, files):
        return pdfsuite.pdfSuitePlugin(Nautilus, files)

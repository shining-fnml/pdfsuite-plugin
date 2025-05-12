from gi.repository import GObject, Gtk, Thunarx
import pdfsuite.pdfsuite as pdfsuite

class ThunarPdfSuitePlugin(GObject.GObject, Thunarx.MenuProvider):
    def __init__(self):
        pass
    
    def get_file_menu_items(self, window, files):
        return pdfsuite.pdfSuitePlugin(Thunarx, files)

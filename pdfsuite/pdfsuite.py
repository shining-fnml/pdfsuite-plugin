import os
import re
from shutil import which
import subprocess

class PdfSuitePlugin:
    def __init__(self, requireds, **kwargs):
        self.ready = True
        self._kwargs={}
        for required in requireds:
            if which(required) is None:
                self.ready = False
                return
        for k,v in kwargs.items():
            if k=='name':
                self._kwargs[k] = "PdfSuiteMenuProvider::"+v
            else:
                self._kwargs[k] = v

    def callback(self, menu, files):
        '''Called when user chooses files though file manager context menu.
        '''
        for file_obj in files:
            # Check if file still exists
            try:
                if not file_obj.is_gone():
                    gio_file = file_obj.get_location()
                    self.run(gio_file.get_path())
            except AttributeError: # missing in Thunar
                gio_file = file_obj.get_location()
                self.run(gio_file.get_path())

    def kwargs(self, translate):
        if translate and 'tooltip' in self._kwargs.keys():
            self._kwargs['tip'] = self._kwargs['tooltip']
            del self._kwargs['tooltip']
        return self._kwargs

    @classmethod
    def plugin(cls, filemanager):
        pass


class EntryChangeResolution(PdfSuitePlugin):
    def __init__(self):
        kwargs = {'name':'ChangeResolutionPdf',
                  'label':'Cambia la risoluzione',
                  'tooltip':'Cambia la risoluzione per ridurre la dimensione del file',
                  'icon':'x-office-document-template'}
        super().__init__(['gs'], **kwargs)

    def run(self, filename_in):
        directory, ext = os.path.splitext(filename_in)
        filename_noext = os.path.basename(directory)
        directory += '.dir'
        if not os.path.exists(directory):
            os.makedirs(directory)
        levels=( "screen", "ebook", "printer", "prepress", "default" )
        command_common = ['gs', '-sDEVICE=pdfwrite', "-dNOPAUSE", "-dBATCH", "-dCompatibilityLevel=1.4" ]
        for level in levels:
            command_part = []
            filename_out = directory + "/" + level + '-' + filename_noext + ".pdf"
            command_part.append("-dPDFSETTINGS=/" + level)
            command_part.append("-sOutputFile=" + filename_out)
            command_part.append(filename_in)
            subprocess.call(command_common+command_part)


class EntryCropA4(PdfSuitePlugin):
    def __init__(self):
        kwargs = {'name':'CropPdf',
                  'label':'Taglia in A4',
                  'tooltip':'Taglia il documento al formato A4',
                  'icon':'applications-accessories'}
        super().__init__(['gs', 'pdfinfo'], **kwargs)

    @staticmethod
    def _cropbox(line):
        m = re.match('\/CropBox \[[0-9]+ [0-9]+ [0-9]+ [0-9]+\]', line)
        return m is not None

    def _grep_in_file(self, filename_in):
        with open(filename_in, 'rb') as fildes:
            lines = fildes.readlines()
            for line in lines:
                try:
                    line = line.decode()
                except UnicodeDecodeError:
                    pass
                else:
                    if self._cropbox(line.rstrip()):
                        return line.rstrip();
        return None;

    @staticmethod
    def _grep_in_stream(callback, stream):
        lines = stream.decode().split()
        for line in lines:
            if line == '':
                break
            if callback(line.rstrip()):
                return line.rstrip();
        return None;

    @staticmethod
    def _insert_str(string, str_to_insert, index):
        return string[:index] + str_to_insert + string[index:]

    @staticmethod
    def _is_A4(line):
        pattern_float = "[[0-9]+[.]?]?[0-9]+"
        pattern_full = 'Page size: +'+pattern_float+' x '+pattern_float+' pts( +\((.+)\))?'
        m = re.match(pattern_full, line)
        if m is None:
            return False
        for i in range(sys.maxsize):
            eprint("i: {}".format(i))
            a4 = m.group(i)
            if a4 is None:
                return False
            if a4 == "A4":
                return True
        return False

    def run(self, filename_in):
        proc = subprocess.run(args=['pdfinfo',filename_in],capture_output=True)
        match = self._grep_in_stream(self._is_A4, proc.stdout)
        if match is None:
            position = filename_in.lower().find('.pdf')
            if position > -1:
                filename_out = self._insert_str(filename_in, '_A4', position)
            command_common = [ 'gs', '-sDEVICE=pdfwrite', '-o', filename_out, '-f', filename_in]
            if self._grep_in_file(filename_in) is None:
                command_part = ['-c', '[/CropBox [0 165.64 595.2 1007.52] /PAGES pdfmark']
            else:
                command_part = ['-sPAPERSIZE=a4', '-dFIXEDMEDIA', '-c', '<</PageOffset [0 -166]>> setpagedevice']
            print (command_common+command_part)
            subprocess.call(command_common+command_part)


class Folder(PdfSuitePlugin):
    def __init__(self):
        kwargs = { 'name': 'Folder', 'label': "Pdf Suite", 'tooltip': '', 'icon': 'gnome-mime-application-pdf' }
        super().__init__([], **kwargs)


def pdfSuitePlugin(filemanager, files):
    '''Attaches context menu in filemanager to local file objects only.
    '''
    if not files:
        return

    for file_obj in files:
        # Do not attach context menu to a directory
        if file_obj.is_directory():
            return
        # Do not attach context menu  to anything other that a file
        # local files only; not remote
        if file_obj.get_uri_scheme() != 'file':
            return
        # Only attach context menu to pdf files
        if not all(file.get_name().lower().endswith(".pdf") for file in files):
            return

    submenu = filemanager.Menu()
    folder = Folder()
    translate = False
    try:
        top_menuitem = filemanager.MenuItem(**folder.kwargs(translate))
    except TypeError:
        translate = True
        top_menuitem = filemanager.MenuItem(**folder.kwargs(translate))
    for entry in [EntryCropA4(), EntryChangeResolution()]:
        kwargs = entry.kwargs(translate)
        if kwargs:
            subitem = filemanager.MenuItem(**kwargs)
            subitem.connect("activate", entry.callback, files)
            submenu.append_item(subitem)
    try:
        top_menuitem.set_submenu(submenu) # Nautilus only
    except AttributeError:
        top_menuitem.set_menu(submenu) # Thunarx only
    return top_menuitem,

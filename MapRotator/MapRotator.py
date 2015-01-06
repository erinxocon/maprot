#import the clr to add references
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

#general imports
import wpf
import System
import Microsoft

#import XAML
#import XAMLstr

#import the window and application objects from System
from System.Windows import Application, Window, Forms


class MyWindow(Window):
    def __init__(self):
        #with System.IO.StringReader(XAMLstr.xaml_str) as stream:
        #    wpf.LoadComponent(self, stream)

        wpf.LoadComponent(self, 'MapRotator.xaml')

    def get_path(self):
        return self._path

    def set_path(self, value):
        self._path = value

    path = property(get_path, set_path)

    def get_destinationFolder(self):
        return self._destinationFolder

    def set_destinationFolder(self, value):
        self._destinationFolder = value

    destinationFolder = property(get_destinationFolder, set_destinationFolder)

    def get_results(self):
        return self._results

    def set_results(self, value):
        self._results = value

    results = property(get_results, set_results)

    def openFileDiag(self, sender, e):
        self._results.Content = ''
        dialog = Microsoft.Win32.OpenFileDialog()
        dialog.DefaultExt = '.cl'
        dialog.Filter = 'CL Files (*.cl)|*.cl|ZIP Files (*.zip)|*.zip|All Files (*.*)|*.*'
        result = dialog.ShowDialog()

        if result:
            self._path.Text = dialog.FileName

    def openFolderDialog(self, sender, e):
        dialog = Forms.FolderBrowserDialog()
        result = dialog.ShowDialog()

        if result == Forms.DialogResult.OK:
            self._destinationFolder.Text = dialog.SelectedPath

    def done_message(self, sender, e):
        self._results.Content = 'Done!!!! Check the out put folder!'
        

    

if __name__ == '__main__':
    Application().Run(MyWindow())

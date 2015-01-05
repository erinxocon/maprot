import clr
clr.AddReference('System.Windows.Forms')
import wpf
import System
import Microsoft

from System.Windows import Application, Window, Forms

class MyWindow(Window):
    def __init__(self):
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

    def openFileDiag(self, sender, e):
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

    

if __name__ == '__main__':
    Application().Run(MyWindow())

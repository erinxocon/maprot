import wpf
import Microsoft

from System.Windows import Application, Window

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'MapRotator.xaml')

    def get_path(self):
        return self._path

    def set_path(self, value):
        self._path = value

    path = property(get_path, set_path)

    def openFileDiag(self, sender, e):
        dialog = Microsoft.Win32.OpenFileDialog()
        dialog.DefaultExt = '.cl'
        dialog.Filter = 'CL Files (*.cl)|*.cl|ZIP Files (*.zip)|*.zip|All Files (*.*)|*.*'
        result = dialog.ShowDialog()

        if result:
            self._path.Text = dialog.FileName
    

if __name__ == '__main__':
    Application().Run(MyWindow())

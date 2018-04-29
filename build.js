var electronInstaller = require('electron-winstaller');

resultPromise = electronInstaller.createWindowsInstaller({
    appDirectory: 'C:\\Users\\erin\\repos\\maprot\\maprotator3000-win32-x64\\',
    outputDirectory: 'C:\\Users\\erin\\repos\\maprot\\build',
    authors: "Erin O'Connell",
    exe: 'maprotator3000.exe',
    iconUrl: 'C:\\Users\\erin\\repos\\maprot\\rotate.ico'
});

resultPromise.then(() => console.log("It worked!"), (e) => console.log(`No dice: ${e.message}`));
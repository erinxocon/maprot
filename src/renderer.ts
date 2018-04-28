import { homedir } from "os";
import { ipcRenderer, remote, Event } from "electron";
// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

const form = document.querySelector('form');

const inputs = {
    source: form.querySelector('input[name="source"]'),
    destination: form.querySelector('input[name="destination"]'),
    name: form.querySelector('input[name="name"]'),
    angle: form.querySelector('input[name="angle"]'),
};

const buttons = {
    source: document.getElementById('chooseSource'),
    destination: document.getElementById('chooseDestination'),
    submit: form.querySelector('button[type="submit"]'),
};

ipcRenderer.on('processing-did-fail', (event: Electron.Event, error: any) => {
    console.error(error);
});

buttons.destination.addEventListener('click', () => {
    const dir = remote.dialog.showOpenDialog({
        properties: [
            'openDirectory',
            'createDirectory',
        ],
    });
    if (dir) {
        (inputs.destination as HTMLInputElement).value = dir[0];
    }
});

buttons.source.addEventListener('click', () => {
    const dir = remote.dialog.showOpenDialog({
        properties: [
            'openFile'
        ],
        filters: [
            { name: 'Content Library', extensions: ['cl'] },
            { name: 'All Files', extensions: ['*'] }
        ]
    });
    if (dir) {
        (inputs.source as HTMLInputElement).value = dir[0];
    }
});

form.addEventListener('submit', (event: Electron.Event) => {
    event.preventDefault();
    ipcRenderer.send('did-submit-form', {
        source: (inputs.source as HTMLInputElement).value,
        destination: (inputs.destination as HTMLInputElement).value,
        name: (inputs.name as HTMLInputElement).value,
        angle: (inputs.angle as HTMLInputElement).value,
    });
});

document.addEventListener('drop', (event: DragEvent) => {
    event.preventDefault();
    event.stopPropagation();
    const f = event.dataTransfer.files[0];
    (inputs.source as HTMLInputElement).value = f.path.split('.').reverse()[0] == 'cl' ? f.path : 'Please choose a content library file!';
});

document.addEventListener('dragover', (event: DragEvent) => {
    event.preventDefault();
    event.stopPropagation();
});

document.addEventListener('dragenter', (event: DragEvent) => {
    event.preventDefault();
    event.stopPropagation();
});

document.addEventListener('dragleave', (event: DragEvent) => {
    event.preventDefault();
    event.stopPropagation();
});
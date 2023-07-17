const {ipcRenderer, contextBridge} = require('electron')

// Exposed protected methods in the render process.
contextBridge.exposeInMainWorld(
    // Allowed 'ipcRenderer' methods.
    'ipcRenderer', {
        // From render to main.
        send: (channel, args) => {
            ipcRenderer.send(channel, args);
        },
        on: (channel, listener) => {
            // Show me the prototype (use DevTools in the render thread)
            // Deliberately strip event as it includes `sender`.
            ipcRenderer.on(channel, (event, ...args) => listener(...args));
        },
        // From main to render.
        once: (channel, listener) => {
            // Show me the prototype (use DevTools in the render thread)
            // Deliberately strip event as it includes `sender`.
            ipcRenderer.once(channel, (event, ...args) => listener(...args));
        },
        // From render to main and back again.
        invoke: (channel, args) => {
            return ipcRenderer.invoke(channel, args);
        }
    },
);


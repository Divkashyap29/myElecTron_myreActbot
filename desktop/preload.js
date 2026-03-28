const{ contextBridge, ipcRenderer} = require('electron');

contextBridge.exposeInMainWorld('kaashvi',{
    sendMessage:(msg)=>
        ipcRenderer.invoke('send-message',msg)
});


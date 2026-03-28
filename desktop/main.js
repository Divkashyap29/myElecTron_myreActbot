const{app,BrowserWindow,ipcMain}=require('electron');
const{spawn}=require('child_process');
const path = require('path')

function createWindow(){
    const win = new BrowserWindow({
        width:900,
        height:700,
        webPreferences:{
            preload: path.join(__dirname,'preload.js'),
            contextIsolation:true,
        }
    });
    win.loadFile('index.html');
}

app.whenReady().then(createWindow);

ipcMain.handle('send-message',async(event,userMessage)=>{
    return new Promise((resolve,reject)=>{
        const py = spawn('python',[path.join(__dirname,'..','main.py'),'--message',userMessage]);
        let output = '';
        py.stdout.on('data',data=>console.erroe('python error:', data.toString()));
        py.on('close',code=>{
            if(code==0)resolve(output.trimEnd());
            else reject(new Error('Agent process failed'));
        });
    });
});

const py = spawn('python',[path.join(__dirname,'..','main.py'),'--message',userMessage]);

let output='';
py.stdout.on('data',data=>{output += data.toString();});

py.stderr.on('data',data=> console.error('python error:',data.toString()));

py.on('close',code=>{ 
    if ( code === 0)resolve(output.trim());
    else reject(new Error('Agent process failed'));
});

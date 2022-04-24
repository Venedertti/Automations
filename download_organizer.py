from distutils import extension
from email.mime import audio
from pydoc import doc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os 
import json
from pathlib import Path

DOWNLOAD_PATH= str(os.path.join(Path.home(), "Downloads", 'teste'))

class MyHandler(FileSystemEventHandler):

    def __init__(self, ):
        self._downloadPath= DOWNLOAD_PATH
        
        # [ToDo] => Update list
        self._filmesExtensions= ['mp4', 'mkv', 'avi', 'wmv']
        self._execExtensions= ['exe', 'msi']
        self._imagesExtensions= ['png', 'jpeg', 'jpg', 'bmp', 'gif', 'tiff', 'psd', 'ai', 'indd', 'raw']
        self._audiosExtensions= ['mp3']
        self._docsExtensions= ['pdf', 'doc', 'txt', 'xls', 'xlsx', 'csv', 'odt', 'file']
        self._torrentExtensions= ['torrent']
        self._compactFoldersExternsions= ['rar', 'zip', '7z', 'tar', 'iso']
        self._programingExtensions= ['py', 'jar', 'java', 'war', 'html', 'css', 'js', 'c', 'sql']

    def onModified(self, event):
        for file in os.listdir(self._downloadPath):
            src= os.path.join(self._downloadPath, file)
            
            if not(file.endswith('newPath')):

                if not(os.path.isdir(src)):
                    fileNameSplited= file.split('.')
                    extension= str(fileNameSplited[1])
                else:
                    extension= 'folder'
                
                newPath= self.getFolderByExtension(extension)
                newSrc= os.path.join(newPath, file)

                os.rename(src, newSrc) # Move file

    def getFolderByExtension(self, extension:str):
        
        # Will be acessed in first conditional in Else
        filmesPath= os.path.join(self._downloadPath, 'Filmes/Series')
        execPath= os.path.join(self._downloadPath, 'Executaveis')
        imagePath= os.path.join(self._downloadPath, 'Imagens')
        audioPath= os.path.join(self._downloadPath, 'Audios')
        docPath= os.path.join(self._downloadPath, 'Documentos')
        torrentPath= os.path.join(self._downloadPath, 'Torrent')
        programmingPath= os.path.join(self._downloadPath, 'Programacao')
        compactFolderPath= os.path.join(self._downloadPath, 'Pasta-compactas')
        outrosPath= os.path.join(self._downloadPath, 'Outros')

        if extension in self._filmesExtensions:
            if not(Path.exists(filmesPath)):
                os.mkdir(filmesPath)

            return filmesPath

        elif extension in self._execExtensions:
            if not(Path.exists(execPath)):
                os.mkdir(execPath)

            return execPath

        elif extension in self._imagesExtensions:
            if not(Path.exists(imagePath)):
                os.mkdir(imagePath)

            return imagePath
        
        elif extension in self._audiosExtensions:
            if not(Path.exists(audio)):
                os.mkdir(audioPath)

            return audioPath

        elif extension in self._docsExtensions:
            if not(Path.exists(docPath)):
                os.mkdir(docPath)
            
            return docPath

        elif extension in self._torrentExtensions:
            if not(Path.exists(torrentPath)):
                os.mkdir(torrentPath)
                
            return torrentPath

        elif extension in self._compactFoldersExternsions:
            if not(Path.exists(compactFolderPath)):
                os.mkdir(compactFolderPath)
            
            return compactFolderPath

        elif extension in self._programingExtensions:
            if not(Path.exists(programmingPath)):
                os.mkdir(programmingPath)
        
        else:
            if extension == 'folder':
                print('FOLDER')
            else:
                if not(Path.exists(outrosPath)):
                    os.mkdir

eventHandler= MyHandler()
observer= Observer()
observer.schedule(event_handler= eventHandler, 
                path= str(DOWNLOAD_PATH),
                recursive= True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
from distutils import extension
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os 
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
        self._configFolders= ['Filmes-Series', 'Executaveis', 'Imagens', 'Audios', 'Documentos', 'Torrent', 'Programacao', 'Pastas', 'Outros']

    def on_created(self, event):
        return self.on_modified(event= event)

    def on_modified(self, event):
        # Sleep while file is downloading
        file_size = -1
        while file_size != os.path.getsize(event.src_path):
            file_size = os.path.getsize(event.src_path)
            time.sleep(1)

        # Start 
        for file in os.listdir(self._downloadPath):
            src= os.path.join(self._downloadPath, file)
            if not(file in self._configFolders):

                if not(os.path.isdir(src)):
                    fileNameSplited= file.split('.')
                    extension= str(fileNameSplited[1])
                else:
                    extension= self._getExtensionByFolder(folder= src)

                newPath= self._getFolderByExtension(extension)
                newSrc= os.path.join(newPath, file)

                self._moveFile(oldSrc= src, newSrc= newSrc)

    def _getFolderByExtension(self, extension:str):
        # Will return the folder to rename by extensions and create the sub-folders
        filmesPath= os.path.join(self._downloadPath, 'Filmes-Series')
        execPath= os.path.join(self._downloadPath, 'Executaveis')
        imagePath= os.path.join(self._downloadPath, 'Imagens')
        audioPath= os.path.join(self._downloadPath, 'Audios')
        docPath= os.path.join(self._downloadPath, 'Documentos')
        torrentPath= os.path.join(self._downloadPath, 'Torrent')
        programmingPath= os.path.join(self._downloadPath, 'Programacao')
        compactFolderPath= os.path.join(self._downloadPath, 'Pastas')
        outrosPath= os.path.join(self._downloadPath, 'Outros')

        if extension in self._filmesExtensions:
            if not(os.path.exists(filmesPath)):
                os.mkdir(filmesPath)

            return filmesPath

        elif extension in self._execExtensions:
            if not(os.path.exists(execPath)):
                os.mkdir(execPath)

            return execPath

        elif extension in self._imagesExtensions:
            if not(os.path.exists(imagePath)):
                os.mkdir(imagePath)

            return imagePath
        
        elif extension in self._audiosExtensions:
            if not(os.path.exists(audioPath)):
                os.mkdir(audioPath)

            return audioPath

        elif extension in self._docsExtensions:
            if not(os.path.exists(docPath)):
                os.mkdir(docPath)
            
            return docPath

        elif extension in self._torrentExtensions:
            if not(os.path.exists(torrentPath)):
                os.mkdir(torrentPath)
                
            return torrentPath

        elif extension in self._compactFoldersExternsions:
            if not(os.path.exists(compactFolderPath)):
                os.mkdir(compactFolderPath)
            
            return compactFolderPath

        elif extension in self._programingExtensions:
            if not(os.path.exists(programmingPath)):
                os.mkdir(programmingPath)

            return programmingPath

        else:
            if not(os.path.exists(outrosPath)):
                os.mkdir(outrosPath)

            return outrosPath

    def _getExtensionByFolder(self, folder:str):
        # Will verificate if is a Movie or a Programming File or Doc and return in that order and return a file formate 
        listFiles= os.listdir(folder)
        filmeFiles= list(filter(self._filterFilmeFiles, listFiles))
        docFiles= list(filter(self._filterDocFiles, listFiles))
        programingFiles= list(filter(self._filterProgrammingFiles, listFiles))

        if len(filmeFiles) > 0:
            return 'mp4'
        elif len(programingFiles) > 0:
            return 'py'
        elif len(docFiles) > 0:
            return 'pdf'
        else:
            return 'zip'

    def _filterProgrammingFiles(self, file:str):
        if(os.path.isdir(file)):
            return False
        
        fileSplited= file.split('.')
        extension= fileSplited[1]
        if file.lower() == 'src' or extension in self._programingExtensions:
            return True
        else:
            return False
    
    def _filterFilmeFiles(self, file:str):
        if(os.path.isdir(file)):
            return False
        
        fileSplited= file.split('.')
        extension= fileSplited[1]
        if extension in self._filmesExtensions:
            return True
        else:
            return False

    def _filterDocFiles(self, file:str):
        if(os.path.isdir(file)):
            return False
        
        fileSplited= file.split('.')
        extension= fileSplited[1]
        if extension in self._docsExtensions:
            return True
        else:
            return False

    def _moveFile(self, oldSrc:str, newSrc:str):
        if os.path.exists(newSrc):
            newSrcSplited= newSrc.split('.')
            newFileName= str(newSrcSplited[0])

            for i in range(999999):
                n= 1+i
                if os.path.isdir(newSrc):
                    newFileName+= ' - Copia ({})'.format(str(n))
                else:
                    extension= str(newSrcSplited[1])
                    newFileName+= ' - Copua ({}).{}'.format(str(n), extension)

                if not(os.path.exists(newFileName)):
                    break
            
            os.rename(oldSrc, newFileName)


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
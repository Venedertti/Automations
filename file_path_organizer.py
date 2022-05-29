'''
===> [Author]: Thiago Ramos de Oliveira
===> [Date]: 28/05/2022
===> [Version]: 0.3

==> [Funcionalities]:

The script will watch a path, if some file is created, moved of deleted on this path the observer 
will call "MyHandler" and the method "on_modified" will be called by Observer.

In method "on_modified" will be verified the extension of every file in the path and classify using 
the list extensions in "MyHandler" class.    

In rename process will be verified if the file name alerdy exists in his new src path. If exists will be added 
the " - COPIA({N})" in file name.

==> [Details]: 

This automation will watch a path that expecified in const WATCHED_PATH
change the const WATCHED_PATH using the func "os.path.join", not "/".

The logs of renames will be in path especifed in variable _logFilePath of MyHandle class.

More in: https://github.com/Venedertti
'''
import time
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

WATCHED_PATH= str(os.path.join(Path.home(), 'Downloads')) # The whatched path will be the 'Downloads'

class MyHandler(FileSystemEventHandler):

    def __init__(self, ):
        self._watchedPath= WATCHED_PATH
        self._logPath= str(os.path.join(Path.home(), 'Documents', 'Logs'))
        self._logFilePath=  str(os.path.join(self._logPath, 'log_path_organizer.txt'))

        # Extensions List:
        self._filmesExtensions= ['mp4', 'mkv', 'avi', 'wmv']
        self._execExtensions= ['exe', 'msi']
        self._imagesExtensions= ['png', 'jpeg', 'jpg', 'bmp', 'gif', 'tiff', 'psd', 'ai', 'indd', 'raw']
        self._audiosExtensions= ['mp3']
        self._docsExtensions= ['pdf', 'doc', 'txt', 'xls', 'xlsx', 'csv', 'odt', 'file']
        self._torrentExtensions= ['torrent']
        self._compactFoldersExternsions= ['rar', 'zip', '7z', 'tar', 'iso']
        self._programingExtensions= ['py', 'jar', 'java', 'war', 'html', 'css', 'js', 'c', 'sql']
        
        self._notAceptedFiles= ['.tmp', '.opdownload', '.parts']
        self._configFolders= ['Filmes-Series', 'Executaveis', 'Imagens', 'Audios', 'Documentos', 'Torrent', 'Programacao', 'Pastas', 'Outros']

        if not(os.path.exists(self._logPath)):
            os.mkdir(self._logPath)

    def on_created(self, event):
        return self.on_modified(event= event)

    def on_modified(self, event):

        if self.validateSrcFile(event.src_path): # -> .opdownload is for opera download before extension rename 
            # Start 
            for file in os.listdir(self._watchedPath):
                src= os.path.join(self._watchedPath, file)
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
        filmesPath= os.path.join(self._watchedPath, 'Filmes-Series')
        execPath= os.path.join(self._watchedPath, 'Executaveis')
        imagePath= os.path.join(self._watchedPath, 'Imagens')
        audioPath= os.path.join(self._watchedPath, 'Audios')
        docPath= os.path.join(self._watchedPath, 'Documentos')
        torrentPath= os.path.join(self._watchedPath, 'Torrent')
        programmingPath= os.path.join(self._watchedPath, 'Programacao')
        compactFolderPath= os.path.join(self._watchedPath, 'Pastas')
        outrosPath= os.path.join(self._watchedPath, 'Outros')

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
        lastIndex= len(fileSplited) - 1  if len(fileSplited) != 0 else 0 
        
        if lastIndex == 0:
            return False 

        extension= fileSplited[lastIndex]
        if file.lower() == 'src' or extension in self._programingExtensions:
            return True
        else:
            return False
    
    def _filterFilmeFiles(self, file:str):
        if(os.path.isdir(file)):
            return False
        
        fileSplited= file.split('.')
        lastIndex= len(fileSplited) - 1  if len(fileSplited) != 0 else 0 
        
        if lastIndex == 0:
            return False 

        extension= fileSplited[lastIndex]
        if extension in self._filmesExtensions:
            return True
        else:
            return False

    def _filterDocFiles(self, file:str):
        if(os.path.isdir(file)):
            return False
        
        fileSplited= file.split('.')
        lastIndex= len(fileSplited) - 1  if len(fileSplited) != 0 else 0 
        
        if lastIndex == 0:
            return False 

        extension= fileSplited[lastIndex]
        if extension in self._docsExtensions:
            return True
        else:
            return False

    def _moveFile(self, oldSrc:str, newSrc:str): 
        
        newSrcSplited= newSrc.split('.')
        newFileName= str(newSrcSplited[0])

        if os.path.exists(newSrc):
            for i in range(999999):
                n= 1+i
                if os.path.isdir(oldSrc):
                    newFileName+= ' - Copia ({})'.format(str(n))
                else:
                    extension= str(newSrcSplited[1])
                    newFileName+= ' - Copia ({}).{}'.format(str(n), extension)

                if not(os.path.exists(newFileName)):
                    newSrc= newFileName
                    break

        try:
            os.rename(oldSrc, newSrc)
            self.generateLog(oldSrc, newSrc, True)
        except OSError as e:
            self.generateLog(oldSrc, newSrc, False)
            
    def validateSrcFile(self, srcFile:str):
        for file in self._notAceptedFiles:
            if file in srcFile:
                return False
        
        return True

    def getLogFile(self, ):
        logFile = self._logFilePath
        if os.path.exists(logFile):
            return open(logFile, 'a')
        
        return open(logFile, 'w')
         
    def generateLog(self, oldSrc:str, newSrc:str, isSucess:bool):
        msgErro= '[ERRO] ==> Erro ao mover: '
        msgInfo= '[INFO] ==> Arquivo movido: '

        now= datetime.now()
        formatedNow= str(now.strftime('%d/%m/%Y %H:%M:%S'))
        msgSrc= '{} para {} as {}'.format(oldSrc, newSrc, formatedNow)

        file= self.getLogFile()
        try:
            if isSucess == True:
                file.write(msgInfo + msgSrc + '\n')
            else:
                file.write(msgErro + msgSrc + '\n')

        except OSError as err:
            print(str(err))
       
        finally:
            file.close()

    def getLogPathStr(self, ):
        return str(self._logFilePath)

eventHandler= MyHandler()
observer= Observer()
observer.schedule(event_handler= eventHandler, 
                path= WATCHED_PATH,
                recursive= True)
observer.start()

now= datetime.now()
formatedNow= str(now.strftime('%d/%m/%Y %H:%M:%S'))

print('[STARTED] ================= [File Organizer] =================\n')
print('[INFO] ==> Watching Path:..... ' + WATCHED_PATH)
print('[INFO] ==> Started at:........ ' + formatedNow) 
print('[INFO] ==> Log Path:.......... ' + eventHandler.getLogPathStr() + '\n')
print('> By: Thiago Ramos de Oliveira')
print('> See more in https://github.com/Venedertti')

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
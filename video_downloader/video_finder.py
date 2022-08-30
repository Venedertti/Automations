
import re
import os

import urllib.request as req
from bs4 import BeautifulSoup

from pathlib import Path
from pytube import YouTube
from HashMap import HashMap
from moviepy.editor import VideoFileClip

RANGE_VIDEO= 10
REGEX_ID= r'watch\?v=(\S{11})'
BASE_URL_YT= 'https://www.youtube.com'

DOWNLOAD_PATH= str(os.path.join(Path.home(), 'Downloads', 'VideoDownloader')) 
MUSIC_PATH= str(os.path.join(DOWNLOAD_PATH, 'Music')) 
VIDEO_PATH= str(os.path.join(DOWNLOAD_PATH, 'Videos'))

def main():
   
    print('\n[STARTED] =================================== [Video Downloader] ===================================')
    print('> [INFO] Path de downloads de musicas:...........' + MUSIC_PATH)
    print('> [INFO] Path de downloads de videos:............' + VIDEO_PATH)
    print('> By: Thiago Ramos de Oliveira')
    print('> https://github.com/Venedertti\n> ...')

    # > Get Info
    info= str(input('> Favor informar uma descrição do video: '))

    # > Find all videos
    returnList= findVideos(info= info)
    listVideos= returnList[0]
    hashVideos= findVideos(info= info)[1]

    # > Select a video
    urlVideo = selectVideo(listIds= listVideos, hashVideos= hashVideos)

    # > Select the mp4 will be converted in mp3
    isMp3Str= str(input('> Tecle "S" para converter o arquivo em musica: '))
    isMp3= isMp3Str.lower() == 's'
    
    # > Download video and convert if necessary
    download(urlVideo= urlVideo, isMp3= isMp3)

def createPaths():
  
    if not(os.path.exists(DOWNLOAD_PATH)):
        os.mkdir(DOWNLOAD_PATH)

    if not(os.path.exists(MUSIC_PATH)):
        os.mkdir(MUSIC_PATH)

    if not(os.path.exists(VIDEO_PATH)):
        os.mkdir(VIDEO_PATH)

def download(urlVideo:str, isMp3:bool):
    # > Create download path's if not exits
    createPaths()

    video= YouTube(url= urlVideo)
    stream= video.streams.get_highest_resolution()
    titleMp4= str(video.title) + '.mp4'
    titleMp3= str(video.title) + '.mp3'
        
    stream.download(output_path= VIDEO_PATH)
    print('> [INFO] => Feito download do arquivo {}'.format(titleMp4))

    if isMp3:
        isOk= True
        mp4FilePath= os.path.join(VIDEO_PATH, titleMp4)
        mp3FilePath= os.path.join(MUSIC_PATH, titleMp3)
        
        try:
            videoClip= VideoFileClip(mp4FilePath)
            audioClip= videoClip.audio
            audioClip.write_audiofile(mp3FilePath)

            videoClip.close()
            audioClip.close()

        except:
            isOk= False
            print('> [ERROR] => A conversão de mp4 para mp3 falhou. O arquivo mp4 será mantido.')

        if isOk:
            print('> [INFO] => Conversão feita com sucesso.')
            os.remove(mp4FilePath)

def findVideos(info:str):
    # Replacing all empty spaces for '+' and creating a seach url 
    infoForQuery= info.replace(' ', '+')
    url= BASE_URL_YT + '/results?search_query=' + infoForQuery

    # Get response and finding all videos ids by regex
    htmlResponse= req.urlopen(url= url)
    videoIds= re.findall(REGEX_ID, htmlResponse.read().decode())
    hashVideos= getTitle(videosIdsList= videoIds[:RANGE_VIDEO])

    # The quantity of videos loaded are defined in the contant RANGE_VIDEO
    returnList = [videoIds[:RANGE_VIDEO], hashVideos]
    return returnList

def selectVideo(listIds:list, hashVideos:HashMap):
    
    indexVideo= 0
    urlWatch= BASE_URL_YT = '/watch?v='

    # Print indexes / titles
    for i in range(1, RANGE_VIDEO):
        hashVideo= hashVideos.get(listIds[i])
        title= hashVideos.get(listIds[i]) if listIds[i] != '' else 'ERROR'
        print('[{}] => {}\n'.format(str(i), title))

    # Select video by index
    while True:
        indexVideo= int(input('[INFO] => Favor informar o index do video: '))
        if(indexVideo != 0 & indexVideo in range(RANGE_VIDEO)):
            return urlWatch + listIds[indexVideo]
        else:
            print('[INFO] => Index invalido.')

def getTitle(videosIdsList:list):
    
    videosAndTitlesHash:HashMap = HashMap()
    
    for id in videosIdsList:
       
        # Making request to find a title by tag <title> in response
        url= BASE_URL_YT + '/watch?v=' + id
        htmlResponse= req.urlopen(url= url)
        soup= BeautifulSoup(htmlResponse, 'html.parser')
        
        # Find title with tag and create a substr removing all tags
        titleTag= soup.find_all('title')
        title= titleTag[8 : int(len(titleTag) - 9)]

        videosAndTitlesHash.put(key= id, value= title)

    return videosAndTitlesHash

if __name__ == '__main__':
    main()
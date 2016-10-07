import os, sys, time
import urllib, urllib2
import urlparse
import re
import buggalo
import mechanize
import HTMLParser
from datetime import datetime

import xbmc, xbmcgui, xbmcaddon, xbmcplugin

CommonRootView = 50
FullWidthList = 51
ThumbnailView = 500
PictureWrapView = 510
PictureThumbView = 514
MediaListView2 = 503
MediaListView3 = 504

_url = sys.argv[0]
_handle = int(sys.argv[1])

__addon = xbmcaddon.Addon()
__addonname = __addon.getAddonInfo('name')
__icon = __addon.getAddonInfo('icon')

__addonpath = __addon.getAddonInfo('path').decode("utf-8")
__resource  = xbmc.translatePath(os.path.join(__addonpath, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")

__debug = __addon.getSetting('debug') == "true" 

sys.path.append(__resource)

import highlights

def showCredit():
  
    if __debug:
        xbmc.log('- credit -')   
   
    # user data                              
    login = xbmcplugin.getSetting(_handle, 'email')
    password = xbmcplugin.getSetting(_handle, 'pass')
    
    data = highlights.login(login, password)
    
    # to do checks
    if(data.state == 'premium'):
        xbmcgui.Dialog().ok('otrstream', __addon.getLocalizedString(30040) + ' ' + xbmcplugin.getSetting(_handle, 'email') ,
                                        __addon.getLocalizedString(30041) +  ' ' + data.state + ' - ' + data.decode,
                                        __addon.getLocalizedString(30042) + ' ' + data.value)
    else:
        xbmcgui.Dialog().ok('otrstream', __addon.getLocalizedString(30040) + ' ' + xbmcplugin.getSetting(_handle, 'email') ,
                                        __addon.getLocalizedString(30041) +  ' ' + data.state + ' - ' + data.decode,
                                        __addon.getLocalizedString(30042) + ' ' + data.value)

def mainSelector():

    if __debug:
        xbmc.log('- main selector -')
        
    xbmcplugin.setContent(_handle, 'files')  

    addPictureItem(__addon.getLocalizedString(30030), _url + '?actual=0', 'DefaultFolder.png')    # highlights
    addPictureItem(__addon.getLocalizedString(30034), _url + '?records=all', 'DefaultFolder.png') # meine aufnahmen
    addPictureItem(__addon.getLocalizedString(30035), _url + '?toplist=all', 'DefaultFolder.png') # top listen
    
    addPictureItem(__addon.getLocalizedString(30032), _url + '?genres=all', 'DefaultFolder.png')  # genres
    
    addPictureItem(__addon.getLocalizedString(30031), _url + '?search=now', 'DefaultFolder.png')  # suche
    addPictureItem(__addon.getLocalizedString(30037), _url + '?station=now', 'DefaultFolder.png')  # suche station
    
    str1 = __addon.getSetting('search1')
    str2 = __addon.getSetting('search2')
    str3 = __addon.getSetting('search3')
    
    if(str1 <>''):
        addPictureItem(__addon.getLocalizedString(30031) + ' : ' + str1, _url + '?search=' + str1 + '&page=1', 'DefaultFolder.png')
    if(str2 <>''):
        addPictureItem(__addon.getLocalizedString(30031) + ' : ' + str2, _url + '?search=' + str2 + '&page=1', 'DefaultFolder.png')
    if(str3 <>''):
        addPictureItem(__addon.getLocalizedString(30031) + ' : ' + str3, _url + '?search=' + str3 + '&page=1', 'DefaultFolder.png')
                         
    addPictureItem(__addon.getLocalizedString(30033), _url + '?credit=now', 'DefaultFolder.png')  # benutzer info
    
    xbmc.executebuiltin('Container.SetViewMode(%d)' % ThumbnailView)
    xbmcplugin.endOfDirectory(_handle)
    
def genresSelector():

    if __debug:
        xbmc.log('- genres selector -')
        
    xbmcplugin.setContent(_handle, 'files')  
    
    addPictureItem(__addon.getLocalizedString(30060), _url + '?search=group11&page=1', 'DefaultFolder.png') # Filme
    addPictureItem(__addon.getLocalizedString(30068), _url + '?search=group1&page=1', 'DefaultFolder.png')  # Sport
    addPictureItem(__addon.getLocalizedString(30062), _url + '?search=group2&page=1', 'DefaultFolder.png')  # Nachrichten
    addPictureItem(__addon.getLocalizedString(30070), _url + '?search=group12&page=1', 'DefaultFolder.png') # Kinder
    addPictureItem(__addon.getLocalizedString(30064), _url + '?search=group3&page=1', 'DefaultFolder.png')  # Doku
    addPictureItem(__addon.getLocalizedString(30065), _url + '?search=group4&page=1', 'DefaultFolder.png')  # Magazine
    addPictureItem(__addon.getLocalizedString(30066), _url + '?search=group5&page=1', 'DefaultFolder.png')  # Wissen
    addPictureItem(__addon.getLocalizedString(30069), _url + '?search=group6&page=1', 'DefaultFolder.png')  # Musik
    addPictureItem(__addon.getLocalizedString(30063), _url + '?search=group7&page=1', 'DefaultFolder.png')  # Comedy
    addPictureItem(__addon.getLocalizedString(30061), _url + '?search=group8&page=1', 'DefaultFolder.png')  # Serien
    addPictureItem(__addon.getLocalizedString(30067), _url + '?search=group9&page=1', 'DefaultFolder.png')  # Show
    
    addPictureItem(__addon.getLocalizedString(30071), _url + '?search=group10&page=1', 'DefaultFolder.png') # Erotic
     
    xbmc.executebuiltin('Container.SetViewMode(%d)' % ThumbnailView)
    xbmcplugin.endOfDirectory(_handle)
    
def toplistSelector():

    if __debug:
        xbmc.log('- toplist selector -')
        
    xbmcplugin.setContent(_handle, 'files')  
    
    addPictureItem(__addon.getLocalizedString(30055), _url + '?toplist=202&page=1', 'DefaultFolder.png') # blockbuster
    addPictureItem(__addon.getLocalizedString(30050), _url + '?toplist=105&page=1', 'DefaultFolder.png') # gestern
    addPictureItem(__addon.getLocalizedString(30051), _url + '?toplist=106&page=1', 'DefaultFolder.png') # wochenende
    addPictureItem(__addon.getLocalizedString(30052), _url + '?toplist=104&page=1', 'DefaultFolder.png') # 7 Tage
    addPictureItem(__addon.getLocalizedString(30053), _url + '?toplist=103&page=1', 'DefaultFolder.png') # 30 Tage
    addPictureItem(__addon.getLocalizedString(30054), _url + '?toplist=101&page=1', 'DefaultFolder.png') # des jahres     
     
    xbmc.executebuiltin('Container.SetViewMode(%d)' % ThumbnailView)
    xbmcplugin.endOfDirectory(_handle)

def showSelector(page):
    
    if __debug:
        xbmc.log('- selector - page ' + page)
        
    xbmcplugin.setContent(_handle, 'movies') 
     
    # user data                              
    login = xbmcplugin.getSetting(_handle, 'email')
    password = xbmcplugin.getSetting(_handle, 'pass')
 
    iPage = int(page)
 
    if(iPage < 2):
        hList = highlights.getData(login, password)
        
        addPictureItem(__addon.getLocalizedString(30020), _url + '?actual=2', 'DefaultFolder.png') 
        
    if(iPage > 1):
        hList = highlights.getMoreData(login, password, iPage)  
        
        no = iPage - 1
        addPictureItem(__addon.getLocalizedString(30021), _url + '?actual=' + str(no), 'DefaultFolder.png') 
        no = iPage + 1
        addPictureItem(__addon.getLocalizedString(30020), _url + '?actual=' + str(no), 'DefaultFolder.png') 
                   
    for aItem in hList:
        title= HTMLParser.HTMLParser().unescape(aItem.title)
        desc = HTMLParser.HTMLParser().unescape(aItem.text)
        url = aItem.url
        thumb = aItem.thumb
        addPictureItem2(title, _url + '?categories=%s' % url + '&title=%s' % title , thumb, desc) 
        
    xbmc.executebuiltin('Container.SetViewMode(%d)' % MediaListView2)
    xbmcplugin.endOfDirectory(_handle)
               
def showCategory(epg_id, iTitle):
     
    if __debug:
        xbmc.log('- category - ' + epg_id + " / " + iTitle) 
        
    xbmcplugin.setContent(_handle, 'movies')
      
    # user data                              
    login = xbmcplugin.getSetting(_handle, 'email')
    password = xbmcplugin.getSetting(_handle, 'pass')
    
    mList = highlights.getMovies(login,password, epg_id)
    for aItem in mList:
        title = aItem.title
        url = aItem.url
        price = aItem.price
        thumb = aItem.thumb
        
        if(title == 'Preview'):
            addPictureItem2(title, _url + '?preview=%s' % url + '&title=%s' % iTitle, thumb, aItem.desc)  
        else:
            para = url
            para = para.replace('"','')
            data = para.split(',')
            
            eid = data[0]
            rid = data[1]
            mode = data[2]
            
            url = _url + '?movie=%s' %  mode + '&eid=%s' %  eid + '&rid=%s' %  rid
            
            addPictureItem2(aItem.title + " / " + price, url, thumb, aItem.desc) 
        
    xbmc.executebuiltin('Container.SetViewMode(%d)' % MediaListView2)
    xbmcplugin.endOfDirectory(_handle) 
 
def showMovie(eid, rid, mode):
    
    add = xbmcaddon.Addon('plugin.video.otrstream') 
    
    user = add.getSetting('email')
    pw = add.getSetting('pass')
    warn = add.getSetting('warning')== "true"
    
    # continue ok
    ok = True
    
    if mode <> 'normal':
        xbmc.executebuiltin('Notification(Free-Stream,Praesentiert von: FernsehFee.de, 10000)')
    else:
        if(warn):
            ok = False    
            ok = xbmcgui.Dialog().yesno('otrstream', __addon.getLocalizedString(30014), __addon.getLocalizedString(30015) )
    
    if(ok or (not warn)):
        link = highlights.getPlayLink(user, pw, eid, rid, mode)
    else:
        link = None
    
    if link is not None:      
        xbmc.log('- movie - ' + link)   
        xbmc.Player().play(link)
    else:
        xbmc.log('- movie - not found')   
            
def showPreview(url, title):
    
    if __debug:
        xbmc.log('- preview - ' + title + " / " + url)   
        
    url = urllib.unquote(url).decode('utf8')
    
    if __debug:
        xbmc.log('Play preview ' + url)
    
    listitem =xbmcgui.ListItem (title)
    listitem.setInfo('video', {'Title': title })
    
    xbmc.Player().play(url, listitem) 
                           
def search():
    
    if __debug:
        xbmc.log('- search -')    
    
    # user data                              
    login = xbmcplugin.getSetting(_handle, 'email')
    password = xbmcplugin.getSetting(_handle, 'pass')
    
    keyboard = xbmc.Keyboard('', __addon.getLocalizedString(30031))
    keyboard.doModal()
        
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        
        if len(keyword) > 0: 
    
            xbmcplugin.setContent(_handle, 'movies') 
            
            addPictureItem(__addon.getLocalizedString(30020), _url + '?search=' + keyword + '&page=2', 'DefaultFolder.png') 
                      
            hList = highlights.search(login,password, keyword, '1')
            for aItem in hList:
                id = aItem.id
                title = aItem.title
                if len(aItem.serie) > 0:
                    desc = aItem.date + " " + aItem.time + " " + aItem.serie +  "-" + aItem.episode +  " " + aItem.desc
                else:
                    desc = aItem.date + " " + aItem.time + " " + aItem.desc
                thumb = aItem.thumb 
       
                addPictureItem3(title, _url + '?categories=%s' % id + '&title=%s' % title, thumb, desc, aItem.genre)
    
            xbmc.executebuiltin('Container.SetViewMode(%d)' % MediaListView3)
            
            xbmcplugin.endOfDirectory(_handle)

def searchStation():
    
    if __debug:
        xbmc.log('- search station -')    
    
    # user data                              
    login = xbmcplugin.getSetting(_handle, 'email')
    password = xbmcplugin.getSetting(_handle, 'pass')
    
    keyboard = xbmc.Keyboard('', __addon.getLocalizedString(30031))
    keyboard.doModal()
    
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
    
        station = ''
        date = ''
    
        keyboard = xbmc.Keyboard('', __addon.getLocalizedString(30036))
        keyboard.doModal()
        
        if (keyboard.isConfirmed()):
            station = keyboard.getText()
         
        now = datetime.strftime(datetime.now(),'%d.%m')  # %y')
           
        keyboard = xbmc.Keyboard(now, __addon.getLocalizedString(30038))
        keyboard.doModal()
        
        if (keyboard.isConfirmed()):
            date = keyboard.getText()
        
        if len(keyword) > 0: 
    
            xbmcplugin.setContent(_handle, 'movies') 
            
            #addPictureItem(__addon.getLocalizedString(30020), _url + '?station=' + station + '&page=2&keyword=' + keyword, 'DefaultFolder.png') 
                      
            hList = highlights.searchStation(login,password, keyword, station, date, '1')
            for aItem in hList:
                id = aItem.id
                title = aItem.title
                if len(aItem.serie) > 0:
                    desc = aItem.date + " " + aItem.time + " " + aItem.serie +  "-" + aItem.episode +  " " + aItem.desc
                else:
                    desc = aItem.date + " " + aItem.time + " " + aItem.desc
                thumb = aItem.thumb 
       
                addPictureItem3(title, _url + '?categories=%s' % id + '&title=%s' % title, thumb, desc, aItem.genre)
    
            xbmc.executebuiltin('Container.SetViewMode(%d)' % MediaListView3)
            
            xbmcplugin.endOfDirectory(_handle)

def searchPage(keyword, page, station=None):

    if __debug:
        xbmc.log('- search ' + keyword +' page ' + page + ' -')     
     
    # user data                              
    login = xbmcplugin.getSetting(_handle, 'email')
    password = xbmcplugin.getSetting(_handle, 'pass')
    
    xbmcplugin.setContent(_handle, 'movies') 
    
    iPage = int(page)
    
    if(iPage < 2):        
        addPictureItem(__addon.getLocalizedString(30020), _url + '?search=' + keyword + '&page=2', 'DefaultFolder.png') 
        
    if(iPage > 1):
        x = iPage - 1
        addPictureItem(__addon.getLocalizedString(30021), _url + '?search=' + keyword + '&page=' + str(x), 'DefaultFolder.png') 
        x = iPage + 1
        addPictureItem(__addon.getLocalizedString(30020), _url + '?search=' + keyword + '&page=' + str(x), 'DefaultFolder.png') 
                     
    hList = highlights.search(login,password, keyword, page)
    for aItem in hList:
        id = aItem.id
        title = aItem.title
        if len(aItem.serie) > 0:
            desc = aItem.date + ' ' + aItem.time + ' S' + aItem.serie +  '-E' + aItem.episode +  ' ' + aItem.desc
        else:
            desc = aItem.date + ' ' + aItem.time + ' ' + aItem.desc
        thumb = aItem.thumb 
       
        addPictureItem3(title, _url + '?categories=%s' % id + '&title=%s' % title, thumb, desc, aItem.genre)
    
    xbmc.executebuiltin('Container.SetViewMode(%d)' % MediaListView3)
    xbmcplugin.endOfDirectory(_handle)

def searchGroup(group , page):
    
    if __debug:
        xbmc.log('- searchgroup ' + group + ' - ' + page )  
    
    # user data                              
    login = xbmcplugin.getSetting(_handle, 'email')
    password = xbmcplugin.getSetting(_handle, 'pass')
    
    xbmcplugin.setContent(_handle, 'movies') 
    
    iPage = int(page)
    
    if(iPage < 2):        
        addPictureItem(__addon.getLocalizedString(30020), _url + '?search=' + group + '&page=2', 'DefaultFolder.png') 
        
    if(iPage > 1):
        x = iPage - 1
        addPictureItem(__addon.getLocalizedString(30021), _url + '?search=' + group + '&page=' + str(x), 'DefaultFolder.png') 
        x = iPage + 1
        addPictureItem(__addon.getLocalizedString(30020), _url + '?search=' + group + '&page=' + str(x), 'DefaultFolder.png') 
                 
    hList = highlights.searchGroup(login, password, group, page)
    
    for aItem in hList:
        id = aItem.id
        title = aItem.title
        if len(aItem.serie) > 0:
            desc = aItem.date + ' ' + aItem.time + ' S' + aItem.serie +  '-E' + aItem.episode +  ' ' + aItem.desc
        else:
            desc = aItem.date + ' ' + aItem.time + ' ' + aItem.desc
        thumb = aItem.thumb 
       
        addPictureItem3(title, _url + '?categories=%s' % id + '&title=%s' % title, thumb, desc, aItem.genre)
    
    xbmc.executebuiltin('Container.SetViewMode(%d)' % MediaListView3)
    xbmcplugin.endOfDirectory(_handle)

def showRecords(page):
    
    if __debug:
        xbmc.log('- records - ' + page)  
    
    # user data                              
    login = xbmcplugin.getSetting(_handle, 'email')
    password = xbmcplugin.getSetting(_handle, 'pass')
       
    xbmcplugin.setContent(_handle, 'movies') 
    
    iPage = int(page)
    
    if(iPage < 2):        
        addPictureItem(__addon.getLocalizedString(30020), _url + '?records=2', 'DefaultFolder.png') 
        
    if(iPage > 1):
        x = iPage - 1
        addPictureItem(__addon.getLocalizedString(30021), _url + '?records=' + str(x), 'DefaultFolder.png') 
        x = iPage + 1
        addPictureItem(__addon.getLocalizedString(30020), _url + '?records=' + str(x), 'DefaultFolder.png') 
         
    hList = highlights.getRecords(login, password, page)
    for aItem in hList:
        id = aItem.id
        title = aItem.title
        if len(aItem.serie) > 0:
            desc = aItem.date + ' ' + aItem.time + ' S' + aItem.serie +  '-E' + aItem.episode +  ' ' + aItem.desc
        else:
            desc = aItem.date + ' ' + aItem.time + ' ' + aItem.desc
        thumb = aItem.thumb 
       
        addPictureItem3(title, _url + '?categories=%s' % id + '&title=%s' % title, thumb, desc, aItem.genre)
    
    xbmc.executebuiltin('Container.SetViewMode(%d)' % MediaListView3)
    xbmcplugin.endOfDirectory(_handle)
    
def showToplist(no, page):
    
    if __debug:
        xbmc.log('- toplist ' + str(no) + "/ p." + str(page))  
    
    # user data                              
    login = xbmcplugin.getSetting(_handle, 'email')
    password = xbmcplugin.getSetting(_handle, 'pass')
       
    xbmcplugin.setContent(_handle, 'movies') 
    
    iPage = int(page)
    
    if(iPage < 2):        
        addPictureItem(__addon.getLocalizedString(30020), _url + '?toplist=' + no + '&page=2', 'DefaultFolder.png') 
        
    if(iPage > 1):
        x = iPage - 1
        addPictureItem(__addon.getLocalizedString(30021), _url + '?toplist=' + no + '&page=' + str(x), 'DefaultFolder.png') 
        x = iPage + 1
        addPictureItem(__addon.getLocalizedString(30020), _url + '?toplist=' + no + '&page=' + str(x), 'DefaultFolder.png') 
                 
    hList = highlights.getList(login, password, no, page)
    for aItem in hList:
        id = aItem.id
        title = aItem.title
        if len(aItem.serie) > 0:
            desc = aItem.date + ' ' + aItem.time + ' S' + aItem.serie +  '-E' + aItem.episode +  ' ' + aItem.desc
        else:
            desc = aItem.date + ' ' + aItem.time + ' ' + aItem.desc
        thumb = aItem.thumb 
       
        addPictureItem3(title, _url + '?categories=%s' % id + '&title=%s' % title, thumb, desc, aItem.genre)
    
    xbmc.executebuiltin('Container.SetViewMode(%d)' % MediaListView3)
    xbmcplugin.endOfDirectory(_handle)
 
 # --------------  helper -------------------

def addPictureItem(title, url, thumb):
    
    list_item = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
        
    list_item.setArt({'thumb': thumb,
                      'icon': thumb,
                      'fanart': thumb}) 
                
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
def addPictureItem2(title, url, thumb, desc):
    
    list_item = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
    list_item.addContextMenuItems([(__addon.getLocalizedString(30022), 'Action(ParentDir)'),
                                   (__addon.getLocalizedString(30023), 'XBMC.Container.Update(plugin://plugin.video.otrstream/?main=go)'),
                                   (__addon.getLocalizedString(30024), 'ActivateWindow(10000)')]) 
                                 
        
    list_item.setArt({'thumb': thumb,
                      'icon': thumb,
                      'fanart': thumb}) 
                
    list_item.setInfo('video', { 'plot': desc })
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)

def addPictureItem3(title, url, thumb, desc, genre):
    
    list_item = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
    list_item.addContextMenuItems([(__addon.getLocalizedString(30022), 'Action(ParentDir)'),
                                   (__addon.getLocalizedString(30023), 'XBMC.Container.Update(plugin://plugin.video.otrstream/?main=go)'),
                                   (__addon.getLocalizedString(30024), 'ActivateWindow(10000)')]) 
                                 
        
    list_item.setArt({'thumb': thumb,
                      'icon': thumb,
                      'fanart': thumb}) 
                
    list_item.setInfo('video', { 'plot': desc, 'genre': genre })
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
def addMovieItem(title, url, thumb):
    
    list_item = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
        
    list_item.setArt({'thumb': thumb,
                      'icon': thumb,
                      'fanart': thumb}) 
                
    xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
        

#### main entry point ####

if __name__ == '__main__':

    PARAMS = urlparse.parse_qs(sys.argv[2][1:])
    
try:    
  
    if PARAMS.has_key('categories'):
        showCategory(PARAMS['categories'][0], PARAMS['title'][0])
    elif PARAMS.has_key('movie'):
        showMovie(PARAMS['eid'][0], PARAMS['rid'][0], PARAMS['movie'][0])
    elif PARAMS.has_key('preview'):
        showPreview(PARAMS['preview'][0],PARAMS['title'][0])
    elif PARAMS.has_key('actual'):
        SHOW_CREDIT = False
        showSelector(PARAMS['actual'][0])
    elif PARAMS.has_key('search'):
        if (PARAMS['search'][0] == 'now'):
            search()
        elif (PARAMS['search'][0][:5] == 'group'):
            searchGroup(PARAMS['search'][0], PARAMS['page'][0])  
        else:
            searchPage(PARAMS['search'][0], PARAMS['page'][0])    
    elif PARAMS.has_key('station'):
        if (PARAMS['station'][0] == 'now'):
            searchStation()
    elif PARAMS.has_key('credit'):
        showCredit()
    elif PARAMS.has_key('genres'):
        genresSelector()
    elif PARAMS.has_key('records'):
        if (PARAMS['records'][0] == 'all'):
            showRecords('1')
        else:
            showRecords(PARAMS['records'][0])
    elif PARAMS.has_key('toplist'):
        if (PARAMS['toplist'][0] == 'all'):
            toplistSelector()
        else:
            showToplist( PARAMS['toplist'][0], PARAMS['page'][0])   
    elif PARAMS.has_key('main'):
        mainSelector()
    else:
        mainSelector() 
        
except Exception:
    buggalo.onExceptionRaised() 
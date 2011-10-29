from elementtree import ElementTree

import sys
import os
import urllib2

import xbmcgui
import xbmcaddon
import xbmcplugin

FEED_URL = "http://natholdet.lbi.dk/xmlfeed.php?feed=33556715"
IPAD_USERAGENT = "AppleCoreMedia/1.0.0.9A334 (iPad; U; CPU OS 5_0 like Mac OS X; en_us) Paros/3.2.13"

class NatholdetAddon(object):
    def listVideos(self):
        r = urllib2.Request(FEED_URL, headers = {'user-agent' : IPAD_USERAGENT})
        u = urllib2.urlopen(r)
        xml = u.read()
        u.close()

        doc = ElementTree.fromstring(xml)
        fanartImage = os.path.join(ADDON.getAddonInfo('path'), 'fanart.jpg')

        for clip in doc.find('.'):
            url = clip.findtext('url') + '|User-Agent=' + IPAD_USERAGENT
            image = clip.findtext('image') + '|User-Agent=' + IPAD_USERAGENT
            title = 'Natholdet - ' + clip.findtext('headline')
            item = xbmcgui.ListItem(title, iconImage = image, thumbnailImage = image)
            item.setProperty('Fanart_Image', fanartImage)
            item.setInfo(type = 'video', infoLabels = {
                'title' : clip.findtext('headline'),
                'duration' : clip.findtext('duration'),
                'plot' : clip.findtext('description'),
                'studio' : 'TV2',
                'cast' : ['Anders Breinholt']
            })

            xbmcplugin.addDirectoryItem(HANDLE, url, item)

        xbmcplugin.endOfDirectory(HANDLE)

if __name__ == '__main__':
    ADDON = xbmcaddon.Addon(id = 'plugin.video.natholdet')
    PATH = sys.argv[0]
    HANDLE = int(sys.argv[1])

    natholdet = NatholdetAddon()
    natholdet.listVideos()

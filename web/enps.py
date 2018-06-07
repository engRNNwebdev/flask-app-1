import xml.etree.ElementTree
from app import db
from models import *

def parseXML (xmlmsg):
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # create empty list for news items
    newsitems = []

    # iterate news items
    for item in root.findall('./roStorySend'):
        # empty news dictionary
        ids = {}
        # iterate child elements of item
        for child in item:
            if child.tag == child.attrib['storyBody']:
                
        for item in root.findall('./storyBody/storyItem'):
            # add mosAbstract objID
        idSend = MosObject(mosAbstract=child.attrib['mosAbstract'], objID=child.attrib['objID'], storySlug=child.attrib['storySlug'], roID=child.attrib['roID'], storyID=child.attrib['storyID'])
        db.session.add(idSend)


             # special checking for namespace object content:media
        #     if child.tag == '{http://search.yahoo.com/mrss/}content':
        #         news['media'] = child.attrib['url']
        #     else:
        #         news[child.tag] = child.text.encode('utf8')

        # append news dictionary to news items list
        # newsitems.append(news)
    db.session.commit()
    # return news items list
    return newsitems

import csv, requests, datetime, re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import urllib2, sys, re, base64, logging
from urlparse import urlparse
from models import *


def writeKalturaReq(jsonData):
    # create the file structure

    mrss = ET.Element('mrss')
    channel = ET.SubElement(mrss, 'channel')
    item = ET.SubElement(channel, 'item')
    action = ET.SubElement(item, 'action')
    type = ET.SubElement(item, 'type')
    userId = ET.SubElement(item, 'userId')
    name = ET.SubElement(item, 'name')
    description = ET.SubElement(item, 'description')
    tags1 = ET.SubElement(item, 'tags')
    tag1 = ET.SubElement(tags1, 'tag')
    tag2 = ET.SubElement(tags1, 'tag')
    media = ET.SubElement(item, 'media')
    mediaType = ET.SubElement(media, 'mediaType')
    contentAssets = ET.SubElement(item, 'contentAssets')
    content = ET.SubElement(contentAssets, 'content')
    dropFolderFileContentResource1 = ET.SubElement(content, 'dropFolderFileContentResource')
    subTitles = ET.SubElement(item, 'subTitles')
    subTitle = ET.SubElement(subTitles, 'subTitle')
    tags2 = ET.SubElement(subTitle, 'tags')
    tag3 = ET.SubElement(tags2, 'tag')
    dropFolderFileContentResource2 = ET.SubElement(subTitle, 'dropFolderFileContentResource')

    mrss.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
    mrss.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    mrss.set('xsi:noNamespaceSchemaLocation', 'ingestion.xsd')
    action.text = 'add'
    type.text = '1'
    userId.text = 'twissman'
    name.text = jsonData["mosID"]
    description.text = jsonData["slug"]
    tag1.text = 'Article'
    tag2.text = 'Creative'
    mediaType.text = '1'
    mpFour = jsonData["mosID"] + '.mp4'
    dropFolderFileContentResource1.set('filePath', mpFour)
    subTitle.set('isDefault', 'true')
    subTitle.set('format', '2')
    subTitle.set('label', 'English')
    subTitle.set('lang', 'English')
    tag3.text = 'test'
    captions = jsonData["mosID"] + '.vtt'
    dropFolderFileContentResource2.set('filePath', captions)

    # item1.set('name','item1')
    # item2.set('name','item2')
    # item1.text = 'item1abc'
    # item2.text = 'item2abc'

    # create a new XML file with the results
    logging.info('Write XML to be filed')
    logging.info('==========================')
    logging.info(channel)
    mydata = ET.tostring(channel)
    filePath = "/folderRNN/" + jsonData["mosID"] + ".xml"
    myfile = open(filePath, "w")
    myfile.write(mydata)

def ammendKalturaReq(jsonData, localFile):
    now = datetime.datetime.now()
    logging.getLogger().setLevel(logging.INFO)
    logging.info(now.strftime("%Y-%m-%d"))
    fileDate = now.strftime("%Y-%m-%d")
    caption = jsonData["mosID"] + "_" + fileDate + ".vtt"
    mpeg = jsonData["mosID"] + "_" + fileDate + ".mp4"
    # Parse the XML template
    pre = minidom.parse('variables.xml')
    logging.info(pre.toprettyxml())
    tree = ET.parse('variables.xml')
    root = tree.getroot()
    # FIND APPROPRIATE ELEMENTS
    logging.info("FIND APPROPRIATE ELEMENTS")
    channel = root.find('channel')
    item = channel.find('item')
    name = item.find('name')
    name.text = jsonData["mosID"]
    description = item.find('description')
    description.text = jsonData["description"]
    name.text = jsonData["slug"]
    contentAssets = item.find('contentAssets')
    content = contentAssets.find('content')
    subTitles = item.find('subTitles')
    subTitle = subTitles.find('subTitle')
    drop1 = content.find('dropFolderFileContentResource')
    drop1.set('filePath', mpeg)
    drop2 = subTitle.find('dropFolderFileContentResource')
    drop2.set('filePath', caption)
    # Write to new XML file
    if localFile == True:
        local = "local"
        logging.info("Local Download Initiated...")
        filePath = "/dropXML/" + local + "_" + jsonData["mosID"] + "_" + fileDate + ".xml"
    else:
        logging.info('Sending to Kaltura...')
        filePath = "/dropXML/" + jsonData["mosID"] + "_" + fileDate + ".xml"
    logging.info("Write to location: " + filePath)
    tree.write(filePath)
    post = minidom.parse(filePath)
    logging.info(post.toprettyxml())

def findBanner(description):
    logging.getLogger().setLevel(logging.INFO)
    logging.info(description)
    banner = ""
    if "[<mos><itemID>" in description and "</mosPayload></mosExternalMetadata></mos>]" in description:
        stripBan= description.strip()
        last = len(stripBan) - 1
        newBan = stripBan[1:last]
        logging.info("Read Banner: " + newBan)
        local_file = open('banner.xml', "wt")
        #Write to our local file
        local_file.write(newBan)
        local_file.close()
        tree = ET.parse('banner.xml')
        # get root element
        root = tree.getroot()
        # create empty list for MOS items
        elem = root.find('itemSlug').text
        match = elem.find('Banner:') + 7
        if match:
            banner += elem[match:]
        else:
            banner += ""
        logging.info(banner)
    elif len(description) < 255:
        banner += description
    return banner

def createWordPressCSV(slug, zone, author, mosID, banner, tags):
    logging.getLogger().setLevel(logging.INFO)
    now = datetime.datetime.now()
    theDate = now.strftime("%Y-%m-%d")
    with open('/wordpress/wordpress_posts.csv', mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow([slug, zone, author, banner, theDate, mosID, tags])


# ImmutableMultiDict([('objectMOS', u''),
# ('description', u''),
# ('slug', u''),
# ('zone', u'Generic'),
# ('tags', u'Regional News'), ('tags', u'National News'), ('tags', u'International News')])

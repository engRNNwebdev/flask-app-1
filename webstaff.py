import csv, requests, PyMediaRSS2Gen
import xml.etree.ElementTree as ET
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
    dropFolderFileContentResource2.set('filePath', 'HVH5ABRK3.vtt')

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


def writeRSS2(jsonData):
    mediaFeed = PyMediaRSS2Gen.MediaRSS2(
        title="A sample Media RSS Feed",
        link="https://github.com/wedi/PyMediaRSS2Gen/",
        description="Description for a feed with media elements"
    )
    mediaFeed.copyright = "Copyright (c) 2014 Foo Inc. All rights reserved."
    # mediaFeed.lastBuildDate = datetime.datetime.now()
    mediaFeed.items = [
        PyMediaRSS2Gen.MediaRSSItem(
            title="First item with media element",
            description="An image of foo attached in a media:content element",
            media_content=PyMediaRSS2Gen.MediaContent(
                url="http://example.com/assets/foo1.jpg",
                fileSize=123456,
                medium="image",
                width="480",
                height="640"
            )
        ),
        PyMediaRSS2Gen.MediaRSSItem(
            title="Second item with media element",
            description="A video with multiple resolutions",
            media_content=[
                PyMediaRSS2Gen.MediaContent(
                    url="http://example.com/assets/foo_HD.mp4",
                    fileSize=8765432,
                    type="video/mp4",
                    width="1920",
                    height="1080"
                ),
                PyMediaRSS2Gen.MediaContent(
                    url="http://example.com/assets/foo_SD.mp4",
                    fileSize=2345678,
                    type="video/mp4",
                    width="1280",
                    height="720"
                ),
            ]
        ),
        PyMediaRSS2Gen.MediaRSSItem(
            title="And an item with no media element at all",
            description="An image of foo attached in an media:content element",
            link="http://example.com/article/important-story.html"
        )
    ]
    mediaFeed.write_xml(open("rss2.xml", "w"))

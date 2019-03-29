import csv, requests
import xml.etree.ElementTree as ET
import urllib2, sys, re, base64, logging
from urlparse import urlparse
from app import db
from models import *

# class enpsModules:
#     def __init__:
#         self.url = os.getenv('URL')
#         self.user = os.getenv('ENPS_NAME')
#         self.api = os.getenv('API_NAME')
#         self.password = os.getenv('PASS_ENPS')
#         self.key = os.getenv('API_KEY')
#         self.db = os.getenv('DATABASE')
#     def login:
#         return loggedIn
#     def

def loadPolitics():
    username = 'WRNN_webfeeds'
    password = 'ap116'
    # url of rss feed
    theurl = 'http://syndication.ap.org/AP.Distro.Feed/GetFeed.aspx?idList=36169&idListType=packages&maxItems=15'
    # 'http://syndication.ap.org/AP.Distro.Feed/GetFeed.aspx?idList=36163&idListType=packagesmaxItems=15'
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
    passman.add_password(None, theurl, username, password)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which `theurl` is a super-url
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.
    f = urllib2.urlopen(theurl)
    # Open our local file for writing
    local_file = open('politics.xml', "wt")
	#Write to our local file
    local_file.write(f.read())
    local_file.close()
    # authentication is now handled automatically for us
    # saving the xml file
    # with open('topnewsfeed.xml', 'w') as f:
    #     f.write(pagehandle)

def loadNational():
    username = 'WRNN_webfeeds'
    password = 'ap116'
    # url of rss feed
    theurl = 'http://syndication.ap.org/AP.Distro.Feed/GetFeed.aspx?idList=36163&idListType=packages&maxItems=15'
    # 'http://syndication.ap.org/AP.Distro.Feed/GetFeed.aspx?idList=36163&idListType=packagesmaxItems=15'
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
    passman.add_password(None, theurl, username, password)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which `theurl` is a super-url
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.
    f = urllib2.urlopen(theurl)
    # Open our local file for writing
    local_file = open('national.xml', "wt")
	#Write to our local file
    local_file.write(f.read())
    local_file.close()
    # authentication is now handled automatically for us
    # saving the xml file
    # with open('topnewsfeed.xml', 'w') as f:
    #     f.write(pagehandle)

def headlines():
    tree1 = ET.parse('politics.xml')
    tree2 = ET.parse('national.xml')
    # get root element
    root1 = tree1.getroot()
    # create empty list for news items
    newsitems = []
    # iterate news items
    for Headline in root1.findall('./ContentMetadata'):
        # iterate child elements of item
        if child.tag == child.attrib['Headline']:
            print child.attrib['Headline']
            logging.info(child.attrib['Headline'])

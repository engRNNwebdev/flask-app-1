import urllib2, json

slicers = [{'id' : 'rnnuplynk1', 'port' : 65009, 'ip': '192.168.101.15'},{'id' : 'rnnuplynk2', 'port' : 65010, 'ip' : '192.1683.101.15'}]
# slicers = {u'_id': '52a347343be0b32a070e5f4f', u'optid': u'52a347343be0b32a070e5f4e'}


def content_start(portnum, title):
    SLICER_IP = "192.168.101.15"  # localhost

    SLICER_PORT = int(portnum)     # default port

    body = json.dumps({"title": title})
    request = urllib2.urlopen("http://%s:%d/content_start" % (SLICER_IP, SLICER_PORT), body)
    response = json.loads(request.read())
    assert response["error"] == 0

def blackout(portnum):
    SLICER_IP = "192.168.101.15"  # localhost
    SLICER_PORT = int(portnum)      # default port

    body = json.dumps({"start_timecode":"00:00:00:00"}) # timecode format HH:MM:SS:Frame
    request = urllib2.urlopen("http://%s:%d/blackout" % (SLICER_IP, SLICER_PORT), body)
    response = json.loads(request.read())
    assert response["error"] == 0

def state(slicer):
    assert response["error"] == 0

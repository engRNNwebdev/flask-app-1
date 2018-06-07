import urllib2, json

def content_start(portnum, external_id, title):
    SLICER_IP = "192.168.101.15"  # localhost

    SLICER_PORT = int(portnum)     # default port
    #{"start_timecode":"00:15:21:09","title":"Some Title","external_id":"asdf1234"}
    body = json.dumps({"title": title,"external_id":external_id})
    request = urllib2.urlopen("http://%s:%d/content_start" % (SLICER_IP, SLICER_PORT), body)
    response = json.loads(request.read())
    assert response["error"] == 0
    #return '%s has been set to capture on slicer %d' % (title,SLICER_PORT)

def blackout(portnum):
    SLICER_IP = "192.168.101.15"  # localhost
    SLICER_PORT = int(portnum)      # default port

    body = json.dumps({"start_timecode":"00:00:00:00"}) # timecode format HH:MM:SS:Frame
    request = urllib2.urlopen("http://%s:%d/blackout" % (SLICER_IP, SLICER_PORT), body)
    response = json.loads(request.read())
    assert response["error"] == 0
    #return '%s has been set to capture on slicer %d' % (title,SLICER_PORT)

def state(slicer):
    assert response["error"] == 0

import urllib2, json


def content_start(title):
    SLICER_IP = "192.168.101.15"  # localhost
    SLICER_PORT = 65009      # default port

    body = json.dumps({"title": title})
    request = urllib2.urlopen("http://%s:%d/content_start" % (SLICER_IP, SLICER_PORT), body)
    response = json.loads(request.read())
    assert response["error"] == 0

def blackout():
    SLICER_IP = "192.168.101.15"  # localhost
    SLICER_PORT = 65009      # default port

    body = json.dumps({"start_timecode":"00:00:00:00"}) # timecode format HH:MM:SS:Frame
    request = urllib2.urlopen("http://%s:%d/blackout" % (SLICER_IP, SLICER_PORT), body)
    response = json.loads(request.read())
    assert response["error"] == 0

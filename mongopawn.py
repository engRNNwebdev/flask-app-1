from pymongo import MongoClient
import datetime, pprint, sys

rnnuplynk1 = { "slicer_id" : "rnnuplynk1", "port" : 65009, "address": "192.168.101.15"}
rnnuplynk2 = { "slicer_id": "rnnuplynk2", "port" : 65011, "address" : "192.168.101.15"}
post = { "author": "Mongo",
         "text": "Mongo is just pawn in life",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow() }

def add_user():
    client.admin.authenticate('siteRootAdmin', 'Test123')
    client.testdb.add_user('newTestUser', 'Test123', roles=[{'role':'readWrite','db':'testdb'}])
    post_id = posts.insert_one(post).inserted_id
    sys.stderr.write(post_id)
    return post_id
def get_post():
    sys.stderr.write(db.command('usersInfo'))
    return db.command('usersInfo')

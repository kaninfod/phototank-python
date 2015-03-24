__author__ = 'hingem'


from pymongo import MongoClient
from bson.objectid import ObjectId



client = MongoClient('localhost', 27017)
db = client['phoman3']
imagesDB = db['images']
collectionsDB = db['collections']
albumsDB = db['albums']




def save_image(image):
    imgobject = {}

    for field in image.__mongo_attributes__():
        if not field == "db_id":
            imgobject[field] = getattr(image, field)

    imagesDB.update({"date_taken": image.db_date_taken}, {"$set": imgobject}, upsert=True)
    image.db_id = str(imagesDB.find(imgobject)[0]["_id"])


def get_image(id):

    record = imagesDB.find_one({'_id': ObjectId(id)})
    return record


def get_images_in_album(album):
        query_string = {}
        if album.tags_exclude or album.tags_include:
            query_string.update({
                '$and':[
                    {'db_tags':{'$in':album.tags_include}},
                    {'db_tags':{'$nin':album.tags_exclude}}
                ]})

        cursor = imagesDB.find(query_string, {"_id":1} )
        list_of_ids = [str(record['_id']) for record in cursor]

        album.image_count = len(list_of_ids)


        albumsDB.update({"_id": album.id}, {"$set": {"imagecount": album.image_count}}, upsert=False)
        return list_of_ids

def save_album(album):
        alb = {
            'tags_exclude': album.tags_exclude,
            'tags_include': album.tags_include,
            'image_count': album.image_count,
            'name': album.name
        }

        if album.id:
            albumsDB.update({'_id': ObjectId(album.id)}, {"$set": alb})
        else:
            album.id = str(albumsDB.insert(alb))

def get_album(album_id):
    record = albumsDB.find_one({"_id": ObjectId(album_id)})
    return record


def get_albums():
    return albumsDB.find()



def get_keywords():
    keywords = imagesDB.distinct('db_tags')
    keyword_list = [([x, y]) for x, y in zip(keywords, keywords)]

    return keyword_list
from bson.objectid import ObjectId
import datetime


class RestifyObject(object):

  id = None
  attrs = ['id']

  def __init__(self, pymongo_object):
    self._set_attrs(pymongo_object)

  def _set_attrs(self, pymongo_object):
    for key, value in pymongo_object.iteritems():
      if key == '_id':
        setattr(self, 'id', str(value))
      else:
        setattr(self, key, value)
        self.attrs.append(key)

  def to_dict(self):
    data = {}
    for attr in self.attrs:
      data[attr] = getattr(self, attr, '')
    return data

  @classmethod
  def create(cls, connection, database_name, collection_name, data):
    collection = connection[database_name][collection_name]
    data['createdAt'] = datetime.datetime.utcnow().isoformat()
    obj_id = collection.insert(data)
    obj = collection.find_one({'_id': obj_id})
    return cls(obj)

  @classmethod
  def get_by_id(cls, connection, database_name, collection_name, object_id):
    collection = connection[database_name][collection_name]
    obj = collection.find_one({'_id': ObjectId(object_id)})
    return cls(obj)

#!/usr/bin/python3
"""RESTful API actions"""
from models import storage


class API_rest():
    def read_all(cls):
        """Method for get all objects"""
        return (list(map(lambda state: state.to_dict(),
                         storage.all(cls).values())))

    def read_by_id(cls, id):
        """Method for get an object by its id"""
        read_object = storage.get(cls, id)
        if read_object:
            return {'status code': 200,
                    'object dict': read_object.to_dict()}
        else:
            return {'status code': 404}

    def delete(cls, id):
        """Method for delete an object"""
        object_delete = storage.get(cls, id)
        if object_delete:

            storage.delete(object_delete)
            storage.save()
            return {'status code': 200}
        else:
            return {'status code': 404}

    def create(obj):
        """Method for post a new object"""
        storage.new(obj)
        storage.save()
        return {'status code': 201, 'object dict': obj.to_dict()}

    def update(cls, state_id, ignored_arguments, date_from_request):
        """Method for put an object"""
        all_date_objects = storage.all(cls)
        arguments = dict(
            filter(lambda a: a[0] not in ignored_arguments, date_from_request.items()))

        if not all_date_objects.get(cls.__name__ + '.' + state_id):
            return {'status code': 404}

        for key, value in arguments.items():
            setattr(all_date_objects[cls.__name__ + '.' + state_id], key, value)
        all_date_objects[cls.__name__ + '.' + state_id].save()
        storage.reload()
        return {'status code': 200, 'object dict':
                all_date_objects[cls.__name__ + '.' + state_id].to_dict()}

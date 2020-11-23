import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user


item = Blueprint('items', 'item')

# current directory is this '/api/v1/resources
@item.route('/', methods=["GET"])
def get_all_items():
    try:
        items = [model_to_dict(item) for item in models.Item.select()]
        print(items)
        return jsonify(data=items, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@item.route('/mypage', methods=["GET"])
def get_my_items():
    try:
        items = [model_to_dict(item) for item in current_user.items]
        print(items)
        return jsonify(data=items, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# Create route
@item.route('/mypage/create', methods=["POST"])
def create_items():
    payload = request.get_json()

    print(type(payload), 'payload')

    new_item = models.Item.create(name=payload['name'], uploader=current_user.id, link=payload['link'],
    description=payload['description'], media_link=payload['media_link'])
    ## see the object
    print(item.__dict__)
    ## Look at all the methods
    print(dir(item))

    # Change the model to a dict
    item_dict = model_to_dict(new_item)
    return jsonify(data=item_dict, status={"code": 201, "message": "Success"})

# Show route
@item.route('/mypage/<id>', methods=['GET'])
def get_one_item(id):
    item = models.Item.get_by_id(id)
    print(item.__dict__)
    return jsonify(data=model_to_dict(item), status={"code": 200, "message": "Success"})

# Update route
@item.route('/mypage/<id>', methods=["PUT"])
def update_item(id):
    payload = request.get_json()
    print(payload)

    query = models.Item.update(**payload).where(models.Item.id==id)
    query.execute()
    item = model_to_dict(models.Item.get_by_id(id))
    return jsonify(data=item, status={"code": 200, "message": "Success"})

# Delete route
@item.route('/mypage/<id>', methods=["Delete"])
def delete_item(id):
    #delete item with id
    delete_query = query = models.Item.delete().where(models.Item.id==id)
    num_of_rows_deleted = delete_query.execute()
    print(num_of_rows_deleted)


    return jsonify(
    data={},
    message="Successfully deleted {} item with id {}".format(num_of_rows_deleted, id),
    status={"code": 200, "message": "Success"}
    )

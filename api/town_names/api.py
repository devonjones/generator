import json

from flask import Blueprint, Response, request

from town_names.commands.generate import generate_command
from town_names.commands.deconstruct import deconstruct_command
from town_names.commands.tags import tag_command
from town_names.utils import GeneralEncoder

town_names = Blueprint('town_names', __name__)

@town_names.route('/api/town_names/generate', methods=['GET'])
def generate_town_name():
    culture = request.args.get('culture')
    tags = request.args.getlist('tags')
    name = generate_command(tags, culture)
    result = {}
    result[str(name)] = name.description_data()
    return Response(json.dumps(result, indent=2, cls=GeneralEncoder),  mimetype='application/json')

@town_names.route('/api/town_names/deconstruct', methods=['GET'])
def deconstruct_town_name():
    namestr = request.args.get('name')
    name = deconstruct_command(namestr)
    result = {}
    result[str(name)] = name.description_data()
    return Response(json.dumps(result, indent=2, cls=GeneralEncoder),  mimetype='application/json')

@town_names.route('/api/town_names/tags', methods=['GET'])
def get_tags():
    return Response(json.dumps(tag_command(), indent=2),  mimetype='application/json')

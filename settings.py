SERVER_NAME = '127.0.0.1:5000'

# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
# MONGO_USERNAME = 'user'
# MONGO_PASSWORD = 'user'
MONGO_DBNAME = 'locoldb'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

events = {
    'schema': {
        # Schema definition, based on Cerberus grammar. Check the Cerberus project
        # (https://github.com/nicolaiarocci/cerberus) for details.
        'title': {
            'type': 'string'
        },
        'url': {
            'type': 'string'
        },
        'thumbnail_url': {
            'type': 'string'
        },
        'category': {
            'type': 'string'
        },
        'time': {
            'type': 'string'
        },
        'date': {
            'type': 'string'
        },
        'location': {
            'type': 'string'
        },
        'organizer': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'max_participants': {
            'type': 'string'
        },
    }
}

DOMAIN = {
    'events': events,
}

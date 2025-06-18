# examples/things.py

# Let's get this party started!
from wsgiref.simple_server import make_server

import falcon


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.status = falcon.HTTP_200  # This is the default status
        # resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.media = {
            'quote': 'Two things awe me most, the starry sky above me and the moral law within me.',
            'author':'Immanuel Kant'
        }


# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/things', things)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()
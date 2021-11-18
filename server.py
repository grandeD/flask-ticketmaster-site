from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TM_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY}

    #
    # - Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    if keyword:
        payload['keyword'] = keyword
    if postalcode:
        payload['postalCode'] = postalcode
    if radius:
        payload['radius'] = radius
    if unit:
        payload['unit'] = unit
    if sort:
        payload['sort'] = sort

    data = requests.get(url, params=payload).json()
    events = data['_embedded']['events']

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function
    # event_id = request.args.get("id")
    url = f'https://app.ticketmaster.com/discovery/v2/events/{id}'
    payload = {'apikey': API_KEY}
    sorted_data = {}

    data = requests.get(url, params=payload).json()
    sorted_data['name'] = data['name']
    sorted_data['url'] = data['url']
    sorted_data['image'] = data['images'][0]['url']
    sorted_data['description'] = data['info']
    sorted_data['start_date'] = data['dates']['start']['localDate']
    sorted_data['venues'] = data['_embedded']['venues']
    sorted_data['classifications'] = data['classifications']


    return render_template('event-details.html', data=sorted_data)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

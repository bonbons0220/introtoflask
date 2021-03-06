#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function, division, absolute_import
from flask import current_app, Blueprint, render_template, abort, g
from flask import session as current_session, request, redirect, url_for, jsonify
import numpy as np
from . import processRequest

# this is a Blueprint.  It helps you modularize your app.
example_page = Blueprint("example_page", __name__)


@example_page.route('/examples/')
def example():
    output = {}
    output['title'] = 'MyApp Examples'
    output['page'] = 'example'

    # Set some variable in g
    g.ra = 2345.456
    dothis()

    # thing to split in browser
    output['splitme'] = 'I-don"t-want-to-be-split-up!'

    # make some list data
    output['listdata'] = ['DOG', 'CAT', 'HORSE', 'PIG']

    # make some table data
    output['tabledata'] = {'head': ['A', 'B'], 'body': [(1, 4), (2, 5), (3, 6)]}

    return render_template('examples.html', **output)


# this function is called from the main example route, and can access the g
def dothis():
    ra = g.get('ra', None)
    print('I am a variable stored in g: ra', ra)


@example_page.route('/getrandomnumber/', methods=['POST'], endpoint='getrandom')
def getrandom():
    ''' Generates a Random Number

    This is function designed primarily with a handling an
    asynchronous javascript request from your browser.  It must
    return a JSON object

    Parameters:
        start (int): the starting value
        end (int): the ending value

    Returns:
        result (dict):
            A python dictionary containing parameters that has been
            turned into a JSON object with Jsonify
    '''
    result = {}
    result['number'] = None
    result['error'] = None
    result['status'] = -1

    # get any form parameters
    form = processRequest(request)
    start = form.get('start', None)
    end = form.get('end', None)

    # Generate a random number based on input
    if all([start, end]):
            result['number'] = np.random.randint(int(start), int(end))
    elif any([start, end]):
        result['error'] = 'Could not generate number!'
    else:
        result['number'] = np.random.random()

    # Check number and set status accordingly
    if result['number']:
        result['status'] = 1
    else:
        val = 'End' if start and not end else 'Start' if end and not start else None
        errmsg = '{0}ing number not specified'.format(val)
        result['error'] = '{0}: {1}'.format(result['error'], errmsg)

    # jsonify will take your contents and convert it to a JSON format using json.dumps
    # it accepts multiple args and kwargs, but I like to package things together
    return jsonify(result=result)


@example_page.route('/changesession/', methods=['POST'], endpoint='changesession')
def changesession():
    result = {}
    result['error'] = None
    result['status'] = -1

    # get any form parameters
    form = processRequest(request)
    active = form.get('isactive', None)

    # set the session variable
    if active == 'true':
        print('setting loadcat false')
        current_session['loadcat'] = False
    elif active == 'false':
        print('setting loadcat true')
        current_session['loadcat'] = True

    return jsonify(result=result)


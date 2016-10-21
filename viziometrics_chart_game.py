"""Methods for creating interactive elements of viziometrics_game"""

import random
import requests

import IPython.display
from IPython.display import display
from ipywidgets import widgets

import mixpanel


# module-level global variables - uncool, but simple
keywords = 'population health'
username = random.getrandbits(32)

def set_keywords(kwstr):
    """Set keywords for random figure selection"""
    global keywords
    
    assert kwstr != '', 'Keyword string may not be blank'
    keywords = kwstr

def set_user(username_str):
    """Set username for leader board (once I make one)"""
    global username
    
    assert username != '', 'Username may not be blank'
    username = username_str
    
def select_random_figure(keywords='population health'):
    """Returns a single random figure"""
    raw_results = requests.get('http://viziometrics.org/api/pmc/image/search/',
                     params=dict(keywords=keywords, number=200, qrandom=True))
    parsed_results = raw_results.json()
    
    # search through results to find an image that
    # viziometrics.org thinks is a visualization
    # and that has a caption of some substance
    for candidate_figure in parsed_results:
        if candidate_figure['class_name'] == 'visualization':
            if len(candidate_figure['caption']) >= 32:
                return candidate_figure
    raise Exception('no visualizations found for keywords "{}"'.format(keywords))

def describe_figure(r):
    """ Generate HTML to describe figure to player"""
    descr = ''
    descr += '<br/><b>Paper:</b> {}'.format(r['title'])
    descr += '<br/><b>Published:</b> {} ({})'.format(r['longname'], r['year_pub'])
    descr += '<br/><b>Figure:</b> {}'.format(r['caption'])
    return descr

def describe_and_show_figure(r):
    """ Generate HTML to describe and show figure to player"""
    s3_key = r['img_loc']
    img_url = 'http://s3-us-west-2.amazonaws.com/escience.washington.edu.viziometrics/{}'.format(s3_key)
    return describe_figure(r) + '<br/><img src="{}"/>'.format(img_url)

def play():
    global keywords
    
    # create button HBox widgets
    expect_buttons = []
    confirm_buttons = []
    for chart_type in ['Scatter', 'Line', 'Bar', 'Horizontal Bar', 'Pie', 'Other']:
        expect_buttons.append(widgets.Button(description=chart_type))
        confirm_buttons.append(widgets.Button(description=chart_type))

    # only include "Don't Know" button on expect activity, not on confirm
    expect_buttons.append(widgets.Button(description='Don\'t Know'))

    # glocal vars to capture state of game
    controls = None
    current_figure = None
    
    # connect expect buttons to "reveal" action
    def reveal_figure(b):
        global controls, current_figure
        controls.close()

        descr = describe_and_show_figure(current_figure)
        descr += '<br/><br/>Actual chart form:'
        controls = widgets.VBox([widgets.HTML(descr),
                                 widgets.HBox(confirm_buttons)])
        display(controls)

    for b in expect_buttons:
        b.on_click(reveal_figure)

    # connect confirm buttons to "new_question" action
    def new_question(b):
        global controls, current_figure, keywords
        controls.close()
        
        current_figure = select_random_figure(keywords)
        descr = describe_figure(current_figure)
        descr += '<br/><br/>Predicted chart form:'
        controls = widgets.VBox([widgets.HTML(descr),
                                 widgets.HBox(expect_buttons)])
        display(controls)
        
    for b in confirm_buttons:
        b.on_click(new_question)

    # start game with a new_question
    new_question(None)

"""Methods for creating interactive elements of viziometrics_game"""

import random
import time
import requests

import IPython.display
from IPython.display import display
from ipywidgets import widgets

import mixpanel

####################################################
# module-level global variables and related methods:
#    uncool, but simple
keywords = 'population health'
def set_keywords(kwstr):
    """Set keywords for random figure selection"""
    global keywords
    
    assert kwstr != '', 'Keyword string may not be blank'
    keywords = kwstr


username = random.getrandbits(32)
def set_user(username_str):
    """Set username for leader board (once I make one)"""
    global username
    
    assert username != '', 'Username may not be blank'
    username = username_str

    
controls = None
current_figure = {}


time_of_last_action = time.time()
def reset_timer():
    """a bit of a hack to measure time between events"""
    global time_of_last_action

    time_of_last_action = time.time()


PROJECT_TOKEN = 'c0428e0fd3f766df0613fa4c1ecb9257'
mp = mixpanel.Mixpanel(PROJECT_TOKEN)
def record_action(action, value):
    """send details of an action to mixpanel for future use"""
    props = {'value':value,
             'keywords': keywords,
             'time_to_action':time.time() - time_of_last_action}
    props.update(current_figure)
    mp.track(username, action, props)
    reset_timer()


#####################################
# more respectable methods start here
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
    global keywords, controls, current_figure
    
    # create button HBox widgets
    expect_buttons = []
    confirm_buttons = []
    for chart_type in ['Scatter', 'Line', 'Bar', 'Horizontal Bar', 'Pie', 'Other']:
        expect_buttons.append(widgets.Button(description=chart_type))
        confirm_buttons.append(widgets.Button(description=chart_type))

    # only include "Don't Know" button on expect activity, not on confirm
    expect_buttons.append(widgets.Button(description='Don\'t Know'))

    # connect expect buttons to "reveal" action
    def reveal_figure(b):
        global controls

        record_action('predict', b.description)
        controls.close()

        descr = describe_and_show_figure(current_figure)
        descr += '<br/><br/>Actual chart form:'
        controls = widgets.VBox([widgets.HTML(descr),
                                 widgets.HBox(confirm_buttons)])
        display(controls)

    for b in expect_buttons:
        b.on_click(reveal_figure)

    # connect confirm buttons to "new_question" action
    def new_question(b=None):
        global controls, current_figure

        if b != None:
            record_action('confirm', b.description)
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
    reset_timer()
    new_question()

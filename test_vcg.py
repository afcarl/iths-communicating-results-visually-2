"""Tests for methods in viziometrics_chart_game.py"""

import pytest
import viziometrics_chart_game as vcg

@pytest.fixture
def fig():
    r = vcg.select_random_figure(keywords='test')
    return r

def test_set_keyworks():
    new_words = 'test words'
    vcg.set_keywords(new_words)
    assert vcg.keywords == new_words

def test_set_user():
    new_name = 'tester'
    vcg.set_user(new_name)
    assert vcg.username == new_name

def test_select_random_figure():
    r = vcg.select_random_figure(keywords='test')

def test_describe_figure(fig):
    descr = vcg.describe_figure(fig)

def test_describe_and_show_figure(fig):
    descr = vcg.describe_and_show_figure(fig)

@pytest.skip
def test_play():
    # not really appropriate for unit tests---
    # how do you do functional testing for
    # ipywidgets?

    vcg.play()

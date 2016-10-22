FROM andrewosh/binder-base

MAINTAINER Abraham D Flaxman <abie@uw.edu>

USER root

# Install ipywidgets, seaborn, and mixpanel
# Also prepare the matplotlib font cache to speed initial setup up.
RUN conda install ipywidgets && \
    /home/main/anaconda2/envs/python3/bin/pip install seaborn mixpanel && \
    /home/main/anaconda2/envs/python3/bin/python -c "import matplotlib.pyplot"

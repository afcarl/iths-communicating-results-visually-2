FROM andrewosh/binder-base

MAINTAINER Abraham D Flaxman <abie@uw.edu>

USER root

# Install ipywidgets
# Also prepare the matplotlib font cache to speed initial setup up.
RUN conda install ipywidgets && \
    pip install seaborn mixpanel && \
    python -c "import matplotlib.pyplot"

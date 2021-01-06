import streamlit as st
from pesummary.io import read
import numpy as np
import altair as alt
import pandas as pd
import gwpy
from scipy import signal
import io
from scipy.io import wavfile
from copy import deepcopy

from pycbc.frame import read_frame
from pycbc.waveform import get_td_waveform
from pycbc.detector import Detector
import os
import base64

from gwosc import datasets
from peutils import *
import pesummary
from peutils import *


def get_params_intersect(sample_dict, chosenlist):
    allparams = set(sample_dict[chosenlist[0]].parameters)
    for event in sample_dict.keys():
        thisparam = set(sample_dict[event].parameters)
        allparams = allparams.intersection(thisparam)
    paramlist = list(allparams)
    paramlist.sort()
    return paramlist
        
def make_altair_plots(chosenlist):

    st.markdown("### Showing parameters for events:")
    for ev in chosenlist:
        if ev is None: continue
        st.markdown(ev)
        
    sample_dict = {}
    data_load_state = st.text('Loading data...')
    for i,chosen in enumerate(chosenlist, 1):
        data_load_state.text('Loading event ... {0}'.format(i))
        if chosen is None: continue
        samples = load_samples(chosen)
        sample_dict[chosen] = samples.samples_dict['PublicationSamples']

    data_load_state.text('Loading event ... done'.format(i))
    published_dict = pesummary.utils.samples_dict.MultiAnalysisSamplesDict( sample_dict )

    # -- Color list
    colorlist = ['blue', 'red', 'green']

    allparams = get_params_intersect(sample_dict, chosenlist)
    
    # -- Loop over parameters
    for param in allparams:

        st.markdown("#### {0}".format(param))
        
        chartlist = []
        for i,event in enumerate(chosenlist):

            if event is None: continue
            
            samples = sample_dict[event]

            # -- Make histogram
            value, bins = np.histogram(samples[param], bins=50, density=True)

            source = pd.DataFrame({
                param: bins[1:],
                'density': value,
                'Event': len(value)*[event]
            })
    
            chart = alt.Chart(source).mark_area(
                opacity=0.5,
                interpolate='step',
            ).encode(
                alt.X(param),
                alt.Y('density'),
                color='Event:N')

            chartlist.append(chart)

        allchart = chartlist[0]
        for chart in chartlist[1:]:
            allchart+=chart

        st.altair_chart(allchart, use_container_width=True)


    # unravel the histogram
    


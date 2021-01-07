import streamlit as st
import pesummary
from pesummary.io import read
from peutils import *
from makewaveform import make_waveform
from makealtair import make_altair_plots, get_params_intersect
from makeskymap import make_skymap

import matplotlib
matplotlib.use('Agg')

from matplotlib.backends.backend_agg import RendererAgg
lock = RendererAgg.lock


st.title('PE demo')

sectionnames = [
    '2-D posterior plot',
    '1-D posterior plots',
    'Waveform',
    'Skymaps'
]

def headerlabel(number):
    return "{0}".format(sectionnames[number-1])

page = st.radio('Select Section:', [1,2,3,4], format_func=headerlabel)
st.markdown("## {}".format(headerlabel(page)))

st.sidebar.markdown("### Select events")
eventlist = get_eventlist(catalog=['GWTC-2', 'GWTC-1-confident'],
                          optional=False)
ev1 = st.sidebar.selectbox('Event 1', eventlist)
eventlist2 = get_eventlist(catalog=['GWTC-2'], optional=True)
ev2 = st.sidebar.selectbox('Event 2', eventlist2)    
ev3 = st.sidebar.selectbox('Event 3', eventlist2)
chosenlist = [ev1, ev2, ev3]

if page == 1:

    st.markdown("### Making plots for events:")
    for ev in chosenlist:
        if ev is None: continue
        st.markdown(ev)
    
    sample_dict = {}
    data_load_state = st.text('Loading data...')
    for i,chosen in enumerate(chosenlist, 1):
        data_load_state.text('Loading event ... {0}'.format(i))
        if chosen is None: continue
        samples = load_samples(chosen)
        try:
            #-- GWTC-2
            sample_dict[chosen] = samples.samples_dict['PublicationSamples']
        except:
            #-- GWTC-1
            sample_dict[chosen] = samples.samples_dict
                
    data_load_state.text('Loading event ... done'.format(i))
    published_dict = pesummary.utils.samples_dict.MultiAnalysisSamplesDict( sample_dict )

    # -- Select parameters to plot
    st.markdown("## Select parameters to plot")
    params = get_params_intersect(sample_dict, chosenlist)

    try:
        indx1 = params.index('mass_1_source')
        indx2 = params.index('mass_2_source')
    except:
        indx1 = 0
        indx2 = 1
        
    param1 = st.selectbox( 'Parameter 1', params, index=indx1 )
    param2 = st.selectbox( 'Parameter 2', params, index=indx2 )

    # -- Make plot based on selected parameters
    st.markdown("### Triangle plot")
    ch_param = [param1, param2]
    with lock:
        fig = published_dict.plot(ch_param, type='reverse_triangle',
                                  grid=False)
        st.pyplot(fig[0])

    st.markdown("### {0}".format(param1))

    with lock:
        fig = published_dict.plot(param1, type='hist', kde=True)
        st.pyplot(fig)

    st.markdown("### {0}".format(param2))

    with lock:
        fig = published_dict.plot(param2, type='hist', kde=True)
        st.pyplot(fig)

if page == 2:    
    make_altair_plots(chosenlist)

if page == 3:
    st.markdown("### Making waveform for Event 1: {0}".format(ev1))
    make_waveform(ev1)

if page == 4:
    make_skymap(chosenlist)

st.markdown("## About this app")

st.markdown("""

This app displays data from LIGO, Virgo, and GEO downloaded from the Gravitational Wave Open Science Center at https://gw-openscience.org .

[See the code](https://github.com/jkanner/streamlit-pe-demo)
""")

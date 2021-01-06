from peutils import *
import streamlit as st

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = False

from matplotlib.backends.backend_agg import RendererAgg
lock = RendererAgg.lock


def make_skymap(chosenlist):

    for ev in chosenlist:

        if ev is None: continue
        
        st.markdown("### Skymap for {0}".format(ev))        
        data = load_samples(ev)
        with lock:
            fig = data.skymap['PublicationSamples'].plot(contour=[50, 90])
            st.pyplot(fig[0])
        

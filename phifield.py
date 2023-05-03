# Author: Anil Kunwar (03.05.2023 Wednesday)
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.title('Comparing magnitudes of bulk and interfacial properties numerically')
st.title('Scale Factors')
length_scale_input = st.number_input("Enter length scale (e.g. 1.0E+09 for m_to_nm) :", value=1.0E+09, format='%.2e', step=1.0E+09)
length_scale = length_scale_input  # convert length from one unit to another
energy_scale_input = st.number_input("Enter energy scale (e.g. 6.242E+18 for J_to_eV) :", value=6.242E+18, format='%.2e', step=1.0)
energy_scale = energy_scale_input  # convert energy from one unit to another
time_scale_input = st.number_input("Enter time scale (e.g. 1.0E+09 for s_to_ns) :", value=1.0E+09, format='%.2e', step=1.0E+09)
time_scale = time_scale_input  # convert time from one unit to another

###################################################################
##Factor for bulk free energy ###########
factor_bulk = energy_scale/length_scale**3
# uncomment the following to know the numerical value of the scale factor
#st.write(f"Scale Factor for Bulk Energy: {factor_bulk}")
##Factor for model parameter mu ###########
factor_mu = energy_scale/length_scale**3
#st.write(f"Scale Factor for Interface MU: {factor_mu}")
##Factor for model parameter kappa ###########
factor_kappa = energy_scale/length_scale
#st.write(f"Scale Factor for Interface KAPPA: {factor_kappa}")
##Factor for diffusion mobility ###########
factor_mobility = (length_scale)**5/(energy_scale*time_scale)
#st.write(f"Scale Factor for Mobility M: {factor_mobility}")
##Factor for interfacial mobility ###########
factor_interfmobility = (length_scale)**3/(energy_scale*time_scale)
#st.write(f"Scale Factor for Interfacial Mobility L: {factor_interfmobility}")
###################################################################
#st.title('Molar Volume in cm^3/mol')
#molar_vol_input = st.number_input("Enter molar volume (e.g. 16.29 cm3/mol) :", value=16.29, step=1.0)
#molar_volume = molar_vol_input*1.0E-06  # convert  cm3/mol to m3/mol
####################################################################
st.title('Enter Physical Quantities in SI Units')
####################################################################
# molar_vol_input = st.number_input("Enter molar volume (e.g. 16.29E-06 m3/mol) :", value=1e-6, format='%.18f', step=1e-6)
molar_vol_input = st.number_input("Enter molar volume (e.g. 16.29E-06 m^3/mol) :", value=1e-6, format='%.2e', step=1e-6)
molar_volume = molar_vol_input
kappa_input = st.number_input("Enter KAPPA (e.g. 1.0E-8 J/m) :", value=1e-8, format='%.2e', step=1e-8)
kappa = kappa_input
mu_input = st.number_input("Enter MU (e.g. 1.0E+8 J/m^3) :", value=1e+8, format='%.2e', step=1e+8)
mu = mu_input
mobility_M_input = st.number_input("Enter mobility M (e.g. 1.0E-19 m^5/Js) :", value=1e-19, format='%.2e', step=1e-19)
diffusion_mobility_M = mobility_M_input
interfmobility_L_input = st.number_input("Enter interfacial mobility L (e.g. 1.0E-03 m^3/Js) :", value=1e-03, format='%.2e', step=1e-03)
interfacial_mobility_L = interfmobility_L_input
####################################################################
st.title('Bulk free energies')
####################################################################
# Define the user-defined functions
def bulk_energy(x, xeq, a, b, c):
    y = (a * (x-xeq)**2 + b * (x-xeq) + c)
    st.write(f"Parabolic Fitted G in J/mol: y = {a}*(x-{xeq})^2 + {b}*(x-{xeq}) + {c}")
    return y
####################################################################
st.title('Scaled Values of Physical Quantities')
####################################################################
scaled_kappa = kappa*factor_kappa
st.write(f"KAPPA in scaled units: {scaled_kappa}")
scaled_mu = mu*factor_mu
st.write(f"MU in scaled units: {scaled_mu}")
scaled_diffusion_mobility_M=diffusion_mobility_M*factor_mobility
st.write(f"Diffusion mobility M  in scaled units: {scaled_diffusion_mobility_M}")
scaled_interfacial_mobility_L=interfacial_mobility_L*factor_interfmobility
st.write(f"Interfacial mobility L  in scaled units: {scaled_interfacial_mobility_L}")














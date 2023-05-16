# Author: Anil Kunwar (03.05.2023 Wednesday)
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import tensorflow as tf

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
st.write("The model parameters $\kappa$ and MU (hereafter called as $\lambda$) of the phase field models are expressed as  the functions of interface energy ($\sigma$) and diffuse interface width ($\delta$),i.e. $\kappa = 0.75 * \sigma \delta $ and $ \lambda  =  6 \sigma/ \delta$" )
# molar_vol_input = st.number_input("Enter molar volume (e.g. 16.29E-06 m3/mol) :", value=1e-6, format='%.18f', step=1e-6)
molar_vol_input = st.number_input("Enter molar volume V$_{molar}$ (e.g. 16.29E-06 m^3/mol) :", value=1e-6, format='%.2e', step=1e-6)
molar_volume = molar_vol_input
kappa_input = st.number_input("Enter $\kappa$ (e.g. 1.0E-8 J/m) :", value=1e-8, format='%.2e', step=1e-8)
kappa = kappa_input
mu_input = st.number_input("Enter $\lambda$ (e.g. 1.0E+8 J/m^3) :", value=1e+8, format='%.2e', step=1e+8)
mu = mu_input
mobility_M_input = st.number_input("Enter mobility M (e.g. 1.0E-19 m^5/Js) :", value=1e-19, format='%.2e', step=1e-19)
diffusion_mobility_M = mobility_M_input
interfmobility_L_input = st.number_input("Enter interfacial mobility L (e.g. 1.0E-03 m^3/Js) :", value=1e-03, format='%.2e', step=1e-03)
interfacial_mobility_L = interfmobility_L_input
####################################################################
st.title('Bulk free energies')
#st.write(f"WORK IN PROGRESS 04.05.2023 THURSDAY")
st.write(" The expression for Gibbs free energy of a phase i is given as a quadratic function: G$_i$ = N *[a$_{i}$(x-x$_{i,eq}$)$^{2}$ + b$_i$(x-x$_{i,eq}$) +c$_i$] J/mol. For three phase system i=1,2,3.")
st.write(f"For the free energy expression of phase i, the amplitude term (N) is the value 10$^n$ which multiplies all the terms of the expression.") 
# E.g. In G$_i$ = N*[a$_i$(x-x$_{ieq}$)$^2$+b$_i$(x-x$_{ieq}$)+c$_i$] J/mol")
st.sidebar.subheader('Amplitude Term N of Free Energy')
amplitude_input = st.sidebar.number_input("Enter the common term (N) indicating range of G (e.g. from 1.0E+04 J/mol to 1.0E+06 J/mol) :", value=1e+5, format='%.2e', step=1e+2)
gibbs_magnitude = amplitude_input
st.write(f"Slide the coefficients  a$_i$, b$_i$ and c$_i$  and the constant x$_{{i,eq}}$ at the sliders in the left side in order to make G$_i$  possess negative values")
#st.title('Bulk free energies')
####################################################################
# Define the user-defined functions
def phase1(x, xeq, a, b, c):
    y = gibbs_magnitude*(a * (x-xeq)**2 + b * (x-xeq) + c)
    st.write(f"Parabolic Fitted G (phase1) in J/mol: G_phase1 = {gibbs_magnitude}*({a}*(x-{xeq})$^2$ + {b}*(x-{xeq}) + {c})")
    return y

def phase2(x, xeq, a, b, c):
    y = gibbs_magnitude*(a * (x-xeq)**2 + b * (x-xeq) + c)
    st.write(f"Parabolic Fitted G (phase2) in J/mol: G_phase2 = {gibbs_magnitude}*({a}*(x-{xeq})$^2$ + {b}*(x-{xeq}) + {c})")
    return y
    
def phase3(x, xeq, a, b, c):
    y = gibbs_magnitude*(a * (x-xeq)**2 + b * (x-xeq) + c)
    st.write(f"Parabolic Fitted G (phase3) in J/mol: G_phase3 = {gibbs_magnitude}*({a}*(x-{xeq})$^2$ + {b}*(x-{xeq}) + {c})")
    return y

# Get user input for function parameters and colors
# the subscript and superscript are utilized in the labels of altair chart using VEGA-lite syntax
# e.g. phase_1 = phase\u2081, phase_2 = phase\u2082, phase_3 = phase\u2083
st.sidebar.subheader('phase\u2081')
# create number input widgets for min and max values
[a1min, a1max, a1step]  = [st.sidebar.number_input("a1min", value=0.01, format='%.2e'), st.sidebar.number_input("a1max", value=10.0, format='%.2e'), st.sidebar.number_input("a1step", value=0.1, format='%.2e')]
[b1min, b1max, b1step]  = [st.sidebar.number_input("b1min", value=0.01, format='%.2e'), st.sidebar.number_input("b1max", value=10.0, format='%.2e'), st.sidebar.number_input("b1step", value=0.1, format='%.2e')]
[c1min, c1max, c1step]  = [st.sidebar.number_input("c1min", value=0.01, format='%.2e'), st.sidebar.number_input("c1max", value=10.0, format='%.2e'), st.sidebar.number_input("c1step", value=0.1, format='%.2e')]

a1 = st.sidebar.slider('Select value for a1', min_value=a1min, max_value=a1max, step=a1step,  key='a1')
b1 = st.sidebar.slider('Select value for b1', min_value=b1min, max_value=b1max, step=b1step,   key='b1')
c1 = st.sidebar.slider('Select value for c1', min_value=c1min, max_value=c1max, step=c1step,   key='c1')
xeq1 = st.sidebar.slider('Select value for x1eq', 0.0, 1.0, 0.1,   key='xeq1')
color1 = st.sidebar.color_picker('Select color for phase one', '#ff5733', key='color1')

st.sidebar.subheader('phase\u2082')
[a2min, a2max, a2step]  = [st.sidebar.number_input("a2min", value=0.01, format='%.2e'), st.sidebar.number_input("a2max", value=10.0, format='%.2e'), st.sidebar.number_input("a2step", value=0.1, format='%.2e')]
[b2min, b2max, b2step]  = [st.sidebar.number_input("b2min", value=0.01, format='%.2e'), st.sidebar.number_input("b2max", value=10.0, format='%.2e'), st.sidebar.number_input("b2step", value=0.1, format='%.2e')]
[c2min, c2max, c2step]  = [st.sidebar.number_input("c2min", value=0.01, format='%.2e'), st.sidebar.number_input("c2max", value=10.0, format='%.2e'), st.sidebar.number_input("c2step", value=0.1, format='%.2e')]

a2 = st.sidebar.slider('Select value for a2', min_value=a2min, max_value=a2max, step=a2step,  key='a2')
b2 = st.sidebar.slider('Select value for b2', min_value=b2min, max_value=b2max, step=b2step,   key='b2')
c2 = st.sidebar.slider('Select value for c2', min_value=c2min, max_value=c2max, step=c2step,   key='c2')
xeq2 = st.sidebar.slider('Select value for xeq2', 0.0, 1.0, 0.1, key='xeq2')
color2 = st.sidebar.color_picker('Select color for phase two', '#338fff', key='color2')    
    
st.sidebar.subheader('phase\u2083')
[a3min, a3max, a3step]  = [st.sidebar.number_input("a3min", value=0.01, format='%.2e'), st.sidebar.number_input("a3max", value=10.0, format='%.2e'), st.sidebar.number_input("a3step", value=0.1, format='%.2e')]
[b3min, b3max, b3step]  = [st.sidebar.number_input("b3min", value=0.01, format='%.2e'), st.sidebar.number_input("b3max", value=10.0, format='%.2e'), st.sidebar.number_input("b3step", value=0.1, format='%.2e')]
[c3min, c3max, c3step]  = [st.sidebar.number_input("c3min", value=0.01, format='%.2e'), st.sidebar.number_input("c3max", value=10.0, format='%.2e'), st.sidebar.number_input("c3step", value=0.1, format='%.2e')]
a3 = st.sidebar.slider('Select value for a3', min_value=a3min, max_value=a3max, step=a3step,  key='a3')
b3 = st.sidebar.slider('Select value for b3', min_value=b3min, max_value=b3max, step=b3step,   key='b3')
c3 = st.sidebar.slider('Select value for c3', min_value=c3min, max_value=c3max, step=c3step,   key='c3')
xeq3 = st.sidebar.slider('Select value for xeq3', 0.0, 1.0, 0.1, key='xeq3')
color3 = st.sidebar.color_picker('Select color for phase three', '#000000', key='color3')     
 

# Generate x values for the functions
x = np.linspace(0, 1, 10)

# Evaluate the functions for the given parameters
y1 = phase1(x, xeq1, a1, b1, c1)
y2 = phase2(x, xeq2, a2, b2, c2)
y3 = phase3(x, xeq3, a3, b3, c3)

############J/mol###################################################
# Create a dataframe with x and y values for each function
df1 = pd.DataFrame({'x': x, 'y': y1})
df2 = pd.DataFrame({'x': x, 'y': y2})
df3 = pd.DataFrame({'x': x, 'y': y3})
df1['function'] = 'phase1'
df2['function'] = 'phase2'
df3['function'] = 'phase3'
df = pd.concat([df1, df2, df3], ignore_index=True)

# Set chart properties for both functions
chart1 = alt.Chart(df).mark_line().encode(
    x=alt.X('x', axis=alt.Axis(title='x', labelFontSize=20, titleFontSize=20)),
    y=alt.Y('y', axis=alt.Axis(format="0.1e", title='G (J/mol)', labelFontSize=20, titleFontSize=20)),
    color=alt.Color('function', scale=alt.Scale(domain=['phase1', 'phase2', 'phase3'], range=[color1, color2, color3]))
).properties(
    width=1400,
    height=800,
    title=alt.TitleParams(text="Gibbs free energy in J/mol", fontSize=20)
).configure_line(
    strokeWidth=5
).configure_legend(
    titleFontSize=25,
    labelFontSize=20,
)#.interactive()
##########################################################################
############J/m3##########################################################
y1=y1/molar_volume
y2=y2/molar_volume
y3=y3/molar_volume
# Create a dataframe with x and y values for each function
df1 = pd.DataFrame({'x': x, 'y': y1})
df2 = pd.DataFrame({'x': x, 'y': y2})
df3 = pd.DataFrame({'x': x, 'y': y3})
df1['function'] = 'phase1'
df2['function'] = 'phase2'
df3['function'] = 'phase3'
df = pd.concat([df1, df2, df3], ignore_index=True)

# Set chart properties for both functions
chart2 = alt.Chart(df).mark_line().encode(
    x=alt.X('x', axis=alt.Axis(title='x', labelFontSize=20, titleFontSize=20)),
    y=alt.Y('y', axis=alt.Axis(format="0.1e", title='f (J/m\u00B3)', labelFontSize=20, titleFontSize=20)),
    color=alt.Color('function', scale=alt.Scale(domain=['phase1', 'phase2', 'phase3'], range=[color1, color2, color3]))
).properties(
    width=1400,
    height=800,
    title=alt.TitleParams(text="Free energy density in J/m\u00B3", fontSize=20)
).configure_line(
    strokeWidth=5
).configure_legend(
    titleFontSize=25,
    labelFontSize=20,
)#.interactive()
##########################################################################
############scaled##########################################################
y1=y1*factor_bulk
y2=y2*factor_bulk
y3=y3*factor_bulk
# Create a dataframe with x and y values for each function
df1 = pd.DataFrame({'x': x, 'y': y1})
df2 = pd.DataFrame({'x': x, 'y': y2})
df3 = pd.DataFrame({'x': x, 'y': y3})
df1['function'] = 'phase1'
df2['function'] = 'phase2'
df3['function'] = 'phase3'
df = pd.concat([df1, df2, df3], ignore_index=True)

# Set chart properties for both functions
chart3 = alt.Chart(df).mark_line().encode(
    x=alt.X('x', axis=alt.Axis(title='x', labelFontSize=20, titleFontSize=20)),
    y=alt.Y('y', axis=alt.Axis(format="0.1e", title='fscaled', labelFontSize=20, titleFontSize=20)),
    color=alt.Color('function', scale=alt.Scale(domain=['phase1', 'phase2', 'phase3'], range=[color1, color2, color3]))
).properties(
    width=1400,
    height=800,
    title=alt.TitleParams(text="Free energy density in scaled units", fontSize=20)
).configure_line(
    strokeWidth=5
).configure_legend(
    titleFontSize=25,
    labelFontSize=20,
).interactive()
##########################################################################
# Draw the chart
st.altair_chart(chart1, use_container_width=True)
st.altair_chart(chart2, use_container_width=True)
st.altair_chart(chart3, use_container_width=True)
####################################################################
####################################################################
st.title('Scaled Values of Physical Quantities')
####################################################################
scaled_kappa = kappa*factor_kappa
st.write(f"$\kappa$ in scaled units: {scaled_kappa}")
scaled_mu = mu*factor_mu
st.write(f"$\lambda$ in scaled units: {scaled_mu}")
scaled_diffusion_mobility_M=diffusion_mobility_M*factor_mobility
st.write(f"Diffusion mobility M  in scaled units: {scaled_diffusion_mobility_M}")
scaled_interfacial_mobility_L=interfacial_mobility_L*factor_interfmobility
st.write(f"Interfacial mobility L  in scaled units: {scaled_interfacial_mobility_L}")

st.title('How to cite this content:')
st.write('If you use this calculator for your work, please cite:')
st.write('Kunwar, A., Yousefi, E., Zuo, X., Sun, Y., Seveno, D., Guo, M., & Moelans, N. (2022). Multi-phase field simulation of Al3Ni2 intermetallic growth at liquid Al/solid Ni interface using MD computed interfacial energies. International Journal of Mechanical Sciences, 215, 106930. https://doi.org/10.1016/j.ijmecsci.2021.106930')
    














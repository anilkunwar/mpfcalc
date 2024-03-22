import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def sigmoid(theta, c):
    return 1 / (1 + np.exp(-theta * (2 * c - 1)))

def main():
    st.title('Interpolation function for material properties dependent on phase composition')
    thetas = []
    chosen_colors = []  # Store chosen colors
    color_map = ['#FF5733', '#33FF57', '#3366FF', '#FF33FF', '#000000']  # A list of distinct colors
    for i in range(5):
        #theta_default = 5 + 5 * i
        theta_default = 5 + 5 * i if i < 4 else 10 * (i+1)  # Increment by 5 for the first 4, by 10 for the last one
        theta = st.sidebar.slider(f'$\\theta_{i+1}$', min_value=0, max_value=100, value=theta_default)
        thetas.append(theta)
        color = st.sidebar.color_picker(f'Choose Color for $\\theta_{i+1}$', value=color_map[i])
        chosen_colors.append(color)  # Save chosen color

    c_values = np.linspace(0, 1, 100)

    fig, ax = plt.subplots(figsize=(6, 5))
    for i, (theta, color) in enumerate(zip(thetas, chosen_colors)):
        h_values = sigmoid(theta, c_values)
        ax.plot(c_values, h_values, label=f'$\\theta_{i+1}$ = {theta}', color=color, linewidth=4)

    ax.set_xlabel('$c$', fontsize=25)
    ax.set_ylabel('$h$', fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=20, width=5.0, size=8)
    ax.legend(fontsize=16)
    ax.grid(True, linestyle='--', linewidth=1.0)
    ax.spines['top'].set_linewidth(4)
    ax.spines['right'].set_linewidth(4)
    ax.spines['bottom'].set_linewidth(4)
    ax.spines['left'].set_linewidth(4)

    st.pyplot(fig)
    
    st.write("### Description:")
    st.write("The sigmoidal interpolation function is given by:")
    st.latex(r'h = \frac{1}{1 + e^{-\theta(2c-1)}}')
    st.write("where, c is the mole fraction of Cr in the alloy phase. ")
    st.write("The term  $\\theta(2c-1)$ is the weighted activation or input to the sigmoidal function.")
    st.write("The constant  $\\theta > 0$ is the weighted parameter controlling/modulating the steepness of the sigmoidal function for a given input feature c.")
    st.write("The mole fraction of Cr is the input feature to the sigmoidal function.")
    
    #c_values = np.linspace(0, 1, 20)
    # more data points in the range 0.4-0.6
    dense_c_values = np.concatenate([np.linspace(0, 0.4, 5),
                                     np.linspace(0.4, 0.6, 11),
                                     np.linspace(0.6, 1, 5)])  # More dense points between 0.4 and 0.6
    c_values = np.unique(dense_c_values)  # Unique values to avoid duplicates

    # Calculate h values for each c value
    #h_values = {}
    #h_values['c'] = c_values  # First column represents concentration c
    #for i, theta in enumerate(thetas):
        #h_values[f'$\\theta_{i+1}$'] = sigmoid(theta, c_values)
        #h_values[theta] = sigmoid(theta, c_values)
        #col_name = f'h({theta},c)' if i != 0 else 'c'  # Set custom column names
        #h_values[col_name] = sigmoid(theta, c_values)
        #if i == 0:
        #    col_name = 'c'  # First column represents c values
        #else:
        #    col_name = f'h({theta},c)'  # Sigmoidal function values for each theta
        #h_values[col_name] = sigmoid(theta, c_values)
        #col_name = f'h({theta},c)'  # Sigmoidal function values for each theta
        #h_values[col_name] = sigmoid(theta, c_values)
        

    # Create DataFrame for table
    #df = pd.DataFrame(h_values, index=c_values)
    # Calculate h values for each c value
    h_values = {'c': c_values}
    for i, theta in enumerate(thetas):
        col_name = f'h({theta},c)'  # Sigmoidal function values for each theta
        h_values[col_name] = sigmoid(theta, c_values)

    # Create DataFrame for table
    df = pd.DataFrame(h_values)

    # Set 'c' as the index
    df.set_index('c', inplace=True)
    

    # Display table
    st.write("### Table of  $h (\\theta,c)$ for given $c$")
    st.write(df)
    
    # Allow user to download CSV
    csv = df.to_csv().encode('utf-8')
    st.download_button(label='Download CSV', data=csv, file_name='interpolation_function.csv', mime='text/csv')
    
    # How to cite this work
    st.write("### How to Cite This Work:")
    st.markdown("""
    If you find this work useful, please cite the following paper:

    ```
    Subedi, U., Moelans, N., Tański, T., & Kunwar, A. (2024). Rapid portabilization  
    of elasto-chemical evolution data for dental Ti-Cr alloy microstructure through
    sparsification and tensor computation. Scripta Materialia, 244, 116027. 
    DOI: https://doi.org/10.1016/j.scriptamat.2024.116027"
   
    ```
    """)


if __name__ == '__main__':
    main()


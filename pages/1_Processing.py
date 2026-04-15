import streamlit as st
import patoolib
import os # to use os.walk 
import yaml # to use yaml.safe_Load fun 
import pandas as pd # to use data cleaning
from pathlib import Path


def yaml_to_dataframe(root_directory):
    all_data = []

    # Using for loop to walk through the "data" directory
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r') as f:
                        # Use safe_load to avoid executing arbitrary code
                        data = yaml.safe_load(f)
                        
                        if isinstance(data, dict):
                            # Optional: add metadata to track source file
                            data['_filename'] = file
                            all_data.append(data)
                        elif isinstance(data, list):
                            # Extend list if the YAML file itself contains a list of records
                            all_data.extend(data)
                            
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Create the DataFrame from the collected list of dictionaries
    return pd.DataFrame(all_data)

def extract_rar(source_path,destination_folder):
    # 1. Get the current working directory
    current_path = Path.cwd()
    st.success(f"Current Path: {current_path}")
    
    destination_folder = current_path / "data" # defining destination folder
    st.success(f"destination folder Path: {destination_folder}")

    print(destination_folder)

    # patool will handle finding the right backend tool for you
    patoolib.extract_archive(source_path, outdir=destination_folder) # extracts rar file to data folder
 

def generate_ticker_csv_files(df):
    # Assuming your dataframe is named 'stockpricedfdf'
    # Create a folder to store the output files if it doesn't exist
    output_dir = 'ticker_data'
    os.makedirs(output_dir, exist_ok=True)

    # Group by the 'Ticker' column and save each group
    for ticker, data in df.groupby('Ticker'):
        # Clean ticker name for filename (remove special characters if necessary)
        filename = f"{ticker}.csv"
        filepath = os.path.join(output_dir, filename)
        
        # Save to CSV (index=False avoids adding the row numbers to the file)
        data.to_csv(filepath, index=False)
    

# --- THE LOAD BUTTON ---
if st.button('🚀 Load & Analyze Market Data'):
    
    with st.spinner('Wait for it...'):  
        
        
        current_path = Path.cwd() # current working directory
        source_path = "data.rar" # assigning the source file name
        destination_folder = current_path / "data" # defining destination folder
        
        #Extract the rar file
        extract_rar(source_path,destination_folder) 
        st.success("data successfully extracted from the data.rar")
                
        
        target_folder = 'data'
        #Extracting the yaml files in the data folder to the dataframe
        stockpricedf = yaml_to_dataframe(target_folder)
        st.success("The files were moved from data folders to a Dataframe")
        
        #Saving the dataframe to the FullData.csv file
        stockpricedf.to_csv("FullData.csv")

        #Generate the ticker csv files
        generate_ticker_csv_files(stockpricedf)
        st.success(f"Saved the csv files in the ticker_data folder ...")


        # Display the first few rows
        st.dataframe(stockpricedf.head())
        
        
    
    st.success('Done!')

    
    
    





 
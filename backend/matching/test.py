import os
import pandas as pd

def combine_csvs_from_directory(directory_path):
    # List all CSV files in the directory
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    
    # Read each CSV into a DataFrame and store in a list
    dataframes = []
    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_path)
        dataframes.append(df)
        print(f"Loaded {file} with shape {df.shape}")
    
    # Concatenate all DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)
    print(f"Combined DataFrame shape: {combined_df.shape}")
    
    return combined_df

# Example usage
if __name__ == "__main__":
    # Replace with your folder path
    folder_path = "/Users/cam/Downloads/archive(5)/csv/"
    combined = combine_csvs_from_directory(folder_path)
    
    # Optional: Save to a new CSV
    combined.to_csv("combined_output.csv", index=False)
    print("Saved combined CSV as 'combined_output.csv'")

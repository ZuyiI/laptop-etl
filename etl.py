import pandas as pd
import transform  # Import transformation functions

# EXTRACT
def extract(file_path):
    """Extracts data from a CSV file into a Pandas DataFrame."""
    df = pd.read_csv(file_path)
    return df

# TRANSFORM
def transform_data(df):
    """Applies transformation functions from transform.py to clean and structure the dataset."""
    df = transform.drop_rows(df)    # Remove rows with missing or invalid values
    df = transform.convert_inches_float(df) # Convert screen size from string to float
    df = transform.ram_standardized(df) # Standardize RAM values by removing "GB" and converting to integer
    df = transform.weight_standardized(df)  # Standardize weight by removing "kg" and converting to float
    df = transform.split_screen_resolution(df)  # Split screen resolution into resolution, and screen_features columns
    df = transform.split_memory(df) # Split memory into memory_size and memory_type
    df = transform.drop_unnamed(df) # Remove unnecessary index column from import
    df = transform.reset_index(df)  # Reset index to ensure it remains sequential after dropping rows
    return df

# LOAD
def load(df, output_file):
    """Loads the cleaned DataFrame into a CSV file."""
    df.to_csv(output_file, index=False)

# EXECUTION OF ETL PIPELINE
def main():
    """Main ETL pipeline execution."""
    input_file = "laptopData.csv"
    output_file = "processed_laptopData.csv"
    
    print("Extracting data...")
    df = extract(input_file)    # Load raw data
    
    print("Transforming data...")
    df = transform_data(df) # Apply transformation functions
    
    print("Loading data...")
    load(df, output_file)   # Save transformed data
    
    print("ETL process completed successfully!")

if __name__ == "__main__":
    main()




# laptop-etl

# Introduction

The ETL process focuses on the preprocessing of a dataset containing over 1,300 laptop product listings from a client's e-commerce platform (sourced via Kaggle).

# Dataset

The source dataset (`laptopData.csv`) includes listings with attributes like brand, type, screen size, resolution, CPU, RAM, storage (memory), GPU, OS, weight, and price (in Rupees). The raw data contains inconsistencies (e.g., units mixed with values like '8GB', '1.2kg'), combined fields (ScreenResolution, Memory), missing values (represented as '?' or NaN), and requires cleaning before analysis.

# ETL Pipeline and Preprocessing Steps

An ETL (Extract, Transform, Load) pipeline was implemented using Python and pandas.

1.  **Extract:** Reads the raw `laptopData.csv` file.
2.  **Transform:** Applies a series of cleaning and structuring functions:
    * `drop_rows`: Removes rows that are entirely empty or contain '?' in any column.
    * `convert_inches_float`: Converts the `Inches` column to numeric float type and renames it to `screen_size_inches`.
    * `ram_standardized`: Removes "GB" from the `Ram` column, converts it to integer type, and renames it to `ram_gb`.
    * `weight_standardized`: Removes "kg" from the `Weight` column, converts it to float type, and renames it to `weight_kg`.
    * `split_screen_resolution`: Parses the `ScreenResolution` column into two new columns: `screen_features` (e.g., "Full HD", "Touchscreen", filling blanks with "No further details") and `screen_resolution` (e.g., "1920x1080"). The original column is dropped.
    * `split_memory`: Parses the complex `Memory` column (e.g., "256GB SSD + 1TB HDD") into `memory_size_gb` (calculating total size in GB) and `memory_type` (e.g., "SSD", "HDD", "SSD + HDD", handling missing values). The original column is dropped.
    * `drop_unnamed`: Removes an unnecessary index column often named 'Unnamed: 0' if present from the initial CSV read.
    * `reset_index`: Resets the DataFrame index to ensure it's sequential after rows may have been dropped.
3.  **Load:** Saves the processed DataFrame to `processed_laptopData.csv`.

import pandas as pd

# Remove rows with missing or invalid values
def drop_rows(df):
    # Drop rows where all columns are NaN (completely empty rows)
    df = df.dropna(how="all")
    # Drop rows that contain a '?' value in any column
    df = df[~df.isin(["?"]).any(axis=1)]
    return df

# Convert screen size from string to float
def convert_inches_float(df):
   df['Inches'] = pd.to_numeric(df['Inches'], errors='coerce')
   df = df.rename(columns={"Inches": "screen_size_inches"})
   return df

# Standardize RAM values by removing "GB" and converting to integer
def ram_standardized(df):
    df['Ram'] = df['Ram'].str.replace('GB', '', regex=False).astype(int) # Removes Unit to make into int data type
    df = df.rename(columns={"Ram": "ram_gb"})
    return df

# Standardize weight by removing "kg" and converting to float
def weight_standardized(df):
    df['Weight'] = pd.to_numeric(df['Weight'].str.replace('kg', '', regex=False), errors='coerce')
    df = df.rename(columns={"Weight": "weight_kg"})
    return df

# Split screen resolution into resolution, and screen_features columns
def split_screen_resolution(df):
    # Get the original index of 'ScreenResolution'
    screen_index = df.columns.get_loc("ScreenResolution")

    # Extract screen features and resolution using regex
    extracted_values = df['ScreenResolution'].str.extract(r'^(.*?)(\d+x\d+)$')
    
    # Clean and replace missing values
    screen_features = extracted_values[0].str.strip().replace('', 'No further details').fillna('No further details')
    screen_resolution = extracted_values[1]

    # Insert new columns at the correct position
    df.insert(screen_index, "screen_features", screen_features)
    df.insert(screen_index + 1, "screen_resolution", screen_resolution)

    # Drop the original column
    df = df.drop(columns=["ScreenResolution"])
    return df

# Split memory into memory_size and memory_type
def split_memory(df):
    def parse_memory(mem):
        if pd.isna(mem):
            return pd.Series([None, None])

        mem = str(mem).upper().replace('+', ' + ')
        drives = mem.split('+')
        total_size = 0.0
        types = set()

        for drive in drives:
            drive = drive.strip()
            size = 0.0
            dtype = ""
            if 'TB' in drive:
                try:
                    size = float(drive.split('TB')[0].strip()) * 1000
                    dtype = drive.split('TB')[1].strip()
                except:
                    continue
            elif 'GB' in drive:
                try:
                    size = float(drive.split('GB')[0].strip())
                    dtype = drive.split('GB')[1].strip()
                except:
                    continue
            else:
                continue

            total_size += size
            if dtype:
                types.add(dtype)

        memory_type = ' + '.join(sorted(types)) if types else None
        return pd.Series([total_size, memory_type])

    # Get the original index of 'Memory'
    mem_index = df.columns.get_loc("Memory")

    # Apply parsing function and insert at correct position
    df.insert(mem_index, "memory_size_gb", df["Memory"].apply(lambda x: parse_memory(x)[0]))
    df.insert(mem_index + 1, "memory_type", df["Memory"].apply(lambda x: parse_memory(x)[1]))

    # Drop the old 'Memory' column
    df = df.drop(columns=["Memory"])

    return df

# Remove unnecessary index column from import
def drop_unnamed(df):
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    return df

# Reset index to ensure it remains sequential after dropping rows
def reset_index(df):
    df = df.reset_index(drop=True)
    return df

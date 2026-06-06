import pandas as pd

def clean_and_prepare_data(input_filepath):
    """
    Loads the Superstore dataset, cleans the data, engineers new features,
    and exports a clean, Power-BI-ready CSV.
    """
    print(f"Loading data from {input_filepath}...")
    
    # Load the CSV. The Superstore dataset sometimes uses 'windows-1252' encoding
    try:
        df = pd.read_csv(input_filepath, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(input_filepath, encoding='windows-1252')
        
    print(f"Original dataset size: {df.shape[0]} rows, {df.shape[1]} columns.\n")

    # --- STEP 1: Remove Duplicates ---
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    duplicates_removed = initial_rows - len(df)
    print(f"Removed {duplicates_removed} duplicate rows.")

    # --- STEP 2: Standardize Data Types (Dates) ---
    # Convert 'Order Date' and 'Ship Date' to actual datetime objects
    # This prevents Power BI from treating dates as random text
    print("Converting date columns to standard Datetime format...")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])

    # --- STEP 3: Handle Missing Values ---
    # Drop rows if crucial columns like 'Sales' or 'Order Date' are missing
    df.dropna(subset=['Sales', 'Order Date', 'Profit'], inplace=True)
    
    # Fill any missing Postal Codes with a placeholder string (so we don't lose the whole row)
    if 'Postal Code' in df.columns:
        df['Postal Code'] = df['Postal Code'].fillna('00000').astype(str)

    # --- STEP 4: Feature Engineering (Creating new data for the CEO) ---
    print("Creating new KPI columns...")
    
    # KPI 1: Shipping Days (How long does it take to fulfill an order?)
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # Feature 2 & 3: Extract Year and Month for easy trend analysis in Power BI
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month_name()
    
    # Feature 4: Profit Margin Percentage (Profit / Sales)
    # This helps answer "Which categories are most profitable?"
    df['Profit Margin %'] = round((df['Profit'] / df['Sales']) * 100, 2)

    # --- STEP 5: Clean Text Data ---
    # Remove accidental leading/trailing spaces from categorical columns
    text_columns = ['Category', 'Sub-Category', 'Region', 'Segment']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # --- STEP 6: Export the Clean Dataset ---
    output_filename = 'Superstore_Cleaned_Ready_For_BI.csv'
    df.to_csv(output_filename, index=False)
    
    print("\n✅ Data cleaning complete!")
    print(f"Cleaned dataset saved as: '{output_filename}'")
    print(f"Final dataset size: {df.shape[0]} rows, {df.shape[1]} columns.")
    
    # Show a quick preview of the new columns
    print("\nPreview of new columns:")
    print(df[['Order Date', 'Shipping Days', 'Order Year', 'Profit Margin %']].head())

if __name__ == "__main__":
    # IMPORTANT: Change 'Sample - Superstore.csv' to the exact name of the file you downloaded
    file_path = 'Sample - Superstore.csv' 
    clean_and_prepare_data(file_path)
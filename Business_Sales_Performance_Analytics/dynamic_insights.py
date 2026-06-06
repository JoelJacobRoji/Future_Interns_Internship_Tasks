import pandas as pd

def generate_terminal_insights(file_path):
    print(f"--- Analyzing Dataset: {file_path} ---\n")
    
    try:
        # Load the dataset (handling common encoding issues)
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='windows-1252')
            
        # Ensure necessary columns exist; adapt if your column names differ slightly
        required_cols = ['Sales', 'Profit', 'Order Date', 'Category', 'Sub-Category', 'Region']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Error: The dataset is missing required columns: {missing_cols}")
            return

        # Prepare dates and standard KPIs
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Order Year'] = df['Order Date'].dt.year
        
        # Calculate Profit Margin
        df['Profit Margin %'] = (df['Profit'] / df['Sales']) * 100

        # ---------------------------------------------------------
        # Question 1: Which products generate the most revenue?
        # ---------------------------------------------------------
        print("💡 Q1: Which products generate the most revenue?")
        top_products = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False)
        top_3 = top_products.head(3)
        print("The top 3 revenue-generating sub-categories are:")
        for product, sales in top_3.items():
            print(f"  - {product}: ${sales:,.2f}")
        print()

        # ---------------------------------------------------------
        # Question 2: How do sales change over time?
        # ---------------------------------------------------------
        print("📈 Q2: How do sales change over time?")
        yearly_sales = df.groupby('Order Year')['Sales'].sum().sort_index()
        start_year = yearly_sales.index.min()
        end_year = yearly_sales.index.max()
        
        print(f"Analyzing trends from {start_year} to {end_year}:")
        for year, sales in yearly_sales.items():
            print(f"  - {year}: ${sales:,.2f}")
            
        # Dynamic trend logic
        if yearly_sales.iloc[-1] > yearly_sales.iloc[0]:
            print("  -> Trend Insight: Overall sales are showing an UPWARD growth trajectory.\n")
        else:
            print("  -> Trend Insight: Overall sales are showing a DOWNWARD or stagnant trajectory.\n")

        # ---------------------------------------------------------
        # Question 3: Which categories or regions are most profitable?
        # ---------------------------------------------------------
        print("💰 Q3: Which categories or regions are most profitable?")
        # Regional Profitability
        region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)
        top_region = region_profit.index[0]
        
        # Category Profitability
        category_profit = df.groupby('Category')['Profit Margin %'].mean().sort_values(ascending=False)
        top_category = category_profit.index[0]
        
        print(f"  - Most Profitable Region (Total Profit): {top_region} (${region_profit.iloc[0]:,.2f})")
        print(f"  - Most Profitable Category (Avg Margin): {top_category} ({category_profit.iloc[0]:.2f}%)\n")

        # ---------------------------------------------------------
        # Question 4: Where should the business focus to grow faster?
        # ---------------------------------------------------------
        print("🚀 Q4: Where should the business focus to grow faster? (Actionable Recommendations)")
        
        # Find money losers (Negative profit margins)
        product_profits = df.groupby('Sub-Category')['Profit'].sum().sort_values()
        money_losers = product_profits[product_profits < 0]
        
        print(f"  1. Capitalize on Strengths: Heavily focus marketing and inventory on the '{top_category}' category in the '{top_region}' region, as they yield the best financial returns.")
        
        if not money_losers.empty:
            worst_product = money_losers.index[0]
            worst_loss = money_losers.iloc[0]
            print(f"  2. Stop the Bleeding: The '{worst_product}' sub-category is actively losing money (Total Loss: ${worst_loss:,.2f}). Review pricing, shipping costs, or discontinue this product line immediately.")
        else:
            print("  2. Maintain Margins: No product categories are operating at a net loss, which is excellent. Focus on upselling existing customers.")
            
        print("\n--- End of Insights ---")

    except Exception as e:
        print(f"An error occurred while processing the data: {e}")

if __name__ == "__main__":
    # To run this, place your CSV file in the same folder and update the name below if needed!
    csv_file_name = "Superstore_Cleaned_Ready_For_BI.csv" 
    generate_terminal_insights(csv_file_name)
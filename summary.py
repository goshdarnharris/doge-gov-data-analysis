import pandas as pd


def summarize():
    # Load the contracts CSV file into a dataframe
    contracts_df = pd.read_csv('contracts.csv')

    # Find rows with "SEE FPDS" in either Value or Savings columns
    fpds_rows = contracts_df[(contracts_df['Value'] == 'SEE FPDS') | (contracts_df['Savings'] == 'SEE FPDS')]
    
    # Print the rows being removed
    if not fpds_rows.empty:
        print("\nRemoving the following rows containing 'SEE FPDS':")
        print(fpds_rows[['Agency', 'Description', 'Value', 'Savings']])
        
    # Remove the rows with "SEE FPDS"
    contracts_df = contracts_df[~((contracts_df['Value'] == 'SEE FPDS') | (contracts_df['Savings'] == 'SEE FPDS'))]

    # Load the real estate CSV file into a dataframe
    real_estate_df = pd.read_csv('real_estate.csv')

    # Convert the 'Savings' and 'Value' columns to numeric, removing any non-numeric characters
    contracts_df['Savings'] = contracts_df['Savings'].replace('[\$,]', '', regex=True).astype(float)
    contracts_df['Value'] = contracts_df['Value'].replace('[\$,]', '', regex=True).astype(float)
    real_estate_df['Savings'] = real_estate_df['Savings'].replace('[\$,]', '', regex=True).astype(float)
    real_estate_df['Value'] = real_estate_df['Value'].replace('[\$,]', '', regex=True).astype(float)

    # Calculate the total savings for contracts and real estate
    total_contracts_savings = contracts_df['Savings'].sum()
    total_real_estate_savings = real_estate_df['Savings'].sum()

    print(f"Total Contracts Savings: ${total_contracts_savings:,.2f}")
    print(f"Total Real Estate Savings: ${total_real_estate_savings:,.2f}")
    print(f"Total Savings: ${total_contracts_savings + total_real_estate_savings:,.2f}")

    # Add a new column for the ratio of Savings to Value in the contracts dataframe
    contracts_df['Savings to Value Ratio'] = contracts_df['Savings'] / contracts_df['Value']

    # Display the first few rows of the updated contracts dataframe
    print("\nUpdated Contracts DataFrame:")
    print(contracts_df.head())


if __name__ == "__main__":
    summarize()


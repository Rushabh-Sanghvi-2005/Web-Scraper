import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def remove_duplicates(df, column_name):
    return df.drop_duplicates(subset=[column_name])

def handle_missing_values(df, column_name):
    return df.dropna(subset=[column_name])

def filter_data(df, column_name, threshold_value):
    return df[df[column_name] > threshold_value]

def aggregate_data(df, column_name, aggregation_function):
    return df[column_name].agg(aggregation_function)

def visualize_data(df, column_name):
    df[column_name].plot.hist()
    plt.title(f'Histogram of {column_name}')
    plt.show()

def export_to_csv(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"DataFrame exported to {file_path}")

# User prompt to choose data source
data_source = input("Choose data source:\n1. Web\n2. Local CSV file\n3. Local Excel file\n")
if data_source == '1':
    # Take URL as input from the user
    url = input("Enter the URL of the website to scrape: ")

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all tables from the page
        tables = soup.find_all('table')

        # Display available tables and prompt user to choose one
        print("Available Tables:")
        for i, table in enumerate(tables):
            print(f"{i + 1}. Table {i + 1}")

        # User prompt to choose a table
        table_choice = int(input("Enter the number of the table you want to process: ")) - 1

        # Use pandas to read the selected HTML table into a DataFrame
        selected_table = tables[table_choice]
        df = pd.read_html(str(selected_table))[0]

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        exit()

elif data_source == '2':
    # Take local CSV file path as input
    csv_file_path = input("Enter the path of the local CSV file: ")

    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

elif data_source == '3':
    # Take local Excel file path as input
    excel_file_path = input("Enter the path of the local Excel file: ")

    # Read Excel file into a DataFrame
    df = pd.read_excel(excel_file_path)

else:
    print("Invalid choice. Please choose a valid option.")
    exit()

while True:
    print("\nCurrent DataFrame:")
    print(df)

    # User prompt
    user_choice = input("Choose an option:\n1. Remove Duplicates\n2. Handle Missing Values\n3. Filter Data\n4. Aggregate Data\n5. Visualize Data\n6. Export to CSV\n7. Exit\n")

    if user_choice == '1':
        column_name = input("Enter the column name for removing duplicates: ")
        df = remove_duplicates(df, column_name)
    elif user_choice == '2':
        column_name = input("Enter the column name for handling missing values: ")
        df = handle_missing_values(df, column_name)
    elif user_choice == '3':
        column_name = input("Enter the column name for filtering: ")
        threshold_value = float(input("Enter the threshold value for filtering: "))
        df = filter_data(df, column_name, threshold_value)
    elif user_choice == '4':
        column_name = input("Enter the column name for aggregation: ")
        aggregation_function = input("Enter the aggregation function (e.g., sum, mean): ")
        result = aggregate_data(df, column_name, aggregation_function)
        print(f"Aggregated result for {column_name}: {result}")
    elif user_choice == '5':
        column_name = input("Enter the column name for visualization: ")
        visualize_data(df, column_name)
    elif user_choice == '6':
        csv_export_path = input("Enter the path for CSV export: ")
        export_to_csv(df, csv_export_path)
    elif user_choice == '7':
        break
    else:
        print("Invalid choice. Please choose a valid option.")

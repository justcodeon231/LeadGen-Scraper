import os
import pandas as pd

def remove_duplicates_and_fill_empty_blocks(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        return

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Fill empty blocks
    # df.fillna(method='ffill', inplace=True)
    # df.fillna(method='bfill', inplace=True)

    # Save the cleaned file
    if file_path.endswith('.csv'):
        df.to_csv(file_path, index=False)
    elif file_path.endswith('.xlsx'):
        df.to_excel(file_path, index=False)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv') or file.endswith('.xlsx'):
                file_path = os.path.join(root, file)
                remove_duplicates_and_fill_empty_blocks(file_path)

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    process_directory(directory)
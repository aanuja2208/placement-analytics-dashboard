import os
import pandas as pd

def convert_csv_to_excel():
    data_dir = 'data'
    excel_path = os.path.join(data_dir, 'placement_dataset.xlsx')
    
    csv_files = {
        'students.csv': 'Students (Primary)',
        'yearly_outcomes.csv': 'Yearly Outcomes'
    }
    
    print("Converting CSV files to Excel sheets...")
    
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for csv_name, sheet_name in csv_files.items():
            csv_path = os.path.join(data_dir, csv_name)
            if os.path.exists(csv_path):
                print(f"Reading {csv_path}...")
                df = pd.read_csv(csv_path)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Added {csv_name} as sheet '{sheet_name}'.")
            else:
                print(f"Warning: {csv_name} not found, skipping.")
                
    print(f"Successfully created Excel file at: {excel_path}")

if __name__ == '__main__':
    convert_csv_to_excel()

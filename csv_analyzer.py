import pandas as pd
import matplotlib.pyplot as plt

def analyze_csv(file_path):
    try:
        # Read the CSV file
        data = pd.read_csv(file_path)
        print("CSV loaded successfully. Columns found:", data.columns.tolist())

        # Example: Assume columns 'Product' and 'Sales'
        # Replace these with actual column names in your CSV
        if 'Product' in data.columns and 'Sales' in data.columns:
            # Group data and plot
            data.plot(kind='bar', x='Product', y='Sales', title='Sales by Product')
            plt.xlabel('Product')
            plt.ylabel('Sales')
            plt.tight_layout()
            plt.show()
        else:
            print("CSV must have 'Product' and 'Sales' columns for this example.")
    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    file_path = input("Enter the path to your CSV file: ")
    analyze_csv(file_path)

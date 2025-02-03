import pandas as pd
import os
from typing import Optional


class DataLoader:
    """
    A class to load the A/B testing dataset.
    """

    def __init__(self, data_dir: str, filename: Optional[str] = None):
        self.data_dir = data_dir
        self.filename = filename if filename else "marketing_AB.csv"
        self.data = None

    def load_data(self) -> pd.DataFrame:
        """
        Loads the dataset from the specified directory.
        """
        file_path = os.path.join(self.data_dir, self.filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: Data file not found at {file_path}")

        try:
            self.data = pd.read_csv(file_path)
        except pd.errors.ParserError as e:
            raise ValueError(
                f"Error parsing the csv file at {file_path}. Please make sure it is valid. Details: {e}"
            )
        return self.data


if __name__ == "__main__":
    try:
        # Usage Example:
        project_dir = os.getcwd()
        raw_data_dir = os.path.join(project_dir, "data", "raw", "1")

        loader = DataLoader(raw_data_dir)
        df = loader.load_data()
        print(df.head())
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)

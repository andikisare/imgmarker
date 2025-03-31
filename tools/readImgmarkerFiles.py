import pandas as pd
import numpy as np

def read_marks(input_file):
    """
    Reads Image Marker marks file and converts to a Pandas DataFrame.

    inputs:
        input_file: str
            filename with full directory

    outputs:
        df: pandas DataFrame
            pandas DataFrame with all numerical values converted to np.float64 and all excessive whitespace removed
    """

    with open(input_file) as file:
        formatted_cols = []
        line0 = True
        for unformatted_line in file:
            if line0:
                line0 = False
                cols = unformatted_line.split('|')
                for col in cols:
                    formatted_col = col.strip()
                    formatted_cols.append(formatted_col)
                formatted_cols = formatted_cols[:-1]

            else:
                dtypes = {0: str, 1: str, 2: str, 3: str, 4: str, 5: str, 6: str, 7: str}
                df = pd.read_csv(input_file, delimiter='|', header=0, names=formatted_cols, usecols=[0,1,2,3,4,5,6,7], dtype=dtypes)
                numbers = ['x', 'y', 'RA', 'DEC']
                for key in df.columns:
                    df[key] = df[key].str.strip()
                    if key in numbers:
                        df[key] = df[key].astype(np.float64)

    return df

def read_images(input_file):
    """
    Reads Image Marker images file and converts to a Pandas DataFrame.

    inputs:
        input_file: str
            filename with full directory

    outputs:
        df: pandas DataFrame
            pandas DataFrame with all numerical values converted to np.float64 and all excessive whitespace removed
    """

    with open(input_file) as file:
        formatted_cols = []
        line0 = True
        for unformatted_line in file:
            if line0:
                line0 = False
                cols = unformatted_line.split('|')
                for col in cols:
                    formatted_col = col.strip()
                    formatted_cols.append(formatted_col)
                formatted_cols = formatted_cols[:-1]

            else:
                dtypes = {0: str, 1: str, 2: str, 3: str, 4: str, 5: str}
                df = pd.read_csv(input_file, delimiter='|', header=0, names=formatted_cols, usecols=[0,1,2,3,4,5], dtype=dtypes)
                numbers = ['RA', 'DEC']
                for key in df.columns:
                    df[key] = df[key].str.strip()
                    if key in numbers:
                        df[key] = df[key].astype(np.float64)
    return df

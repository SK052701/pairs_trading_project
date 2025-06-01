#!/usr/bin/env python
# coding: utf-8



import yfinance as yf
import pandas as pd
import os
from datetime import datetime




# 1. Download raw data
def download_data(tickers, start='2015-01-01', end=None, save_path=None):
    """
    Downloads historical market data for given tickers using yfinance and saves each as a CSV.

    Parameters:
    ----------
    tickers : list of str
        A list of stock ticker symbols to download (e.g., ['AAPL', 'MSFT']).
    start : str, optional
        Start date for the data in 'YYYY-MM-DD' format. Default is '2010-01-01'.
    end : str or None, optional
        End date for the data in 'YYYY-MM-DD' format. Default is None (uses today's date).
    save_path : str, optional
        Directory where raw CSV files will be saved. Default is 'data/raw'.

    Returns:
    -------
    dict
        A dictionary mapping each ticker to its corresponding raw DataFrame.
        Tickers that fail to download are skipped with an error message.
    """
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')

    data = {}
    for ticker in tickers:
        print(f"Downloading {ticker}...")
        try:
            df = yf.download(ticker, start=start, end=end)
            if df.empty:
                print(f"Warning: No data found for '{ticker}'. Skipping.")
                continue

            df['Ticker'] = ticker
            data[ticker] = df

            if save_path:
                os.makedirs(save_path, exist_ok=True)
                df.to_csv(f"{save_path}/{ticker}_raw.csv")

        except Exception as e:
            print(f"Error downloading '{ticker}': {e}")
            continue

    return data




# 2. Clean a single DataFrame
def clean_data(df, ticker=None, verbose=True):
    """
    Cleans a raw stock price DataFrame by handling missing values, duplicates, and invalid rows.

    Parameters:
    ----------
    df : pandas.DataFrame
        Raw stock data to be cleaned. Must contain columns: ['Open', 'High', 'Low', 'Close', 'Volume'].
    ticker : str, optional
        Ticker symbol used for logging purposes. Default is None.
    verbose : bool, optional
        Whether to print the cleaning logs. Default is True.

    Returns:
    -------
    tuple
        (cleaned_df, logs)
        cleaned_df : pandas.DataFrame
            The cleaned DataFrame.
        logs : list of str
            Log messages describing what cleaning steps were applied.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected a pandas DataFrame, but got {type(df).__name__}")

    # Check for required columns
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    logs = []
    ticker_info = f"[{ticker}]" if ticker else ""

    initial_rows = df.shape[0]
    logs.append(f"{ticker_info} Initial rows: {initial_rows}")

    # Convert index to datetime format
    try:
        df.index = pd.to_datetime(df.index)
    except Exception as e:
        raise ValueError("Index could not be converted to datetime format.") from e

    # Remove duplicate rows
    df = df.sort_index()
    df = df[~df.index.duplicated(keep='first')]
    logs.append(f"{ticker_info} Removed duplicate index entries.")

    # Remove missing values
    before = df.shape[0]
    df = df.dropna(subset=required_columns)
    logs.append(f"{ticker_info} Dropped {before - df.shape[0]} rows with NaNs.")

    # Remove nonsense entries
    before = df.shape[0]
    df = df[(df['Open'] > 0) & (df['High'] > 0) & (df['Low'] > 0) & (df['Close'] > 0) & (df['Volume'] >= 0)]
    logs.append(f"{ticker_info} Dropped {before - df.shape[0]} rows with invalid values.")

    # Final cleanup of NA's
    df = df.ffill().bfill()
    logs.append(f"{ticker_info} Final rows: {df.shape[0]}")

    if verbose:
        for line in logs:
            print(line)

    return df, logs




# 3. Clean multiple tickers
def batch_clean_data(raw_data_dict):
    """
    Applies the clean_data function to each DataFrame in a dictionary of raw data.

    Parameters:
    ----------
    raw_data_dict : dict
        Dictionary where keys are ticker symbols and values are raw DataFrames.
    verbose : bool, optional
        Whether to print cleaning logs for each ticker. Default is True.

    Returns:
    -------
    tuple
        (cleaned_data_dict, all_logs)
        cleaned_data_dict : dict
            Dictionary with cleaned DataFrames.
        all_logs : dict
            Dictionary mapping ticker symbols to their corresponding cleaning logs.
    """
    cleaned_data = {}
    logs = {}

    for ticker, df in raw_data_dict.items():
        cleaned_df, log = clean_data(df, ticker)
        cleaned_data[ticker] = cleaned_df
        logs[ticker] = log

    return cleaned_data, logs




# 4. Load data from CSV
def load_data(file_path):
    '''
    Loads a CSV file as a DataFrame with a datetime index.

    '''

    df = pd.read.csv(file_path, index_col=0, parse_dates=True)
    return df



# 5. Save cleaned data
def save_clean_data(df, ticker, save_path="data/clean", log_path=None):
    """
    Saves a cleaned DataFrame to a CSV file with a standardized filename.

    Parameters:
    ----------
    df : pandas.DataFrame
        The cleaned DataFrame to be saved.
    ticker : str
        The stock ticker symbol (used in the filename).
    save_path : str, optional
        Directory where the cleaned CSV will be saved. Default is 'data/clean'.
    log_path : str or None, optional
        If provided, a log entry will be written to this file upon successful save.
    """
    os.makedirs(save_path, exist_ok=True)
    file_name = f"{ticker}_clean.csv"
    file_path = os.path.join(save_path, file_name)
    
    df.to_csv(file_path)
    
    print(f"[Saved] Cleaned data saved to: {file_path}")
    
    if log_path:
        with open(log_path, 'a') as f:
            f.write(f"{pd.Timestamp.now()}: Saved cleaned data for {ticker} to {file_path}\n")




# 6. Logging function
def log_pipeline_step(log_path, message):
    """
    Appends a timestamped message to a log file.

    This function is useful for recording the steps of a data pipeline,
    such as downloading, cleaning, or saving data, to help with debugging,
    traceability, and auditing.

    Parameters:
    ----------
    log_path : str
        The file path to the log file where the message will be saved.
        If the file does not exist, it will be created.
    message : str
        The message to log. It will be prefixed with the current timestamp.

    Returns:
    -------
    None
    """
    with open(log_path, 'a') as f:
        f.write(f"{pd.Timestamp.now()}: {message}\n")







import pandas as pd
import random
import string
from datetime import datetime, timedelta
import numpy as np

def generate_loyalty_id():
    """Generate a loyalty ID with format: AA0000000000"""
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(str(random.randint(0, 9)) for _ in range(10))
    return letters + numbers

def generate_sequential_transaction_ids(start_num, count):
    """
    Generate sequential transaction IDs with format: XXXX-XXXX-XXXX
    Where X is a numeric digit and the overall number is ascending
    """
    transaction_ids = []
    for i in range(count):
        num = start_num + i
        # Format number to 12 digits with leading zeros
        num_str = str(num).zfill(12)
        # Split into groups of 4
        parts = [num_str[i:i+4] for i in range(0, 12, 4)]
        transaction_ids.append('-'.join(parts))
    return transaction_ids

def generate_sequential_timestamps(date_str, num_records):
    """
    Generate timestamps for a single date with random but ascending intervals
    """
    base_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Generate random seconds between transactions (between 1 and 300 seconds)
    intervals = sorted(random.randint(1, 300) for _ in range(num_records))
    
    # Calculate cumulative seconds and create timestamps
    cumulative_seconds = np.cumsum(intervals)
    
    # Spread the timestamps across the entire day
    total_seconds_in_day = 24 * 60 * 60
    scaling_factor = total_seconds_in_day / cumulative_seconds[-1]
    
    timestamps = [
        base_date + timedelta(seconds=int(sec * scaling_factor))
        for sec in cumulative_seconds
    ]
    
    return timestamps

def generate_dummy_data(
    start_date='2025-06-01',
    num_days=5,
    start_record_id=1,
    start_transaction_num=1000000,
    num_unique_customers=100
):
    """
    Generate dummy transaction data for multiple consecutive days
    
    Parameters:
    -----------
    start_date : str
        Starting date for transactions in 'YYYY-MM-DD' format
    num_days : int
        Number of consecutive days to generate data for
    start_record_id : int
        Starting value for record_id
    start_transaction_num : int
        Starting number for transaction IDs
    num_unique_customers : int
        Number of unique loyalty IDs to generate
    """
    
    # Generate fixed set of loyalty IDs
    loyalty_ids = [generate_loyalty_id() for _ in range(num_unique_customers)]
    
    # Categories
    categories = ['DRINKS', 'TOPUP', 'BILLS', 'FOOD', 'OTC', 'SUNDRIES', 'MEALS', 'GAMES']
    
    # Initialize empty DataFrame
    all_data = []
    current_record_id = start_record_id
    current_transaction_num = start_transaction_num
    
    # Convert start_date to datetime
    base_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    # Generate data for each day
    for day_offset in range(num_days):
        # Random number of transactions for this day
        daily_transactions = random.randint(5000, 6000)
        
        # Current date
        current_date = base_date + timedelta(days=day_offset)
        current_date_str = current_date.strftime('%Y-%m-%d')
        
        # Generate timestamps for this day
        timestamps = generate_sequential_timestamps(current_date_str, daily_transactions)
        
        # Generate transaction IDs for this day
        transaction_ids = generate_sequential_transaction_ids(
            current_transaction_num, 
            daily_transactions
        )
        
        # Generate data for this day
        daily_data = {
            'record_id': range(
                current_record_id, 
                current_record_id + daily_transactions
            ),
            'loyalty_id': random.choices(loyalty_ids, k=daily_transactions),
            'transaction_id': transaction_ids,
            'amount': np.round(np.random.uniform(50, 1000, daily_transactions), 2),
            'category': random.choices(categories, k=daily_transactions),
            'transaction_ts': timestamps
        }
        
        # Update counters for next day
        current_record_id += daily_transactions
        current_transaction_num += daily_transactions
        
        # Add daily data to the list
        all_data.append(pd.DataFrame(daily_data))
    
    # Combine all days' data
    df = pd.concat(all_data, ignore_index=True)
    
    return df

if __name__ == "__main__":
    # Generate sample data
    df = generate_dummy_data(
        start_date='2024-01-01',     # Starting date
        num_days=5,                  # Number of consecutive days
        start_record_id=1001,        # Starting record ID
        start_transaction_num=1000000, # Starting transaction number
        num_unique_customers=2500      # Number of unique loyalty IDs
    )
    
    # Save to CSV
    csv_filename = 'transaction_data.csv'
    df.to_csv(csv_filename, index=False)
    print(f"Generated {len(df)} records and saved to {csv_filename}")
    
    # Display summary statistics
    print("\nRecords per day:")
    print(df.groupby(df['transaction_ts'].dt.date).size())
    
    # Display first few records
    print("\nFirst few records:")
    print(df.head())
    
    # Display basic statistics
    print("\nAmount statistics:")
    print(df['amount'].describe())

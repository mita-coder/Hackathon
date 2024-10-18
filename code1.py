import pandas as pd
import time
from datetime import datetime, timedelta

# Load the dataset from a CSV file
def load_data(file_path):
    return pd.read_csv(file_path)

# Calculate signal timings
def calculate_signal_timings(df):
    # Step 1: Calculate total wait duration and PCU for each road
    road_stats = df.groupby('Road_No').agg({
        'Wait_Duration': 'sum',
        'PCU': 'sum'
    }).reset_index()

    # Step 2: Dynamic Programming allocation of green times
    total_green_time = 60  # Total time for green light cycle in seconds
    green_times = []

    for index, row in road_stats.iterrows():
        # Calculate proportionate green time based on PCU
        green_time = (row['PCU'] / road_stats['PCU'].sum()) * total_green_time
        green_times.append(green_time)

    # Step 3: Calculate red times
    red_times = [total_green_time - green for green in green_times]

    return road_stats['Road_No'], green_times, red_times

# Real-time signal simulation
def simulate_signals(road_numbers, green_times, red_times):
    start_time = datetime.strptime("08:00:00.000", "%H:%M:%S.%f")

    while True:
        for index in range(len(road_numbers)):
            road = road_numbers[index]
            green_time = green_times[index]
            red_time = red_times[index]
            
            # Calculate and print green signal time
            green_start = start_time
            green_end = start_time + timedelta(seconds=green_time)
            print(f"\nRoad {road}: Green Signal from {green_start.strftime('%H:%M:%S.%f')[:-3]} to {green_end.strftime('%H:%M:%S.%f')[:-3]}.")
            
            time.sleep(green_time)  # Simulate green signal duration
            start_time = green_end  # Update start time for red signal
            
            # Calculate and print red signal time
            red_end = start_time + timedelta(seconds=red_time)
            print(f"Road {road}: Red Signal from {start_time.strftime('%H:%M:%S.%f')[:-3]} to {red_end.strftime('%H:%M:%S.%f')[:-3]}.")
            
            time.sleep(red_time)  # Simulate red signal duration
            start_time = red_end  # Update start time for next cycle

# Main function
def main():
    # Path to your CSV file
    file_path = 'C:\\Users\\bhavy\\OneDrive\\Desktop\\hackathon\\traffic_dataset.csv'  # Change to your actual file path
    df = load_data(file_path)
    
    road_numbers, green_times, red_times = calculate_signal_timings(df)
    
    print("Signal Timing for Each Road:")
    output = pd.DataFrame({
        'Road_No': road_numbers,
        'Green_Time (s)': [round(time, 2) for time in green_times],
        'Red_Time (s)': [round(time, 2) for time in red_times]
    })
    
    print(output)
    
    simulate_signals(road_numbers, green_times, red_times)

if __name__ == "__main__":
    main()

# PM2.5 Monitoring System

This project is a **Python-based PM2.5 monitoring system** that retrieves air quality data from the **Taiwan Ministry of Environment Open Data API**.

Users can select a city or county to monitor, view the latest PM2.5 readings from different monitoring stations, and automatically check for updated data every **15 minutes**.

The system also provides an audible warning when the highest PM2.5 concentration in the selected area reaches or exceeds the predefined threshold.

## Features

- Connects to the Taiwan Ministry of Environment Open Data API
- Supports user-provided API Keys
- Supports multiple cities and counties in Taiwan
- Displays available monitoring locations
- Allows users to select a default monitoring city
- Allows users to change the monitoring city while the program is running
- Immediately refreshes the data after changing the monitoring city
- Automatically checks for the latest PM2.5 data every 15 minutes
- Keeps only the latest reading from each monitoring station
- Sorts monitoring stations by PM2.5 concentration
- Displays the station name, PM2.5 value, unit, and data time
- Identifies the monitoring station with the highest PM2.5 concentration
- Plays a warning sound when PM2.5 reaches or exceeds the threshold
- Supports interactive commands during monitoring
- Uses multithreading to handle user commands while monitoring continues

## Monitoring Process

The basic monitoring process is:

```text
Enter API Key
      ↓
Select City / County
      ↓
Retrieve PM2.5 Data
      ↓
Keep Latest Data from Each Station
      ↓
Sort by PM2.5 Concentration
      ↓
Display Monitoring Results
      ↓
Check Warning Threshold
      ↓
Wait 15 Minutes
      ↓
Check Again
```

The monitoring process continues until the user enters `stop` or `shutdown`.

## PM2.5 Warning Threshold

The default PM2.5 warning threshold is:

```text
35
```

The warning condition is:

```text
PM2.5 < 35  → Normal Monitoring

PM2.5 >= 35 → Warning
```

When the highest PM2.5 value in the selected city or county reaches or exceeds `35`, the program displays a warning message and plays an audible alert.

The threshold can be changed in the program:

```python
THRESHOLD = 35
```

## Update Interval

The program checks for the latest PM2.5 data every:

```text
15 minutes
```

The checking interval is defined as:

```python
CHECK_INTERVAL = 900
```

where `900` seconds is equal to 15 minutes.

If the user changes the monitoring city using the `change` command, the program does not wait for the next 15-minute interval and immediately retrieves data for the new location.

## Monitoring Data

For each monitoring station, the program displays:

- Station name
- PM2.5 concentration
- Measurement unit
- Data creation time
- Warning status

The program keeps only the latest available record from each monitoring station.

The monitoring stations are then sorted from the highest PM2.5 concentration to the lowest.

Example:

```text
============================================================
臺中市 PM2.5 即時監測
檢查時間: 2026-08-09 20:00:00
============================================================

測站:測站A    PM2.5:38.0    μg/m3    時間:2026-08-09 19:00 ⚠️超標
測站:測站B    PM2.5:25.0    μg/m3    時間:2026-08-09 19:00
測站:測站C    PM2.5:18.0    μg/m3    時間:2026-08-09 19:00
```

The station with the highest PM2.5 value is also displayed separately.

## Commands

### Main Menu

The following commands are available from the main menu:

| Command | Function |
|---------|----------|
| `start` | Start PM2.5 monitoring |
| `city` | Display the available cities and counties |
| `change` | Change the default monitoring city |
| `shutdown` | Close the program |

### During Monitoring

The following commands can be entered while monitoring is active:

| Command | Function |
|---------|----------|
| `stop` | Stop monitoring and return to the main menu |
| `change` | Change the monitoring city and immediately refresh the data |
| `city` | Display the available cities and counties |
| `shutdown` | Stop monitoring and close the program |

## Supported Locations

The program supports the following cities and counties:

```text
臺北市
新北市
桃園市
新竹市
新竹縣
苗栗縣
臺中市
彰化縣
南投縣
雲林縣
嘉義市
嘉義縣
臺南市
高雄市
屏東縣
宜蘭縣
花蓮縣
臺東縣
澎湖縣
金門縣
連江縣
```

## API

This project uses PM2.5 data provided by the:

**Taiwan Ministry of Environment Open Data Platform**

The program retrieves data from the PM2.5 dataset through the Ministry of Environment API.

An API Key is required before starting the monitoring system.

The API Key is entered when the program starts:

```text
請輸入 API Key：
```

## Installation

Install the required Python package using:

```bash
pip install requests
```

If a `requirements.txt` file is included, you can also use:

```bash
pip install -r requirements.txt
```

## Running the Program

Run the program using:

```bash
python PM2.5_pro.py
```

After starting the program:

```text
1. Enter the API Key
2. Use "city" to view available locations
3. Use "change" to select a default monitoring city
4. Use "start" to begin monitoring
5. Use "stop" to stop monitoring
6. Use "shutdown" to close the program
```

## Multithreading

The program uses Python's `threading` module to allow user commands to be entered while PM2.5 monitoring is active.

A separate listener thread handles commands such as:

```text
stop
change
city
shutdown
```

while the main monitoring loop continues retrieving and displaying PM2.5 data.

This allows the user to control the program without waiting for the 15-minute monitoring interval to finish.

## Warning Sound

The program uses the Python `winsound` module to generate an audible warning.

When the PM2.5 value reaches or exceeds the threshold:

```python
winsound.Beep(2000, 1000)
```

A 2000 Hz warning sound is played for 1000 milliseconds.

Because `winsound` is used, the audible alert feature is intended for **Windows systems**.

## Error Handling

The program includes basic error handling for:

- Network connection failures
- API response errors
- Invalid JSON responses
- Missing monitoring station data
- Invalid PM2.5 values
- Invalid date and time values
- Invalid city names
- Invalid user commands

## Tools and Technologies

- Python
- Requests
- REST API
- JSON
- Python Threading
- Python Event Objects
- Windows `winsound`
- Taiwan Ministry of Environment Open Data API

## Learning Objectives

This project demonstrates several Python programming concepts, including:

- REST API integration
- HTTP requests
- JSON data processing
- Environmental data monitoring
- Data filtering
- Data sorting
- Date and time processing
- Threshold-based warning systems
- Multithreading
- Thread synchronization using `Event`
- Interactive command processing
- Error handling

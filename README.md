# PM2.5 Real-Time Monitoring System

This project is a **Python-based PM2.5 real-time monitoring system** that retrieves the latest air quality data from the **Taiwan Ministry of Environment Open Data API**.

Users can select a city or county to monitor, and the program automatically checks the latest PM2.5 readings from monitoring stations in the selected area.

The system updates the data every **15 minutes** and provides an alert when the PM2.5 concentration exceeds the specified threshold.

## Features

- Connects to the Taiwan Ministry of Environment Open Data API
- Supports user-provided API Keys
- Displays available cities and counties for monitoring
- Allows users to select a monitoring location
- Allows users to change the monitoring location while using the program
- Automatically updates PM2.5 data every 15 minutes
- Keeps the latest PM2.5 reading from each monitoring station
- Displays the monitoring time and PM2.5 concentration
- Plays a warning sound when PM2.5 exceeds the specified threshold
- Supports commands for stopping monitoring or closing the program

## Monitoring Process

The basic monitoring process is:

```text
Select City / County
        ↓
Retrieve PM2.5 Data
        ↓
Display Latest Station Data
        ↓
Check PM2.5 Threshold
        ↓
Wait 15 Minutes
        ↓
Update Again
```

The system continuously monitors PM2.5 levels until the user stops the monitoring process.

## PM2.5 Warning

The program compares the latest PM2.5 value with a predefined threshold.

If the PM2.5 concentration exceeds the threshold, the system plays a warning sound to notify the user.

For example:

```text
PM2.5 <= Threshold → Normal Monitoring

PM2.5 > Threshold  → Warning Sound
```

The threshold can be modified in the Python program according to the user's requirements.

## Update Interval

The default monitoring interval is:

```text
15 minutes
```

After each update, the program waits for 15 minutes before retrieving the latest PM2.5 data again.

## Commands

The program provides simple commands for controlling the monitoring system.

| Command | Function |
|---------|----------|
| `start` | Start PM2.5 monitoring |
| `city` | View available monitoring locations |
| `change` | Change the monitoring city or county |
| `stop` | Stop the current monitoring process |
| `shutdown` | Close the program |

## API

This project uses air quality data provided by the **Taiwan Ministry of Environment Open Data Platform**.

An API Key is required to access the environmental data.

The API Key can be obtained from the Ministry of Environment Open Data Platform.

## Installation

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

## Running the Program

Run the program using:

```bash
python PM2.5_pro.py
```

After starting the program, enter the required API Key and select the city or county you want to monitor.

## Example

```text
Start Program
     ↓
Enter API Key
     ↓
Select Monitoring City
     ↓
Start Monitoring
     ↓
Retrieve PM2.5 Data
     ↓
Display Latest Results
     ↓
Check Every 15 Minutes
```

## Files

- `PM2.5_pro.py` - Main PM2.5 monitoring program
- `requirements.txt` - Required Python packages

## Tools and Technologies

- Python
- Requests
- Taiwan Ministry of Environment Open Data API
- Multithreading
- Windows Sound Alert

## Learning Objectives

This project demonstrates several Python programming concepts, including:

- REST API integration
- JSON data processing
- Real-time environmental data monitoring
- User command processing
- Periodic data updates
- Multithreading
- Threshold-based warning systems
- Error handling

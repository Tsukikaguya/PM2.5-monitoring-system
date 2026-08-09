
```markdown
# PM2.5 Real-Time Monitoring System

A Python-based PM2.5 monitoring system that retrieves the latest air quality data from the Taiwan Ministry of Environment Open Data API.

## Features

- Supports user-provided Ministry of Environment API Keys
- Displays available cities and counties for monitoring
- Allows users to select and change the monitoring location
- Automatically updates PM2.5 data every 15 minutes
- Keeps only the latest reading from each monitoring station
- Plays an alert sound when the PM2.5 level exceeds the specified threshold
- Enter `stop` to stop monitoring
- Enter `shutdown` to exit the program

## Installation

```bash
pip install -r requirements.txt

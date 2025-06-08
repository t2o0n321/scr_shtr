# scr_shtr

**Tool to take screenshots of eBooks automatically**

This tool automates the process of capturing screenshots from eBooks by allowing you to set specific positions and configure settings. Follow the setup and usage instructions below to get started.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
  - [1. Set Positions through `position_chooser.py`](#1-set-positions-through-position_chooserpy)
  - [2. Set `pages_count`](#2-set-pages_count)
  - [3. (Optional) Set `Times` Section](#3-optional-set-times-section)
  - [4. Run `screenshots.py`](#4-run-screenshotspy)

## Setup

To set up the `scr_shtr` tool, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/t2o0n321/scr_shtr.git
   ```

2. Create and activate a virtual environment:
   - **Linux/MacOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     python3 -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example configuration file:
   ```bash
   cp conf.yaml.example conf.yaml
   ```

## Usage

### 1. Set Positions through `position_chooser.py`

This script allows you to choose three positions for screenshot automation:
- **Top-Left Corner** (`book_pos_1`)
- **Down-Right Corner** (`book_pos_2`)
- **Next Page Button** (`next_page`)

- Click to set each position in sequence.
- Press `'esc'` to save the positions and exit.
- Press `'r'` to reset all positions to zero.

Run the script:
```bash
python3 position_chooser.py
```

### 2. Set `pages_count`

- `pages_count` determines the number of pages to capture screenshots for.
- Edit this value in the `conf.yaml` file under the `General` section to specify the total number of pages.

### 3. (Optional) Set `Times` Section

- To avoid being blocked by the eBook vendor, the tool applies a random delay between actions by default.
- If you are using an offline eBook reader (e.g., bookshelf) and are certain you won't be blocked, you can adjust the `Times` section in `conf.yaml` for faster execution:
  - `delay_to_start`: Initial delay before starting (default: 10 seconds).
  - `min_delay_between`: Minimum delay between actions (default: 3.0 seconds).
  - `max_delay_between`: Maximum delay between actions (default: 5.0 seconds).

### 4. Run `screenshots.py`

Once positions and settings are configured, run the main script to start capturing screenshots:
```bash
python3 screenshots.py
```
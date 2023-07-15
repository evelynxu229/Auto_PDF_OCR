# Real-Time OCR Model for Automotive Parts Data Recognition


## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage Guide](#usage-guide)


## Project Overview

In this project, an innovative Optical Character Recognition (OCR) model was developed, specifically designed to auto-recognize automotive parts data from PDFs and integrate this data directly into Excel spreadsheets. The system continuously monitors a specified folder for new PDF updates and initiates automatic processing and image enhancement for optimal text recognition when an update is detected. This project highlights the effective use of advanced automation solutions for the seamless extraction and organization of key data, significantly enhancing efficiency in the handling of automotive parts information.

## Project Structure

- /PDF_OCR
  - /code
    - HoughLinesP.py
    - shmain.py
    - shuanghuan_watchdog.py
    - shPdfOcr.py
  - /data
    - testfile.pdf
  - /log
    - shuanghuanMatchlog_traceback.log
  - /output
    - /pic
    - /txt
    - /xlsx
  - /template
    - templatefile.xlsx
  - readme.md
  - requirements.txt

## Installation
To install the required dependencies for the project, run the following command in the command line:
```bash
$ pip install -r requirements.txt
```

## Usage Guide

To run the project, use the following command in the command line:

```bash
$ python ./code/shuanghuan_watchdog.py
```


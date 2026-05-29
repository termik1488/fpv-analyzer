# FPV Analyzer

FPV Analyzer is a Python-based tool for analyzing intercepted FPV drone telemetry and OCR data from WhatsApp groups.

The project parses messages, extracts telemetry data using OCR, stores results in SQLite, and generates analytical Excel reports.

## Features

* WhatsApp chat parsing
* OCR processing using Tesseract
* SQLite database storage
* Frequency analytics
* Excel report generation
* Control/video frequency distribution analysis
* Crew activity statistics
* Launch distance estimation
* Automatic highlighting of dangerous launch distances

---

## Technologies

* Python 3
* SQLite
* OpenPyXL
* Pillow
* Pytesseract

---

## Project Structure

```text
fpv_analyzer/
│
├── data/
├── db/
├── export/
├── parser/
├── utils/
├── whatsapp/
│
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/termik1488/fpv-analyzer.git
cd fpv-analyzer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Tesseract OCR separately:

https://github.com/tesseract-ocr/tesseract

---

## Usage

Run the analyzer:

```bash
python main.py
```

Generated Excel reports will contain:

* Interceptions table
* Frequency analytics
* Crew statistics
* Detection range analysis

---

## Example Analytics

The analyzer supports:

* Video frequency analysis
* Control frequency distribution
* Protocol detection
* LoRa parameter extraction
* Launch distance estimation

---

## Future Plans

* Real-time WhatsApp monitoring
* Automatic graph generation
* Map visualization
* AI-assisted signal classification
* Web dashboard

---

## License

This project is for educational and research purposes only.

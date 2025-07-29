#!/bin/bash
set -e
# Example integration test: run scanner CLI and check output
python main_cli.py report --input tests/test_scan.json --format html --output test_report.html
if [ ! -f test_report.html ]; then
  echo "[ERROR] Report not generated!"; exit 1
fi
echo "[INFO] Integration test passed."

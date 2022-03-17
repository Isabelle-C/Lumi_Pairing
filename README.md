# Lumi_Pairing

This repository is for Lumi Pairing. Follow steps below to run the code.

1. Clone the repo.
2. Initialize the repository with Poetry by running:
$ poetry init
3. Install dependencies.
$ poetry install
4. Activate the environment.
$ poetry shell
5. Run the command in following format: python ./main.py /path/to/students.csv /path/to/tutors.csv /path/for/all/outputs

Some troubleshooting tips:
1. Make sure you are inputting csv files
2. Make sure those two files include columns: "Language", "Interest", and "Submission Date"

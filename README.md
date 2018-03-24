# Prerequisites:
* Python 2.7 or 3.6
* Python pip
* Virtualenv

# How to set up and start
1. Clone the repo and open a terminal in the root
2. Set up local virtualenv: `virtualenv ./virtualenv`
3. Activate virtualenv: `source ./virtualenv/bin/activate` 
4. Install dependencies: `pip install -r requirements.txt`
5. Place your data in `data` folder
6. Start: `python src/main.py <path-to-data> <time-base>`, where:
    * `<path-to-data>` is the relative (or absolute) path to the directory containing all the data.
    * `<time-base>` is the date of the export that serves as relative time base for any date calculations.

# Project 1

This is my first project for CSE 564


# Directory structure

- `assets/` - contains **style.css** file for custom styling.
- `data/` - contains both raw and preprocessed data.
- `app.py` - main file for this application. Contains all functioning Dash and Plotly code.
- `features.json` - json file of my feature names separated by whether they're categorical or numerical. Gets read by `app.py`.
- `preprocess_data.ipynb` - file for preprocesing data

# Requirements
- python = "^3.9"
- numpy = "^1.24.1"
- pandas = "^1.5.3"
- plotly = "5.13.0"
- dash = "^2.8.1"
- dash-bootstrap-components = "^1.3.1"

# Usage

Run:
```shell
python app.py
```
to execute the application and open the webpage.
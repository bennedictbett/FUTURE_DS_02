import os
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "churn_analysis"

list_of_files = [

    ".github/workflows/.gitkeep",

    # Source modules
    f"src/{project_name}/__init__.py",
    "src/__init__.py",
    "src/load_clean.py",           
    "src/churn_metrics.py",        
    "src/cohort_analysis.py",      
    "src/segmentation.py",         
    "src/lifetime_value.py",       
    "src/export_for_powerbi.py",   

    # Notebooks
    "notebooks/01_data_exploration.ipynb",
    "notebooks/02_churn_analysis.ipynb",
    "notebooks/03_cohort_retention.ipynb",
    "notebooks/04_segmentation.ipynb",

    # Data folders
    "data/raw/.gitkeep",           
    "data/processed/.gitkeep",    

    # Power BI
    "powerbi/.gitkeep",            

    # Reports
    "reports/figures/.gitkeep",    
    "reports/summary.md",          

    # Config & setup
    "config.yaml",
    "requirements.txt",
    "setup.py",
    "README.md",
    ".gitignore",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

logging.info("Churn Analysis project structure created successfully!")
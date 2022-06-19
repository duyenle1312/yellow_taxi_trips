# yellow_taxi_trips
Extract data, remove outliers or false datapoints and load data to a remote db

There are two versions of the code: Collab Notebook and Python file. The notebook version is easier to use for exploring because it shows the results of data processing in each step. For production or automation purposes, the Python version is recommended.

Here is the link to the original Collab folder with all the files that are generated: https://colab.research.google.com/drive/1soVQAq3wW4AYBIcFqWP5zSrDe4MDvWni?usp=sharing

To run the python script locally:

1. Create virtual environment
```bash
python -m venv venv
```

2. Activate virtual environment
For Windows: 
```bash
venv\Scripts\activate
```
For Linux: 
```bash
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the script
```bash
python processing.py
```

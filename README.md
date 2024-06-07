# PyLucene-based Search Interface for Reddit Data

## Overview

This project demonstrates the creation of a search interface for Reddit data using PyLucene. The system parses JSON objects from large Reddit datasets, indexes the data using PyLucene, and provides a web-based interface built with Flask. Users can search through the indexed Reddit posts and retrieve results ordered by a combination of relevance and timestamp.

<div style="display: flex;"><h3>languages and tools:</h3>
  <img alt="HTML5" src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white"/>
  <img alt="CSS3" src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white"/>
  <img alt="Git" src="https://img.shields.io/badge/git%20-%23F05033.svg?&style=for-the-badge&logo=git&logoColor=white"/>
  <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
  <img alt="Flask" src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white"/>

</div>

# Prerequisites

1. **Python 3.x**: Ensure Python is installed on your system.
2. **PyLucene**: Install PyLucene by following the instructions [here](https://lucene.apache.org/pylucene/).
3. **Flask**: Install Flask using pip:
   ```bash
   pip install flask
   ```
   or
   ```bash
   pip3 install flask
   ```
  
# Installation
## Clone the Repository:

```bash
git clone https://github.com/your-repo/pylucene-reddit-search.git
cd pylucene-reddit-search
```

## Prepare the Data:
Place your Reddit JSON data files in the searchBrowser directory.

# Running the Web Application
## Set Environment Variable:

```bash
export FLASK_APP=pylucene.py
```
## Run Flask:

```bash
flask run -h 0.0.0.0 -p 8888
```

## Access the Interface:
Open your web browser and go to http://127.0.0.1:8888.

# Web Interface
The web interface contains a search textbox and a search button. When a search query is entered and the button is clicked, the application displays a list of the first 10 results returned by PyLucene, ordered by a combination of relevance and timestamp.

# Ranking Function
The ranking function orders the posts based on a combination of relevance and timestamp. Relevance is determined by PyLucene's scoring mechanism, and the timestamp ensures that more recent posts are given higher priority.

# Contributors
- Lester Lien
- Chaiwat Wongsatjachock
- Dennis Santoso
- Elijah Fang
- Neel Parekh




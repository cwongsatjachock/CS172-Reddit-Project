# Ensure Python 3.x is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3.x is not installed. Please install it and run the script again."
    exit 1
fi

# Install Flask
pip3 install flask

# Assuming user navigates to CS172-Reddit-Project directory, move to /searchBrowser
cd searchBrowser

# Run pylucene.py file
export FLASK_APP=pylucene.py
flask run -h 0.0.0.0 -p 8888
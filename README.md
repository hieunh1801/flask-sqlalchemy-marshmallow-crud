# FLASK + SQLALCHEMY + MARSHMALLOW

## script
```bash
# create venv
virtualenv venv

# install lib
pip install -r requirements.txt

# generate db
python create_db.py

# run 
python app.py
```

## query
```python
# get all
data = UserModel.query.all()

# get paginate
data = UserModel.query.all()
```
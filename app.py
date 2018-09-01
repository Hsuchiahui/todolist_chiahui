from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

# initialize
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# models
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(120), nullable=True)
    date = db.Column(db.Date, nullable=True)
    check = db.Column(db.Boolean, nullable=True)


# views
@app.route("/")
def index():
    return render_template('index.html')



@app.route("/record", methods=['POST'])
def add_record():
    req_data = request.form
    event = req_data['event']
    date = datetime.strptime(req_data['date'],'%Y-%m-%d')
    date = datetime.date(date)
    record = Record(event = event, date = date)
    db.session.add(record)
    db.session.commit()
    return 'Create Succeeded', 200


@app.route("/record", methods=['GET'])
def get_records():
    records = Record.query.all()
    records_data = [
        {
            'id': record.id,
            'event': record.event,
            'date': datetime.strftime(record.date,'%Y-%m-%d'),
            'check':record.check 
        }
        for record in records
    ]
    return jsonify(records_data), 200
#前端傳送check的值到伺服器變成str，此函數將str轉回boolean
def str2bool(v):
  return v in ("true")

@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = Record.query.filter_by(id=record_id).first()
    record_data = {
        'id': record.id,
        'event': record.event,
        'date': record.date,
    }
    print(record_data)
    return jsonify(record_data), 200


@app.route('/record/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    req_data = request.form
    record = Record.query.filter_by(id=record_id).first()
    if 'check' in req_data:
        record.check =str2bool(req_data['check'])
    else:     
        record.event = req_data['event']
        record.date = req_data['date']
        date = datetime.strptime(req_data['date'],'%Y-%m-%d')
        record.date = datetime.date(date)
    db.session.add(record)
    db.session.commit()
    return 'Update Succeeded', 200
    
@app.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    record = Record.query.filter_by(id=record_id).first()
    db.session.delete(record)
    db.session.commit()
    return 'Delete Succeeded', 200

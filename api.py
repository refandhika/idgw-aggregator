import MySQLdb

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/v1/aggrdata")
def get_aggr_data():
    db = MySQLdb.connect(user='1dGWUs3r!', passwd='1dGWp4Ss!', db='idgwoffsite', host='localhost', charset="utf8", use_unicode=True)
    cur = db.cursor()

    try:
        page = 1
        parampage = request.args.get('page')
        if parampage is not None:
            if parampage > 1:
                page = parampage
        offset = (page - 1) * 20

        try:
            cur.execute("""SELECT * FROM articles ORDER BY created_at DESC LIMIT 20 OFFSET %s""", (offset,))
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
       
            response = {
                "data": [],
                "status": 500,
                "message": e
            }

            return jsonify(response)

        try:
            records = cur.fetchall()
            total = len(records)
            articles = []

            for row in records:
                site = "#"
                if row[8] is not "null":
                    site = row[8]
                item = {
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "image": row[3],
                    "link": row[4],
                    "author": row[5],
                    "source": row[6],
                    "created_at": row[7],
                    "site": site
                }
                articles.append(item)

            response = {
                "data": {
                    "articles": articles,
                    "total": total
                },
                "status": 200,
                "message": "Data found!"
            }

            return jsonify(response)
        except TypeError as e:
            print(e)

            response = {
                "data": [],
                "status": 500,
                "message": e
            }

            return jsonify(response)
    finally:
        cur.close()
        db.close()

@app.get("/v1/aggrdata/single")
def get_aggr_single():
    db = MySQLdb.connect(user='1dGWUs3r!', passwd='1dGWp4Ss!', db='idgwoffsite', host='localhost', charset="utf8", use_unicode=True)
    cur = db.cursor()

    try:
        iid = request.args.get('iid')

        try:
            cur.execute("""SELECT * FROM articles WHERE id = %s""", (iid,))
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
       
            response = {
                "data": [],
                "status": 500,
                "message": e
            }

            return jsonify(response)

        try:
            record = cur.fetchone()
            
            item = {}
            response = {
                "data": [],
                "status": 400,
                "message": "Data not found!"
            }

            if record is not None: 
                item = {
                    "id": record[0],
                    "title": record[1],
                    "content": record[2],
                    "image": record[3],
                    "link": record[4],
                    "author": record[5],
                    "source": record[6],
                    "created_at": record[7],
                    "site": record[8]
                }

                response = {
                    "data": item,
                    "status": 200,
                    "message": "Data found!"
                }


            return jsonify(response)
        except TypeError as e:
            print(e)

            response = {
                "data": [],
                "status": 500,
                "message": e
            }

            return jsonify(response)

    finally:
        cur.close()
        db.close()
 

if __name__ == "__main__":
    app.run(host='0.0.0.0')

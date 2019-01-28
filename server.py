from bottle import response, error, redirect, HTTPResponse, HTTPError, get, post, put, delete, request, template
import json

###############################################################################
# Routes
###############################################################################

#Fetches the entire database of items.
@get('/db')
def db_all(db):
    db.execute("SELECT * FROM supermarket")
    products = db.fetchall()
    if products:
        return HTTPResponse(body=json.dumps(products), status=200, content_type='application/json')
    else:
        return HTTPResponse(body="Database is empty.", status=200, content_type='application/json')
	
	

# Fetches a single item by ID.
@get('/db/<itmid>')
def db_get(db, itmid):
    db.execute("SELECT * FROM supermarket WHERE id=?", (itmid,))
    products = db.fetchall()
    if products:
        return HTTPResponse(body=json.dumps(products), status=200, content_type='application/json')
    else:
        return HTTPError(status=404, content_type='application/json')
	
	

# Resets the entire database by deleting all entries.
@get('/db/reset')
def db_reset(db):
    db.execute("DELETE FROM supermarket")
    return HTTPResponse(body="Success, the database has been reset.", status=200, content_type='application/json')
	
	
	

# Deletes a single item from the database by ID.
@delete('/db/<itmid>')
def db_reset(db, itmid):
    db.execute("SELECT * FROM supermarket WHERE id=?", (itmid,))
    products = db.fetchall()

    if not products:
        return HTTPError(status=404, content_type='application/json')
    
    db.execute("DELETE FROM supermarket WHERE id=?", (itmid,))
    return HTTPResponse(body="Success, this item ID has been deleted.", status=200, content_type='application/json')
	
	

# Adds a new item to the database, autoassigns an ID.
@post('/db')
def db_post(db):
    
    data = request.json
    product = data["product"]
    origin = data["origin"]
    amount = data["amount"]
    image = data["image"]
    best_before_date = data["best_before_date"]
    
    if product and origin and amount and image and best_before_date:
        db.execute("INSERT INTO supermarket VALUES (null, ?,?,?,?,?)", (product, origin, amount, image, best_before_date))
        db.execute("SELECT * FROM supermarket ORDER BY id DESC LIMIT 1")
        products = db.fetchall()
        return HTTPResponse(body=json.dumps(products), status=201, content_type='application/json')
    else:
        return HTTPError(status=400, content_type='application/json')
	
	

# Updates an item from the database by ID.
@put('/db/<itmid>')
def db_update(db, itmid):
    
    data = request.json
    product = data["product"]
    origin = data["origin"]
    amount = data["amount"]
    image = data["image"]
    best_before_date = data["best_before_date"]

    db.execute("SELECT * FROM supermarket WHERE id=?", (itmid,))
    products = db.fetchall()

    if not products:
        return HTTPError(status=404, content_type='application/json')

    if product and origin and amount and image and best_before_date:
        db.execute("UPDATE supermarket SET product=?, origin=?, amount=?, image=?, best_before_date=? WHERE id=?", (data["product"], data["origin"], data["amount"], data["image"], data["best_before_date"], itmid))
        db.execute("SELECT * FROM supermarket WHERE id=?", (itmid,))
        products = db.fetchall()
        return HTTPResponse(body=json.dumps(products), status=200, content_type='application/json')
    else:
        return HTTPError(status=400, content_type='application/json')



###############################################################################
# Error handling
###############################################################################

@error(404)
def error404(error):
    return 'Not Found: Item does not exist.'

@error(400)
def error400(error):
    return 'Bad Request: Invalid JSON'

###############################################################################
# This starts the server
#
# Access it at http://localhost:8080
#
# The installed plugin 'WtPlugin' takes care of enabling CORS (Cross-Origin
# Resource Sharing; you need this if you use your API from a website) and
# provides you with a database cursor.
###############################################################################

if __name__ == "__main__":
    from bottle import install, run
    from wtplugin import WtDbPlugin, WtCorsPlugin

    install(WtDbPlugin())
    install(WtCorsPlugin())
    run(host='localhost', port=8080, reloader=True, debug=True, autojson=False)

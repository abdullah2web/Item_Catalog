from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Catalog, MenuItem

app = Flask(__name__)

engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/catalog/<int:catalog_id>/menu/JSON')
def catalogMenuJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(MenuItem).filter_by(
        catalog_id=catalog_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/catalog/<int:catalog_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(catalog_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/catalog/JSON')
def catalogsJSON():
    catalogs = session.query(Catalog).all()
    return jsonify(catalogs=[r.serialize for r in catalogs])


# Show all catalogs
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    catalogs = session.query(Catalog).all()
    return render_template('index.html', catalogs=catalogs)


# Create a new catalog
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCatalog():
    if request.method == 'POST':
        newCatalog = Catalog(name=request.form['name'])
        session.add(newCatalog)
        session.commit()
        return redirect(url_for('showCatalogs'))
    else:
        return render_template('newCatalog.html')


# Edit a catalog
@app.route('/catalog/<int:catalog_id>/edit/', methods=['GET', 'POST'])
def editCatalog(catalog_id):
    editedCatalog = session.query(
        Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCatalog.name = request.form['name']
            return redirect(url_for('showCatalogs'))
    else:
        return render_template(
            'editCatalog.html', catalog=editedCatalog)


# Delete a catalog
@app.route('/catalog/<int:catalog_id>/delete/', methods=['GET', 'POST'])
def deleteCatalog(catalog_id):
    catalogToDelete = session.query(
        Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        session.delete(catalogToDelete)
        session.commit()
        return redirect(
            url_for('showCatalogs', catalog_id=catalog_id))
    else:
        return render_template(
            'deleteCatalog.html', catalog=catalogToDelete)


# Show a catalog menu
@app.route('/catalog/<int:catalog_id>/')
@app.route('/catalog/<int:catalog_id>/menu/')
def showMenu(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(MenuItem).filter_by(
        catalog_id=catalog_id).all()
    return render_template('menu.html', items=items, catalog=catalog)


# Create a new menu item
@app.route(
    '/catalog/<int:catalog_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(catalog_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], catalog_id=catalog_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showMenu', catalog_id=catalog_id))
    else:
        return render_template('newmenuitem.html', catalog_id=catalog_id)

    return render_template('newMenuItem.html')


# Edit a menu item
@app.route('/catalog/<int:catalog_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(catalog_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu', catalog_id=catalog_id))
    else:

        return render_template(
            'editmenuitem.html', catalog_id=catalog_id, menu_id=menu_id, item=editedItem)


# Delete a menu item
@app.route('/catalog/<int:catalog_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(catalog_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', catalog_id=catalog_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

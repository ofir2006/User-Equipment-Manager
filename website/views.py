from collections import UserList
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import User, itemPool, Item
from . import db
import json
from werkzeug.utils import secure_filename
import os


views = Blueprint('views', __name__)

@views.route("/", methods=['GET','POST'])
def index():
    error = ''
    user=''
    filename = ''
    itemList = []
    userList = []
    username = request.form.get('username')
    allitems = itemPool.query.all()
    for item in allitems:
        itemList.append(item.name)
    
    allusers = User.query.all()
    for i in allusers:
        userList.append(i.name.title())

    if request.method == 'POST':
            
        name = request.form.get('name')
        if name:
            name = name.lower()

        if not name:
            name = username

        user = User.query.filter_by(name=name).first()
        
        if not user:
            error = "User does not exist"
    
        itemName = request.form.get('inputitem')
        
        if itemName:
            error =''
            file = ''
            file = request.files['file']
            

            if file:
               filename = secure_filename(file.filename)
               dir_path = os.path.dirname(os.path.realpath(__file__))
               file.save(dir_path + '/static/uploads/'+ filename)

           
            owner = User.query.filter_by(name=username).first()
            notes = request.form.get('notes')
            item = Item(name=itemName, notes = notes, createdBy=current_user.firstName +' '+ current_user.lastName, belongsTo=owner.id, fileName=filename)
            db.session.add(item)
            db.session.commit()
            flash("Item added!", category="success")
    
    if current_user.is_authenticated:
        return render_template("home.html", owner = user,  user=current_user, error=error, itemlist = itemList, userlist = userList, page='home')

    
    return redirect("/login")

@views.route('/item-management', methods=['GET','POST'])
def management():
    items = itemPool.query.all()
    itemList = []
    itemToAdd = None

    for item in items:
        itemList.append(item.name.lower())
    

    if request.method == 'POST':

        itemToAdd = request.form.get('itemname')
        item = itemPool(name = itemToAdd)

        if itemToAdd.lower() in itemList:
            flash("Item already exists!", category="error")

        elif itemToAdd is not None:
            flash('Item added successfully!', category="success")
            db.session.add(item)
            db.session.commit()
    
        return redirect('/item-management')



    return render_template('items.html', items=items, user=current_user, page='item')

@views.route('/delete-item', methods=['POST'])
def deleteitem():
    data = json.loads(request.data)
    itemId = data['itemId']
    item = itemPool.query.get(itemId)
    userItem = Item.query.get(itemId)
    
    if item:
        db.session.delete(item)
        db.session.commit()
    elif userItem:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fullPath = dir_path + '/static/uploads/' + userItem.fileName
        if os.path.isfile(fullPath):
            os.remove(fullPath)
        db.session.delete(userItem)
        db.session.commit()
    
    return jsonify({})

@views.route('/delete-user', methods=['POST'])
def deleteuser():
    data = json.loads(request.data)
    userId = data['userId']
    user = User.query.get(userId)
    
    if user:
        db.session.delete(user)
        db.session.commit()
    return jsonify({})


@views.route('/user-management', methods=['GET','POST'])
def userManagement():

    users = User.query.all()
    userList = []

    for user in users:
        userList.append(user.name.lower())

    userToAdd = None
    
    if request.method == 'POST':
        userToAdd = request.form.get('user-name')
    
        if userToAdd.lower() in userList:
            flash('User already exists!', category='error')

        elif userToAdd is not None:
            item = User(name = userToAdd.lower())
            db.session.add(item)
            db.session.commit()

            return redirect('/user-management')    
    
    return render_template('user-management.html', users=users, user=current_user, page='user')

@views.route('/additem', methods=['GET','POST'])
def additem():
    


    return render_template('user-management.html', user=current_user)



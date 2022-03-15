import bs4
from flask import Flask, render_template, redirect, request, url_for
import os
from pathlib import Path
from configs.config import Development, Production
from flask_sqlalchemy import SQLAlchemy
from utils.file_upload import FileUpload
import pandas as pd
import ntpath
from bs4 import BeautifulSoup

UPLOAD_FOLDER = os.getcwd() + '/data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_object(Development)
# app.config.from_object(Production)

db = SQLAlchemy(app)

# import models
from models.product import Product

@app.before_first_request
def create():
    db.create_all()

@app.route('/add-product', methods=["GET", "POST"])
def add_product():

    if request.method == 'POST':
        product_name = request.form["product_name"]
        quantity = request.form["quantity"]
        buying_price =  int(request.form["buying_price"])
        selling_price = int(request.form["selling_price"])

        # calculate the profit and percentage profit

        profit = selling_price - buying_price
        percentage_profit = (profit/buying_price) * 100

        product = Product(product_name=product_name, quantity=quantity, 
                          buying_price = buying_price, selling_price=selling_price, profit=profit, 
                          percentage_profit = percentage_profit)

        db.session.add(product)
        db.session.commit()
        print("product added successfully")
        return redirect(url_for('products'))


    return render_template('addproduct.html')

@app.route('/', methods =['GET', 'POST'])
def products():
    
    products = Product.query.filter().all()

    return render_template("index.html", products=products)

@app.route('/upload-data', methods=["GET", "POST"])
def upload_data():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        
        filename = FileUpload.dump_file(file=file)

        # read the data
        data = FileUpload.read_file(filename=filename)

        print(data)

        if data: 

            if data["filename_extension"] == "csv":
                csvData = pd.read_csv(data["file"])

                for each, row in csvData.iterrows():
                    # save the data to a database

                    profit = int(row['selling_price']) - int(row['buying_price'])
                    percentage_profit = (profit/row['buying_price']) * 100


                    product = Product( 
                        product_name=row['product_name'],
                        buying_price = row['buying_price'],
                        selling_price = row['selling_price'],
                        quantity = row['quantity'],
                        profit = profit,
                        percentage_profit = percentage_profit
                    )

                    db.session.add(product)
                    db.session.commit()
                    print("product saved successfully")

                # delete the file

            if data["filename_extension"] == "json":

                jsonData = pd.read_json(data["file"])

                for each, row in jsonData.iterrows():
                    # save the data to a database

                    profit = int(row['selling_price']) - int(row['buying_price'])
                    percentage_profit = (profit/row['buying_price']) * 100


                    product = Product( 
                        product_name=row['product_name'],
                        buying_price = row['buying_price'],
                        selling_price = row['selling_price'],
                        quantity = row['quantity'],
                        profit = profit,
                        percentage_profit = percentage_profit
                    )

                    db.session.add(product)
                    db.session.commit()
                    print("product saved successfully")

                    # delete file

            # if data["filename_extension"] == "xml":

            #     bs_data = BeautifulSoup(data, 'xml')

            #     b_unique = bs_data.find_all('record')

            #     for each in b_unique:
            #         if type(each) is not bs4.element.NavigableString:
                        
            #             profit = int(each.selling_price.text) - int(each.buying_price.text)
            #             percentage_profit = (profit/ int(each.buying_price.text)) * 100

            #             product = Product( 
            #                 product_name=each.product_name.text,
            #                 buying_price = each.buying_price.text,
            #                 selling_price = each.selling_price.text,
            #                 quantity = each.quantity.text,
            #                 profit = profit,
            #                 percentage_profit = percentage_profit
            #             )
            #             db.session.add(product)
            #             db.session.commit()
            #             print("Product added successfully")

    return render_template("upload.html")

@app.route('/read-file')
def read_file():

    # data = FileUpload.read_file("MOCK_DATA.csv")

    data_folder = Path(os.getcwd() + '/data')

    print(data_folder)
    
    

    # check the file extensions

    

    return render_template('read.html')

@app.route('/visualization')
def visualization():

    products = Product.query.filter().all()

    print(products)

    return render_template('visualization.html')

# update product
@app.route('/update/<int:id>', methods=['POST'])
def update_product(id):

    if request.method == "POST":
        product_name = request.form["product_name"]
        quantity = request.form["quantity"]
        buying_price = int(request.form["buying_price"])
        selling_price = int(request.form["selling_price"])
        profit = selling_price - buying_price
        percentage_profit = (profit/buying_price) * 100

        Product.update_by_id(id=id, product_name=product_name, 
                            quantity=quantity, buying_price=buying_price,
                            selling_price=selling_price,
                            profit=profit, percentage_profit=percentage_profit)

        print("record updated successfully")
        return redirect(url_for("products"))

    return redirect(url_for('upload_file'))


# deleting a product
@app.route('/delete/<int:id>', methods=['GET','POST'] )
def deleteProduct(id):

    # fetch product first
    delete_product = Product.delete_product(id=id)

    if delete_product:
        print('Record deleted successfully')
        return redirect(url_for('upload_file'))
    else:

        print('record not found')
        return redirect(url_for('upload_file'))


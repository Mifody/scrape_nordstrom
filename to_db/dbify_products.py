'''
Add Product JSON to DB
'''

import argparse
import json
import dataset

def get_db(args):
    sqlite_path = 'sqlite:///{0}'.format(args.db)
    db = dataset.connect(sqlite_path)
    return db

def inflat_product(p_json):
    product = {}
    product['id'] = p_json['json']['StyleNumber']
    product['url'] = p_json['url']
    product['price'] = p_json['json']['Prices'][0]['MinItemPrice']
    return product

def add_product(table, product):
    table.upsert(product, ['id'])

def read_products(p_filename):
    print('reading products from {0}'.format(p_filename))
    new_products = []
    with open(p_filename) as p_file:
        json_data = json.load(p_file)
        for p_json in json_data:
            product = inflat_product(p_json)
            new_products.append(product)
    return new_products

def add_new_products(table, products):
    id_column = table.distinct('id')
    print('{0} total products'.format(str(len(products))))

    sorted_products = sorted(products, key=lambda x: x['id'])
    filtered_new_products = []

    if len(sorted_products) > 0:
        filtered_new_products.append(sorted_products[0])

    for prod in sorted_products:
        if prod['id'] > filtered_new_products[-1]['id']:
            filtered_new_products.append(prod)
    print('{0} unique products'.format(str(len(filtered_new_products))))

    existing_ids = [val['id'] for val in id_column]
    print('{0} existing products'.format(str(len(existing_ids))))
    
    new_products = [p for p in filtered_new_products if p['id'] not in existing_ids]
    print('{0} new products'.format(str(len(new_products))))

    table.insert_many(new_products)

    # for prod in new_products:
    #     if prod['id'] not in ids:
    #         filtered_new_products.append(prod)
    #         ids.append(prod['id'])



def add_products(db, p_filename):
    product_table = db['product']
    price_table = db['price']
    new_products = read_products(p_filename)
    add_new_products(product_table, new_products)


def setup_tables(db):
    tables = db.tables
    if 'product' not in tables:
        print('creating product table')
        db.create_table('product', primary_id='id', primary_type='String')
    if 'price' not in tables:
        print('creating prices table')
        db.create_table('price', primary_id='id', primary_type='String')
    return db


def main(args):
    db = get_db(args)
    setup_tables(db)
    add_products(db, args.json)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--db', help='Database to add products to')
    parser.add_argument('--json', help='JSON of products to add')

    args = parser.parse_args()

    main(args)

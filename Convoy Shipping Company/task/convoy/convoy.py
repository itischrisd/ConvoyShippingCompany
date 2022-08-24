import json
import re
import pandas as pd
import sqlite3
from lxml import etree

filename = ""
filename_stripped = ""
dataframe = pd.DataFrame()

def prompt_name():
    global filename, filename_stripped
    print("Input file name")
    filename = str(input())
    filename_stripped = filename\
        .removesuffix('.xlsx')\
        .removesuffix('.csv')\
        .removesuffix('[CHECKED]')\
        .removesuffix('.s3db')

def import_data():
    global filename, dataframe
    if filename.endswith('.xlsx'):
        dataframe = pd.read_excel(filename, sheet_name='Vehicles', dtype=str)
    elif filename.endswith('.csv'):
        dataframe = pd.read_csv(filename)
    elif filename.endswith('.s3db'):
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        if len(list(pd.DataFrame(cursor.execute('SELECT * FROM convoy;')).head())) == 5:
            dataframe = pd.DataFrame(cursor.execute('SELECT * FROM convoy;'), columns=["vehicle_id", "engine_capacity", "fuel_consumption", "maximum_load", "score"])
        else:
            dataframe = pd.DataFrame(cursor.execute('SELECT * FROM convoy;'), columns=["vehicle_id", "engine_capacity", "fuel_consumption", "maximum_load"])
        connection.commit()
        connection.close()
    else:
        print("FILE NOT RECOGNISED")


def convert_xlsx():
    global filename, filename_stripped, dataframe
    if filename.endswith('.xlsx'):
        if len(dataframe.index) == 1:
            print(f'{len(dataframe.index)} line was added to {filename_stripped}.csv')
        else:
            print(f'{len(dataframe.index)} lines were added to {filename_stripped}.csv')
        dataframe.to_csv(filename_stripped + '.csv', index=False, header=True)

def cleanup_csv():
    global filename_stripped, dataframe
    count = 0
    item_list = dataframe.values.tolist()
    for item in item_list:
        for cell in item:
            if re.match('^\D*\d+\D*$', str(cell)) is not None and re.match('^\d+$', str(cell)) is None:
                item[item.index(cell)] = re.search('\d+', cell).group(0)
                count += 1
    if count != 0:
        pd.DataFrame(item_list, columns=list(dataframe)).to_csv(filename_stripped + '[CHECKED].csv', index=False, header=True)
    if count == 1:
        print(f'{count} cell was corrected in {filename_stripped}[CHECKED].csv')
    elif count > 1:
        print(f'{count} cells were corrected in {filename_stripped}[CHECKED].csv')
    dataframe = pd.DataFrame(item_list, columns=list(dataframe))

def export_to_db():
    global filename, filename_stripped, dataframe
    connection = sqlite3.connect(filename_stripped + '.s3db')
    cursor = connection.cursor()
    header = list(dataframe.head())
    if len(list(dataframe.head())) == 5:
        return
    if filename.endswith('.s3db'):
        cursor.execute('DROP TABLE convoy')
    cursor.execute('CREATE TABLE convoy (' +
                        header[0] + ' INTEGER PRIMARY KEY,' +
                        header[1] + ' INTEGER NOT NULL,' +
                        header[2] + ' INTEGER NOT NULL,' +
                        header[3] + ' INTEGER NOT NULL,' +
                        ' score INTEGER NOT NULL);')
    record_list = dataframe.values.tolist()
    count = 0
    for record in record_list:
        count += 1
        cursor.execute('INSERT INTO convoy VALUES (' +
                            str(record[0]) + ', ' +
                            str(record[1]) + ', ' +
                            str(record[2]) + ', ' +
                            str(record[3]) + ', ' +
                            str(get_score(record)) + ');')
    cursor = connection.cursor()
    dataframe = pd.DataFrame(cursor.execute('SELECT * FROM convoy;'),
                             columns=["vehicle_id", "engine_capacity", "fuel_consumption", "maximum_load", "score"])
    connection.commit()
    connection.close()
    if count == 1:
        print(f'{count} record was inserted into {filename_stripped}.s3db')
    else:
        print(f'{count} records were inserted into {filename_stripped}.s3db')

def export_to_json():
    global filename_stripped, dataframe
    record_dict = {"convoy": []}
    record_list = dataframe.values.tolist()
    header = list(dataframe.head())
    count = 0
    for record in record_list:
        if int(record[4]) < 4:
            continue
        count += 1
        record_dict["convoy"].append({header[0]: record[0], header[1]: record[1], header[2]: record[2], header[3]: record[3]})
    with open(filename_stripped + ".json", "w") as json_file:
        json.dump(record_dict, json_file, indent=4)
    if count == 1:
        print(f'{count} vehicle was saved into {filename_stripped}.json')
    else:
        print(f'{count} vehicles were saved into {filename_stripped}.json')

def export_to_xml():
    global filename_stripped, dataframe
    xml_string = "<convoy>"
    record_list = dataframe.values.tolist()
    header = list(dataframe.head())
    count = 0
    for record in record_list:
        if int(record[4]) > 3:
            continue
        count += 1
        xml_string += "<vehicle>"
        xml_string += "<" + header[0] + ">" + str(record[0]) + "</" + header[0] + ">"
        xml_string += "<" + header[1] + ">" + str(record[1]) + "</" + header[1] + ">"
        xml_string += "<" + header[2] + ">" + str(record[2]) + "</" + header[2] + ">"
        xml_string += "<" + header[3] + ">" + str(record[3]) + "</" + header[3] + ">"
        xml_string += "</vehicle>"
    xml_string += "</convoy>"
    root = etree.fromstring(xml_string)
    tree = etree.ElementTree(root)
    tree.write(filename_stripped + ".xml", method='html')
    if count == 1:
        print(f'{count} vehicle was saved into {filename_stripped}.xml')
    else:
        print(f'{count} vehicles were saved into {filename_stripped}.xml')

def get_score(vehicle):
    score = 0
    fuel_burned = 4.5 * float(vehicle[2])
    pitstop = fuel_burned / float(vehicle[1])
    if pitstop < 1:
        score += 2
    elif pitstop < 2:
        score += 1
    if fuel_burned > 230:
        score += 1
    else:
        score += 2
    if int(vehicle[3]) >= 20:
        score += 2
    return score


prompt_name()
import_data()
convert_xlsx()
cleanup_csv()
export_to_db()
export_to_json()
export_to_xml()
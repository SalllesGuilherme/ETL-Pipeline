#  FEUP - Master in Data Science and Engineering 2021
#  FCED - Databases
# 
#  Ana Catarina Mesquita
#  Filipe Dória
#  Guilherme Salles
#
#  https://dbm.fe.up.pt/phppgadmin/

import psycopg2
import pandas as pd
import csv

# con = psycopg2.connect(
#    database="fced_guilherme_salles",             # your database is the same as your username
#    user="fced_guilherme_salles",    # your username admin
#    password="admin",             # your password
#    host="dbm.fe.up.pt",             # the database host
#    port="5433",
#    options='-c search_path=employees'  # use the schema you want to connect to
# )


def delete_all(con,table):
    cur = con.cursor()
    cur.execute(f"DELETE FROM {table}")
    con.commit()


def insert_countries_db (con):

    cur = con.cursor()
    file = open('countries of the world.csv')
    csvreader = csv.reader(file)
    rows = []

    for row in csvreader:

        for i in range(len(row)):
            row[i] = row[i].replace(",",".")
            if row[i] == "":
                row[i] = 'Null'
        if row != []:
            country_name=row[0]
            region=row[1]
            population=row[2]
            area=row[3]
            population_des=row[4]
            coastline=row[5]
            net_migration=row[6]
            infant_mortality=row[7]
            GDP=row[8]
            literacy=row[9]
            phones=row[10]
            arable=row[11]
            crops=row[12]
            other=row[13]
            climate=row[14]
            birthrate=row[15]
            deathrate=row[16]
            agriculture=row[17]
            industry=row[18]
            service=row[19]

            if country_name == "Cote d'Ivoire ":
                country_name ='Ivory coast'

            if country_name != "Country":
              cur.execute(f"INSERT INTO country VALUES ('{country_name}','{region}',{population},{area},{population_des},{coastline},{net_migration},{infant_mortality},{GDP},{literacy},{phones},{arable},{crops},{other},{climate},{birthrate},{deathrate},{agriculture},{industry},{service});")
    con.commit()


def insert_countries_pandas_db(con):
    df = pd.read_csv('countries of the world.csv')

    #Correct the missing values per null
    df = df.fillna('Null')
    df.columns = ['country_name', 'region', 'population', 'area', 'population_des','coastline','net_migration','infant_mortality','GDP','literacy','phones','arable','crops','other','climate','birthrate','deathrate','agriculture','industry','service']

    #Correct name of the country which has an especial char on world country list
    #all the other corrections were made on happiness code.
    df["country_name"].replace({"Cote d'Ivoire ": "Ivory Coast",  "Bosnia & Herzegovina ": "Bosnia and Herzegovina", "Trinidad & Tobago ":"Trinidad and Tobago"}, inplace=True)

    #Convert decimal comman to decimal dot in order to perform the database import
    country=df['country_name']
    population = df['population']
    area = df['area']
    GDP = df['GDP']
    df = df.stack().str.replace(',', '.').unstack()
    df['population'] = population
    df['area'] = area
    df['GDP'] = GDP
    df['country_name'] = country

    cur = con.cursor()
    for l in df.itertuples():
        country = l.country_name.strip()
        region = l.region.strip()
        cur.execute(f"INSERT INTO country VALUES ('{country}','{region}',{l.population},{l.area},{l.population_des},{l.coastline},{l.net_migration},{l.infant_mortality},{l.literacy},{l.phones},{l.arable},{l.crops},{l.other},{l.climate},{l.birthrate},{l.deathrate},{l.agriculture},{l.industry},{l.service});")

    con.commit()
    print(f"3 correction has been made on country name:")
    print(f" - From Cote d'Ivoire to Ivory Coast ")
    print(f" - From Bosnia & Herzegovina to Bosnia and Herzegovina")
    print(f" - From Trinidad & Tobago to Trinidad and Tobago\n")

def select_db(con,query):
    cur = con.cursor()
    cur = con.cursor()
    cur.execute(f"{query}")
    country = cur.fetchall()
    for row in country:
        print (row)

def rollback_db(con):
    cur = con.cursor()
    cur.execute("ROLLBACK")
    con.commit()

def create_table_country(con):
    cur = con.cursor()
    cur.execute(f"SET search_path to country;")
    cur.execute(f"CREATE TABLE country (country_name text   NOT NULL, region text ,population int ,area int ,population_des numeric ,coastline numeric ,net_migration numeric  ,infant_mortality numeric ,literacy numeric ,phones numeric ,arable numeric ,crops numeric ,other numeric ,climate int ,birthrate numeric ,deathrate numeric ,agriculture numeric ,industry numeric ,service numeric , CONSTRAINT pk_Country PRIMARY KEY (country_name ));")
    con.commit()

def connect_local():
    con = psycopg2.connect(
         database="db_report",  # your database is the same as your username
         user="db_report",  # your username admin
         password="db_report",  # your password
         host="localhost",  # the database host
         port="5409", # the defined database port
         options='-c search_path=country'  # use the schema you want to connect to
     )
    print(f"Establishing connection with local database...")
    return con

def connect_feup():
    con = psycopg2.connect(
        database="fced_guilherme_salles",  # your database is the same as your username
        user="fced_guilherme_salles",  # your username admin
        password="admin",  # your password
        host="dbm.fe.up.pt",  # the database host
        port="5433",
        options='-c search_path=country'  # use the schema you want to connect to
    )
    print(f"Establishing connection with Feup database...")
    return con

if __name__ == "__main__":

    #conn = connect_feup()
    conn = connect_local()
    print(f"Starting to load countries dataset to database...")
    print("Cleaning old records...")

    try:
        delete_all(conn, 'country')

    except psycopg2.errors.ForeignKeyViolation:
        print(f"\nWarning: Failure on delete row, it violates foreign key constraint")
        print(f"Warning: Data on table score it will be deleted in order to perform import,so please insert again later\n")
        rollback_db(conn)
        delete_all(conn, 'score')
        delete_all(conn, 'country')

    except psycopg2.errors.UndefinedTable:
        rollback_db(conn)
        create_table_country(conn)
        print("Table Country created")

    print("Importing csv file to database...\n")

    try:
        insert_countries_pandas_db(conn)
        print("Import data operation concluded successfully!")

    except psycopg2.errors.InFailedSqlTransaction:
        print('ALERT: Failed to insert data!')
        print('Import data operation canceled!')





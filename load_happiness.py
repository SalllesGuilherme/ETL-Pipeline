#  FEUP - Master in Data Science and Engineering
#  Ana Catarina Mesquita
#  Filipe Dória
#  Guilherme Salles
#https://dbm.fe.up.pt/phppgadmin/

import pandas as pd
import psycopg2
import sys


def delete_happiness_year(con,year):
    cur = con.cursor()
    cur.execute(f"DELETE FROM score where year={year}")
    con.commit()

def delete_happiness_all(con):
    cur = con.cursor()
    cur.execute(f"DELETE FROM score")
    con.commit()

def import_happiness_year(con,year,csv_file):

    df = pd.read_csv(csv_file)
    #Rename columns
    if year == 2015:
        df.columns = ['country', 'region', 'happiness_rank', 'happiness_score', 'standart_error', 'economy', 'family',
                       'health', 'freedom', 'trust_perp_corruption', 'generosity', 'dystopia_residual']
    elif year == 2016:
        df.columns = ['country', 'region', 'happiness_rank', 'happiness_score', 'low_ci','upper_ci' , 'economy', 'family',
                      'health', 'freedom', 'trust_perp_corruption', 'generosity', 'dystopia_residual']
    elif year == 2017:
        df.columns = ['country', 'happiness_rank', 'happiness_score', 'whisker_hi','whisker_lo' , 'economy', 'family',
                      'health', 'freedom','generosity', 'trust_perp_corruption', 'dystopia_residual']
    elif year == 2018:
        df.columns = ['happiness_rank', 'country', 'happiness_score', 'economy', 'social_support',
                      'health', 'freedom', 'generosity', 'trust_perp_corruption']
    elif year == 2019:
        df.columns = ['happiness_rank', 'country', 'happiness_score', 'economy', 'social_support',
                      'health', 'freedom', 'generosity', 'trust_perp_corruption']

    #correct names of countries
    df["country"].replace({"Congo (Kinshasa)": "Congo, Dem. Rep.", "Congo (Brazzaville)": "Congo, Repub. of the","Hong Kong S.A.R., China":"Hong Kong",
                           "Central African Republic":"Central African Rep." , "Trinidad & Tobago":"Trinidad and Tobago" , "Gambia":"Gambia, The",
                           "Bosnia & Herzegovina ": "Bosnia and Herzegovina" , "South Korea":"Korea, South","Taiwan Province of China":"Taiwan"}, inplace=True)

    #remove some countries from list
    list_to_remove = [ 'North Cyprus','Northern Cyprus','North Macedonia','Kosovo','Montenegro','Somaliland Region','Somaliland region','South Sudan','Palestinian Territories','Myanmar']
    for country_item in list_to_remove:
        r = df[df.country == country_item].index
        df = df.drop(r)

    #Go though the row of the dataframe and perform a insert on the database table
    cur = con.cursor()
    for l in df.itertuples():
        cur.execute(f"INSERT INTO score VALUES ('{l.country}',{l.happiness_rank},{l.happiness_score},{l.economy},{year});")
    con.commit()

    #Funtion to print text. It prints the countries that corrected/removed in each file.
def print_country_corrected(year):
    if year == 2015:
        print(f"\nADJUSTED:")
        print(f"4: Congo (kinshana) , Congo (Brazzaville), Central African Repuplic, South Korea ")
        print(f"REMOVED:")
        print(f"6: North Cyprus , Kosovo, Montenegro, Somaliland region, Palestinian Territories, Myanmar\n")
    elif year == 2016:
        print(f"\nADJUSTED:")
        print(f"3: Congo (kinshana) , Congo (Brazzaville), South Korea ")
        print(f"REMOVED:")
        print(f"7: North Cyprus , Kosovo, Montenegro, Somaliland region, South Sudan, Palestinian Territories, Myanmar\n")
    elif year == 2017:
        print(f"\nADJUSTED:")
        print(f"6: Taiwan, Hong Kong, Congo (kinshana) , Congo (Brazzaville), South Korea ,  Central African Repuplic ")
        print(f"REMOVED:")
        print(f"6: North Cyprus , Kosovo, Montenegro, South Sudan, Palestinian Territories, Myanmar\n")
    elif year == 2018:
        print(f"\nADJUSTED:")
        print(f"4:  Congo (kinshana) , Congo (Brazzaville), South Korea ,  Central African Repuplic ")
        print(f"REMOVED:")
        print(f"6: Northern Cyprus , Kosovo, Montenegro, South Sudan, Palestinian Territories, Myanmar\n")
    elif year == 2019:
        print(f"\nADJUSTED:")
        print(f"5:  Congo (kinshana) , Congo (Brazzaville), South Korea ,  Central African Repuplic, Gambia ")
        print(f"REMOVED:")
        print(f"6: Northern Cyprus , Kosovo, Montenegro, South Sudan, Palestinian Territories, Myanmar, North Macedonia\n")

#Function to perform a rollback in case of error on postgreeSQL.
def rollback_db(con):
    cur = con.cursor()
    cur.execute("ROLLBACK")
    con.commit()

# Function to create score table
def create_table_score(con):
    cur = con.cursor()
    cur.execute(f"SET search_path to country;")
    cur.execute(f"CREATE TABLE score (country_name text   NOT NULL, happiness_rank int  NOT NULL,happiness_score numeric   NOT NULL,GDP money   NOT NULL, year SMALLINT   NOT NULL, UNIQUE (country_name, year));")
    cur.execute(f"ALTER TABLE score ADD CONSTRAINT fk_Score_country_name FOREIGN KEY(country_name) REFERENCES country (country_name);")
    con.commit()

def connect_local():
    con = psycopg2.connect(
         database="db_report",  # your database is the same as your username
         user="db_report",  # your username admin
         password="db_report",  # your password
         host="localhost",  # the database host
         port=5409, #your database access port 
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
#for year in ([2015,2016,2017,2018,2019]):

    year = int(sys.argv[1])
    csv_file =  str(sys.argv[2])

    #csv_file = f"wh-{year}.csv"

    if year != int(csv_file[3:7]):
        print('\nWarning:Values inserted as arguments has a different year, please check it\n')
        csv_file = f"wh-{year}.csv"
        print(f"\nWarning:The program wil consider the year {year} for proceed with importation\n")


    #conn = connect_feup()
    conn = connect_local()
    print(f"\nStarting to load happiness dataset {year} to database...")

    print("Cleaning old records...")

    try:
        delete_happiness_year(conn, year)
    except:
       rollback_db(conn)
       create_table_score(conn)
       print("Table score created")

    print("Importing csv file to database...")
    import_happiness_year(conn,year,csv_file)
    print_country_corrected(year)

    print(f"Import data from {year} concluded successfully!")









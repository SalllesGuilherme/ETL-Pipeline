#  FEUP - Master in Data Science and Engineering 2021
#  FCED - Databases
#  
#  Ana Catarina Mesquita
#  Filipe Dória
#  Guilherme Salles

import pandas as pd
import csv

## Funtion for compare similar words on a list
# it compares words between two lists, and identifies the words that are present on list1, but it aren't found on list2.

def compare_list(wordlist1,wordlist2):
    elements_matched=[]
    elements_notfound = []

    for i in range(len(wordlist1)):
        word_found=1

        for j in range(len(wordlist2)):
            word1_i= wordlist1[i]
            word2_j= wordlist2[j]

            sorted_word1_i = ''.join(sorted(word1_i)).strip()
            sorted_word2_j = ''.join(sorted(word2_j)).strip()

            if sorted_word1_i == sorted_word2_j:
                elements_matched.append(wordlist1[i])
                word_found=1     #Found same word
                break
            else:
                word_found=0

        if word_found == 0: # If after the loop it don't find a match, it stores in a different list
            elements_notfound.append(wordlist1[i])

    return(elements_notfound)

if __name__ == "__main__":

    #Load countries world dataset
    df = pd.read_csv('countries of the world.csv')

    #Get the Countries names from dataset
    country_world_list= df['Country'].unique()

    #combine all year in a list
    happines_list_year = [2015,2016,2017,2018,2019]

    #Uses the fuction compare_list to generate a output of not match contries
    # per year on the Happiness country dataset.

    with open('output/output-compare-countries.txt', 'w',encoding='utf-8') as f:

        #writer = csv.writer(f)
        for list_year in happines_list_year:

            csv_file = f"wh-{list_year}.csv"
            df_happiness=pd.read_csv(csv_file)

            if list_year in ([2015,2016,2017]):
                countries_happy_list = df_happiness['Country'].unique()
            elif list_year in ([2018,2019]):
                countries_happy_list = df_happiness['Country or region'].unique()

            notfoundcountries = compare_list(countries_happy_list,country_world_list)

            print(f"Countries to be removed or corrected on year {list_year}:")
            f.write(f"Countries to be removed or corrected on year {list_year}:\n")
            for item in notfoundcountries:
                print(f"{item} ")
                f.write(f"{item} \n")
            print(f"{len(notfoundcountries)} total countries")
            f.write(f"{len(notfoundcountries)} total countries\n")
            print(f"_________________________________________________________\n")
            f.write(f"_________________________________________________________\n")




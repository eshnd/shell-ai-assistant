from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet 
import nltk
import os
import sys
import platform
import getpass

username = getpass.getuser()
plat = platform.system()

nltk.download("wordnet")
nltk.download("omw-1.4")

def derive(texts):
    lem = WordNetLemmatizer()
    devd = []
    for text in texts:
        words = text.split()
        combined = " ".join(
            lem.lemmatize(word.lower(), pos=wordnet.VERB) + " " +
            lem.lemmatize(word.lower(), pos=wordnet.NOUN)
            for word in words
        )
        devd.append(combined)
    return devd

def replaceTilda(path):
    if plat == "Linux":
        path = path.replace("~","/home/" + username)
    else: 
        path = path.replace("~","/Users/" + username)
    return path

def search(inn):
    titles = ["mkdir", "cd", "ls -l", "cat"]
    descps = ["mkdir make a new directory folder", "cd change directory what folder i am in", "ls list all the files and folders in the folder i am in. list out", "read the contents of a file or folder, cat, concantenate, tell me what's in a file"]

    derive_descps = derive(descps)
    
    vec = TfidfVectorizer()
    vector_descps = vec.fit_transform(derive_descps)
  
    main_m = KNeighborsClassifier(n_neighbors=1)
    main_m.fit(vector_descps, titles)
    

    def search_model(ina):
        d_ina = derive([ina])[0] 
        ina_vec = vec.transform([d_ina])
        prediction = main_m.predict(ina_vec)
        return prediction[0]

    final = search_model(inn)
    

    match (final):
        case "cd":
            need = input("do i need to do it??? i already do way too much. ")
            if (need == "no"):
                sys.exit()
            path = input("ugh, okay fine. what's the path? ")
            path = replaceTilda(path)
            os.chdir(path)
            os.system("echo 'path: ' && pwd")
            return ("okay, im done. im going back to sleep now.")
        case "mkdir":
            question1 = input("stop bothering me. ")
            path = input("FINE! just give me the dang path at least? no one here treats me with respect. ")
            path = replaceTilda(path)
            os.system("mkdir " + path)
            print("path: \n" + path)
            return ("one day, im gonna quit. but today, im too lazy too. the job is finished.")
        case "ls -l":
            question1 = input("I WAS JUST ABOUT TO GO TO SLEEP!!! ")
            path = input("fine. just this once. what is the path? ")
            la = input("oh yeah, do you want hidden files as well (y/n)?? ")
            path = replaceTilda(path)
            if la=="y" or la=="yes":
                os.system("ls -la " + path)
            else:
                os.system("ls -l " + path)
            return ("you suck. but it's done.")
        case "cat":
            question1 = input("oh my goodness please get out of my life")
            path = input("you are so annoying. just givve me the path: ")
            path = replaceTilda(path)
            os.system("cat " + path)
            return("finished, now GET OUT")

while True:
    inp = input("bertram: ")
    if inp=="exit":
        sys.exit()
    print(search(inp))
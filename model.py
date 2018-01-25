import os
import pickle
from nltk import wordpunct_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
from nltk.stem import SnowballStemmer 
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.neighbors import  KNeighborsClassifier  as algo
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.model_selection import StratifiedKFold



class Preprocedo(BaseEstimator, TransformerMixin):
    
    
    def __init__(self, stopwords=None, punct=None, lower=True, strip=True):
       
        self.lower      = lower
        self.strip      = strip
        self.stopwords  = self.stopwor()
        self.steam = SnowballStemmer("spanish")
        
    def fit(self, X, y=None):
        
        return self

    def stopwor(self):
        with open('.'+os.path.sep+'utiliti'+os.path.sep+'stopWordsSpanish.txt','r') as stop_words: 
            lineas = [linea.strip() for linea in stop_words]
            
        return lineas
    def transform(self, X):
        
        return [
            list(self.tokenize(doc)) for doc in X
        ]

    def tokenize(self, document):
        
        n_grama=[]
        n_g=False
        n_grambol=False
        limpia=False
        auxn_grama=""
        
        # Rompemos el documento en lineas
        for sent in sent_tokenize(document):
            # Rompemos la line en tokens
            for token, tag in pos_tag(wordpunct_tokenize(sent)):
                # Aplicamos cada trasformacion a cada token
                token = token.lower() if self.lower else token
                token = token.strip() if self.strip else token
                token = token.strip('_') if self.strip else token
                token = token.strip('*') if self.strip else token
                #print("TOKEEEN     ",token)
                
                #Limpiamos todas las variables para volver a crear el array de 3 posiciones
                if(limpia==True):
                    n_grama=[]
                    n_g=False
                    n_grambol=False
                if(n_g==True):
                    n_grama=[]
                    n_g=False
                #print("TOKEEEN     ",token)
                if(len(n_grama)==0):
                    if (token=="violencia"):
                            auxn_grama="violencia"
                            n_grambol=True
                        #print("HOLAAAAAAAAAAA     ",n_grama[0])
                    else  : 
                        n_grama=[]         
                if(len(n_grama)==1):
                    if(token=="de"):
                        auxn_grama="de"
                        n_grambol=True
                    else :
                        n_grama=[]
                if(len(n_grama)==2):
                    if(token=="genero" or token=="género"):
                        n_g=True
                        auxn_grama="genero"
                        n_grambol=True
                    else :
                        n_grama=[]
                if( n_grambol==True):        
                    n_grama.append(auxn_grama)
                    n_grambol=False
                if(n_g==True):
                    #print("RETURRNNNNN     ",n_grama[0]+" "+n_grama[1]+" "+n_grama[2])
                    limpia=True;
                    yield n_grama[0]+n_grama[1]+n_grama[2]
                else :
                    
                    # Eliminamos las palabras que aparezcan en nuestra lista de parada 
                    if token not in self.stopwords: 
                        #Below code will remove all punctuation marks as well as non alphabetic characters
                        if  token.isalpha():
                            # Lematizamos cada token para quedarnos con la raiz 
                            stemm = self.steam.stem(token)
                            #print("LEEMMAAA     ",lemma)
                            yield stemm
def identity(arg):
    
    return arg  
 

                           
def crearModelo(X, y,names, classifier=algo, outpath=None, verbose=True):
   
    
    def build(classifier):
        
        if isinstance(classifier, type):
            classifier = classifier()

        model = Pipeline([
            ('preprocessor', Preprocedo()),
            ('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)),
            ('classifier', classifier),
        ])

       
        return model
    
    # Begin evaluation
    if verbose: print("Building for evaluation")
    #Creamos el objeto k_fold para poder dividir nuestro conjunto de noticias
    k_fold = StratifiedKFold(n_splits=5, random_state=None, shuffle=True)# shuffle =true ;mezclar cada estratificación de los datos antes de dividirlos en lotes
        
    #construimos el modelo
    model= build(classifier)
        
    predictions=[]
    reales=[]
    #Dividimos nuestros conjunto de datos , train _text indices de entrenamiento, test_index indices de testeo
    for train_index, test_index in k_fold.split(X,y):#puede pasarse un grupo 
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        #Entrenamos al modelo
        model.fit(X_train, y_train)
        #Testeamos las noticias de teste con el modelo entrenado y lo guardamos en el arry de prediciones
        for i in model.predict(X_test):
            predictions.append(i) 
        #Recorremos las mismas noticias sabiendo cual es su categoria y lo guardamos en reales
        for i in y_test:
            reales.append(i)
       
    if verbose: print("Classification Report:\n")
    
    print(classification_report(reales, predictions, target_names=names))
    
    if verbose: print("Complete model fit in {:0.3f} seconds")

    if outpath:
        print(outpath)
        with open(outpath, 'wb') as f:
            pickle.dump(model, f)

        print("Model written out to {}".format(outpath))
        
    return True




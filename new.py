import pandas as pd
import numpy as np
import nltk
import string
nltk.download('punkt')
from nltk.tokenize import word_tokenize
#have imported extracted file from file 1
text=pd.read_fwf("/Users/adityakumar/codes/internship/TitleText/123.0.txt",header=None)
text.info()
text.drop(1,axis=1,inplace=True)
text=text.astype(str)
#converting text to sentence
import re
# have splitted text on each '.'
a=text[0].str.split('([\.]\s)',expand=False)
#exploding a that is converting to rows
b=a.explode()
# creating data frame from pandas
b=pd.DataFrame(b)
b.columns=['abc']

#have removed punctuation . from each 
def abcd(x):    
    nopunc =[char for char in x if char != '.']
    return ''.join(nopunc)
b['abc']=b['abc'].apply(abcd)

#if null spaces in b replacing with null value
c=b.replace('',np.nan,regex=True)
c=c.mask(c==" ")

c=c.dropna()
#dropping empty valuee
c.reset_index(drop=True,inplace=True)
print(c)
punc=[punc for punc in string.punctuation]
print(punc)
auditor=pd.read_fwf("/Users/adityakumar/codes/internship/StopWords/StopWords_Auditor.txt",header=None)
currencies=pd.read_fwf("/Users/adityakumar/codes/internship/StopWords/StopWords_Currencies.txt",header=None,encoding="ISO-8859-1",sep='\n' )
datesandNumbers=pd.read_fwf("/Users/adityakumar/codes/internship/StopWords/StopWords_DatesandNumbers.txt",header=None)
generic=pd.read_fwf("/Users/adityakumar/codes/internship/StopWords/StopWords_Generic.txt",header=None)
GenericLong=pd.read_fwf("/Users/adityakumar/codes/internship/StopWords/StopWords_GenericLong.txt",header=None)
Geographic=pd.read_fwf("/Users/adityakumar/codes/internship/StopWords/StopWords_Geographic.txt",header=None)
Names=pd.read_fwf("/Users/adityakumar/codes/internship/StopWords/StopWords_Names.txt",header=None)
def text_process(text):
    nopunc =[char for char in text if char not in punc or char not in [':',',','(',')','’','?']]
    nopunc=''.join(nopunc)
    #auditor
    txt=' '.join([word for word in nopunc.split() if word.lower() not in auditor])
    #Currencies
    txt1=' '.join([word for word in txt.split() if word.lower() not in currencies])
    #dataandnumbers
    txt2=' '.join([word for word in txt1.split() if word.lower() not in datesandNumbers])
    #generic
    txt3=' '.join([word for word in txt2.split() if word.lower() not in generic])

    txt4=' '.join([word for word in txt3.split() if word.lower() not in GenericLong])
    txt5=' '.join([word for word in txt4.split() if word.lower() not in Geographic])
    return ' '.join([word for word in txt5.split() if word.lower() not in Names])
#applying text_process on 'abc'
c['abc']=c['abc'].apply(text_process)
print(c)
#reading files for positive
positive=pd.read_fwf("/Users/adityakumar/codes/internship/MasterDictionary/positive-words.txt",header=None)
#reading file for negative 
negative=pd.read_fwf("/Users/adityakumar/codes/internship/MasterDictionary/negative-words.txt",header=None,encoding="ISO-8859-1",sep='\n' )

positive.columns=['abc']
negative.columns=['abc']
positive['abc']=positive['abc'].astype(str)
negative['abc']=negative['abc'].astype(str)
positive['abc']=positive['abc'].apply(text_process)
negative['abc']=negative['abc'].apply(text_process)
length=positive.shape[0]
post=[]
#removing '+' in positive
for i in range(0,length):
   nopunc =[char for char in positive.iloc[i] if char not in string.punctuation or char != '+']
   nopunc=''.join(nopunc)

   post.append(nopunc)
length=negative.shape[0]
neg=[]
#removing '-' in negative
for i in range(0,length):
  nopunc =[char for char in negative.iloc[i] if char not in string.punctuation or char != '+']
  nopunc=''.join(nopunc)
  neg.append(nopunc)
txt_list=[]

length=c.shape[0]
for i in range(0,length):
  txt=' '.join([word for word in c.iloc[i]])
  txt_list.append(txt)
tokenize_text=[]
for i in txt_list:
  
  tokenize_text+=(word_tokenize(i))
#printing tokenize text
print(tokenize_text)
#printing len tokenize text
print(len(tokenize_text))
positive_score=0 
#updating positive score for every tokenize text text found in positive
for i in tokenize_text:
  if(i.lower() in post):
    positive_score+=1

print('postive score=', positive_score)
#updating negative score for every tokenize text text found in negative
negative_score=0
for i in tokenize_text:
  if(i.lower() in neg):
    negative_score+=1
print('negative score=', negative_score)


Polarity_Score=(positive_score-negative_score)/((positive_score+negative_score)+0.000001)
print('polarity_score=', Polarity_Score)
subjectiivity_score=(positive_score-negative_score)/((len(tokenize_text))+ 0.000001)
print('subjectivity_score',subjectiivity_score)
length=c.shape[0]
avg_length=[]
for i in range(0,length):
  avg_length.append(len(c['abc'].iloc[i]))
avg_senetence_length=sum(avg_length)/len(avg_length)
print('avg sentence length=', avg_senetence_length)
#complex word
def complexword(tokenize_text):
   
    vowels=['a','e','i','o','u']

    count=0
    complex_Word_Count=0
    for i in tokenize_text:
        x=re.compile('[es|ed]$')
        if x.match(i.lower()):
            count+=0
        else:
            for j in i:
                if(j.lower() in vowels ):
                    count+=1
    if(count>2):
        complex_Word_Count+=1
        count=0
    Percentage_of_Complex_words=complex_Word_Count/len(tokenize_text)
    return Percentage_of_Complex_words
print("complex word"+str(complexword(tokenize_text)))

print('percentag of complex words= '+str(complexword(tokenize_text)))
Fog_Index = 0.4 * (avg_senetence_length +complexword(tokenize_text))
print('fog index= ',Fog_Index )
length=c.shape[0]
avg_length=[]
for i in range(0,length):
  a=[word.split( ) for word in c.iloc[i]]
  avg_length.append(len(a[0]))
  a=0
#avg
avg_no_of_words_per_sentence=sum(avg_length)/length
print("avg no of words per sentence= ",avg_no_of_words_per_sentence)
#complex words 
def complexword(tokenizetext):

    vowels=['a','e','i','o','u']

    count=0
    complex_Word_Count=0
    for i in tokenize_text:
        x=re.compile('[es|ed]$')
        if x.match(i.lower()):
            count+=0
        else:
            for j in i:
                if(j.lower() in vowels ):
                    count+=1
    if(count>2):
        complex_Word_Count+=1
    return complex_Word_Count
print('complex words count=', str(complexword(tokenize_text)))

word_count=len(tokenize_text)
print('word count= ', word_count)


#syllable per word 
def syllableperword(tokenize_text):
    vowels=['a','e','i','o','u']

    count=0
    for i in tokenize_text:
        x=re.compile('[es|ed]$')
        if x.match(i.lower()):
            count+=0
        else:
            for j in i:
                if(j.lower() in vowels ):
                    count+=1
    syllable_count=count
    return syllable_count
print('syllable_per_word= '+str(syllableperword(tokenize_text)))

#personal pronouns 

def pronoun(tokenize_text):
    pronouns=['i','we','my','ours','us' ]
    count=0
    for i in tokenize_text:
        if i.lower() in pronouns:
            count+=1
    personal_pronouns=count
    return personal_pronouns
print("personal pronoun"+str(pronoun(tokenize_text)))
#average word count
def average_word(tokenize_text):
    count=0
    for i in tokenize_text:
        for j in i:
            count+=1
    avg_word_length=count/len(tokenize_text)
    
    return avg_word_length
print("average_word_lenght ="+str(average_word(tokenize_text)))

data={'positive_score':positive_score,'negative_score':negative_score,'Polarity_Score':Polarity_Score,'subjectiivity_score':subjectiivity_score,'avg_senetence_length':avg_senetence_length,'Percentage_of_Complex_words':av,'Fog_Index':Fog_Index,'avg_no_of_words_per_sentence':avg_no_of_words_per_sentence,'complex_Word_Count':complex_Word_Count,'word_count':word_count,'syllable_count':syllableperword(tokenize_text),'personal_pronouns':pronoun(tokenize_text),'avg_word_length':average_word(tokenize_text)}
#output=pd.DataFrame()

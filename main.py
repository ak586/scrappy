import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import string 
import re
import chardet
from os import listdir
from read_file import read_file
# local file

nltk.download('punkt')
nltk.download('stopwords')


# First run scrap.ipynb which will scrap and store data in scrapped_data folder
# After that run main.py



# Get stop words
import chardet
stop_word_files = [
    'StopWords_Auditor.txt',
    'StopWords_DatesandNumbers.txt',
    'StopWords_GenericLong.txt',
    'StopWords_Names.txt',
    'StopWords_Currencies.txt',
    'StopWords_Generic.txt',
    'StopWords_Geographic.txt'
]

custom_stop_words = []

for name in stop_word_files:
    file_name = './StopWords/' + name

    # Detect the encoding of the file
    with open(file_name, 'rb') as f:
        result = chardet.detect(f.read())

    # Use the detected encoding to read the file
    try:
        with open(file_name, 'r', encoding=result['encoding']) as f:
            lines = f.readlines()
            for line in lines:
                curr_line = line.split(' ')
                custom_stop_words.append(curr_line[0].strip())
        print(f"Successfully read {file_name} with encoding: {result['encoding']}")
    except UnicodeDecodeError:
        print(f"Failed to read {file_name} with detected encoding: {result['encoding']}")

# for words in custom_stop_words:
#     print(words)



""" Extract positive and Negative words from given dictionary """
positive_words=[]
negative_words=[]

# detect encoding as its not standard utf8
with open('./MasterDictionary/negative-words.txt', 'rb') as f:
        result = chardet.detect(f.read())
        
with open('./MasterDictionary/positive-words.txt','r',encoding=result['encoding']) as f:
        positive_words=f.read()
with open('./MasterDictionary/negative-words.txt', 'r', encoding=result['encoding']) as f:
        negative_words=f.read()


# create the output file
# Define the column names
column_names = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
                'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE',
                'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']

output = pd.DataFrame(columns=column_names)
input_data=pd.read_excel('./data/Input.xlsx')

file_list=listdir('./scrapped_data/')
for file in file_list:
    text=read_file(file)
    word_tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    stop_words.update(custom_stop_words)
    filtered_tokens = [word for word in word_tokens if word.lower() not in stop_words]
    
    punctuation_marks = list(string.punctuation)
    positive_score=0
    negative_score=0
    word_count=0
    sentences = nltk.sent_tokenize(text)
    total_sentences=len(sentences)
    syllable_word_count=0
    syllable_count=0
    total_char_length=0
    pronoun_count=0
    complex_word_count=0



    for word in filtered_tokens:
        if word in punctuation_marks:
            continue
        else:
            if word.lower() in positive_words:

                positive_score+=1
            elif word.lower() in negative_words: 
                negative_score+=1

            word_count+=1
            total_char_length += len(word)
        
        # counting syllables
            if word.lower().endswith("es") or word.lower().endswith("ed"):
                continue
            else:
                vowels = ['a', 'e', 'i', 'o', 'u']
                for vowel in vowels:
                    current_count = word.lower().count(vowel)
                    syllable_count+=current_count
                    if current_count>2:
                        complex_word_count+=1
                
                syllable_word_count+=1
        
            # counting pronouns
            # Define a regular expression pattern to match the personal pronouns
            pattern = r'\b(?!(?:US\b))(I|we|my|ours|us)\b'
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            pronoun_count+=1
            

    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)

    syllable_per_word=syllable_count/word_count

    average_sentence_length = word_count / total_sentences

    # Calculate the Percentage of Complex Words
    percentage_complex_words = (complex_word_count / word_count) * 100

    # Calculate the Fog Index
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
    avg_words_per_sentence= word_count/total_sentences
    avg_word_length= total_char_length/word_count
    url_id=file.replace('.txt','')
    url=input_data[input_data['URL_ID'] == float(url_id)]['URL'].iloc[0]
    curr_row_data = {
    'URL_ID': url_id,
    'URL': url,
    'POSITIVE SCORE': positive_score,
    'NEGATIVE SCORE': negative_score,
    'POLARITY SCORE': polarity_score,
    'SUBJECTIVITY SCORE': subjectivity_score,
    'AVG SENTENCE LENGTH': average_sentence_length,
    'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
    'FOG INDEX': fog_index,
    'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
    'COMPLEX WORD COUNT': complex_word_count,
    'WORD COUNT': word_count,
    'SYLLABLE PER WORD': syllable_per_word,
    'PERSONAL PRONOUNS': pronoun_count,
    'AVG WORD LENGTH': avg_word_length
    }
    output=output._append(curr_row_data, ignore_index=True)

output.to_excel('./ouput.xlsx', index=False)
    




    
    

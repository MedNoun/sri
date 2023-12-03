import codecs
import pickle
import sys
import os
import nltk
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')


class TokenBuilder:
    
    def __init__(self, collection_path) -> None:
        self.collection_path = collection_path
        self.file_tokens = {}
        self.tokens = self.__get_tokens()
        self.__create_file_dic()
        self.create_index()
    
    def create_index(self):
      result = {}
      for token in self.tokens:
        result[token] = set()
      for file in self.file_tokens:
        for token in self.file_tokens[file]:
            if token in self.tokens:
              result[token].add(file)
      self.__dump_pkl(result, "app/output/inversed_index.pkl")
          
          
    def __dump_pkl(self,  data, pkl_file):
       with open(pkl_file, "wb") as fp:
        pickle.dump(data, fp)
    def __create_file_dic(self):
       for key in self.file_tokens.keys():
          file_occ = {}
          for token in self.file_tokens[key]:
             if token in self.tokens:
                file_occ[token] = file_occ.get(token, 0) + 1
          self.file_tokens[key] = file_occ.copy()
          self.__dump_pkl(file_occ,"app/output/files/" + key + ".pkl")

    def __get_tokens(self):
        files = os.listdir(self.collection_path)
        tokens = set()
        for file in files:
            self.file_tokens[file] = []
            with open (os.path.join(self.collection_path, file)) as fin:
              line_tokens = word_tokenize(fin.read().lower(),"french")
              self.file_tokens[file].extend(line_tokens[::]) 
              tokens = tokens.union(line_tokens)
        punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
        print(self.file_tokens)
        for pun in punc:
            if pun in tokens:
              tokens.remove(pun)
        tokens_without_sw = {word for word in tokens if not word in stopwords.words()}
        self.__dump_pkl(tokens_without_sw, "app/output/tokens.pkl")
        return tokens_without_sw
TokenBuilder("app/files")
        

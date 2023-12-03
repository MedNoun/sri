import pickle
class SearchEngine:
    def __read_pkl(self, pkl_file):
        with open(pkl_file, "rb") as fp:
            return pickle.load(fp)
    def __init__(self,index : str = "app/output/inversed_index.pkl") -> None:
        self.index = self.__read_pkl(index)
        print(self.index)
    def query(self, query):
        new_query = []
        for el in query:
            if el not in {"+","-","*"}:
                print("in not : ", el)
                el = self.index.get(el,set())
                print(el)
            new_query.append(el)
        print(new_query)
        return self.evalRPN(new_query)
    
    def evalRPN(self , tokens: list) -> int:
        oprands = []
        for i in range(len(tokens)):
            op = tokens[i]
            if(op in ["+","*","-"]):
                second : set = oprands.pop()
                first : set = oprands.pop()
                if op == "+": 
                    rlt =  first.union(second)
                if op == "-": 
                    rlt = first.difference(second)
                if op == "*": 
                    rlt = first.intersection(second)
                oprands.append(rlt)
            else:
                oprands.append(op)
        return oprands.pop()
se = SearchEngine()
print(se.query(["amour","sahnoun", "+"]))

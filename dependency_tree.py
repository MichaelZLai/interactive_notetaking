import requests

sentence =  '''
            Canada is one of the best countries in the world to live in. 
            '''
url = "http://corenlp.run/"
POST_PROPERTIES = '{"annotators":"tokenize,ssplit,pos,depparse,lemma,ner","outputFormat":"json","ssplit.eolonly":"true"}'

ret = requests.post(data=sentence.encode("utf-8"),
                    params={"properties": POST_PROPERTIES},
                    url=url)

relations = ret.json()['sentences'][0]['basicDependencies']
for relation in relations:
    print(relation)

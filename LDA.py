from konlpy.tag import Hannanum
hannanum = Hannanum()

class Processing():
    '''
    input: list type of documents
    '''
    def __init__(self):
        pass

    def lemma_sentences(self,documents):
        temp = [hannanum.morphs(document) for document in documents]

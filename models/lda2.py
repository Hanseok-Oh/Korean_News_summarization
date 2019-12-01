import konlpy
from konlpy.tag import Okt
import gensim
from gensim import corpora
import pyLDAvis.gensim
from pprint import pprint
import os
import matplotlib.pyplot as plt
from gensim.models.coherencemodel import CoherenceModel
import warnings
warnings.filterwarnings('ignore')
from preprocess import Processing

p = Processing()
result_path = os.getcwd().replace("\\","/")
print(result_path+'/data/{}_contents_text.txt'.format('현대자동차'))
content = p.main(result_path+'/data/{}_contents_text.txt'.format('현대자동차'))
print("content:",len(content))


class LDA:
    def __init__(self, processed_data, passes=1, limit=12, start=2, step=2):
        self.texts = processed_data
        self.passes = passes
        self.dictionary = corpora.Dictionary(processed_data)
        self.corpus = [self.dictionary.doc2bow(text) for text in processed_data]

        coherence_values = []
        model_list = []
        for num_topics in range(start, limit, step):
            model = gensim.models.ldamodel.LdaModel(self.corpus, num_topics=num_topics, id2word=self.dictionary,
                                                    passes=self.passes, random_state=2019)
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=self.texts, dictionary=self.dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())

        x = range(start, limit, step)
        # Print the coherence scores
        for m, cv in zip(x, coherence_values):
            print("Num Topics =", m, " has Coherence Value of", round(cv, 4))
        # plt.plot(x, coherence_values)
        # plt.xlabel("Num Topics")
        # plt.ylabel("Coherence score")
        # plt.legend(("coherence_values"), loc='best')
        # plt.show()

    def selected_model(self, num_topics):
        pyLDAvis.enable_notebook()
        ldamodel = gensim.models.ldamodel.LdaModel(self.corpus, num_topics=num_topics, id2word=self.dictionary,
                                                   passes=self.passes, random_state=2019)
        vis = pyLDAvis.gensim.prepare(ldamodel, self.corpus, self.dictionary)
        pprint(ldamodel.print_topics())
        # pyLDAvis.display(vis)

        return ldamodel, vis

    # def visualize_selected_model(self,vis):
    #     pyLDAvis.enable_notebook()
    #     pyLDAvis.display(vis)

    def format_topics_sentences(self, ldamodel):
        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row in enumerate(ldamodel[self.corpus]):
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(
                        pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]), ignore_index=True)
                else:
                    break
        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(self.texts)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1).reset_index()
        sent_topics_df.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
        sent_topics_df = sent_topics_df.set_index('Document_No')

        return (sent_topics_df)

    def extract_index_per_topic(self, ldamodel):
        df_topic_sents_keywords = self.format_topics_sentences(ldamodel)

        # Group top 5 sentences under each topic
        sent_topics_sorteddf = pd.DataFrame()
        sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')

        for i, grp in sent_topics_outdf_grpd:
            sent_topics_sorteddf = pd.concat([sent_topics_sorteddf,
                                              grp.sort_values(['Topic_Perc_Contrib'], ascending=False).head(1)],
                                             axis=0)
        # Format
        sent_topics_sorteddf.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]

        return sent_topics_sorteddf

a = LDA(content)
ldamodel,vis = a.selected_model(8)

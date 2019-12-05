import gensim
from gensim import corpora
import pyLDAvis.gensim
from gensim.models.coherencemodel import CoherenceModel
from tqdm import tqdm
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
# from preprocess import Processing



class LDA:
    def __init__(self, processed_data, passes=30, limit=12, start=3, step=2):
        self.texts = processed_data
        self.passes = passes
        self.dictionary = corpora.Dictionary(processed_data)
        self.corpus = [self.dictionary.doc2bow(text) for text in processed_data]

        coherence_values = []
        model_list = []
        for num_topics in tqdm(range(start, limit, step),desc="LDA-find proper number of topic"):
            model = gensim.models.ldamodel.LdaModel(self.corpus, num_topics=num_topics, id2word=self.dictionary,
                                                    passes=self.passes, random_state=2019)
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=self.texts, dictionary=self.dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())

        x = range(start, limit, step)
        # Print the coherence scores

        for m, cv in zip(x, coherence_values):
            print("Num Topics =", m, " has Coherence Value of", round(cv, 4))

        self.best_topic_num = x[coherence_values.index(max(coherence_values))]
        # self.best_topic_num = 2

        print("\nbest topic num is {}".format(self.best_topic_num))

    def selected_model(self):
        ldamodel = gensim.models.ldamodel.LdaModel(self.corpus, num_topics= self.best_topic_num, id2word=self.dictionary,
                                                   passes=self.passes, random_state=2019)
        vis = pyLDAvis.gensim.prepare(ldamodel, self.corpus, self.dictionary)
        return ldamodel, vis

    def format_topics_sentences(self, ldamodel,query):
        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row in enumerate(ldamodel[self.corpus]):
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            # print("row of index-{}:\n".format(i),row)
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp if word != query])
                    # print("topic keywords:",topic_keywords)
                    sent_topics_df = sent_topics_df.append(
                        pd.Series([int(topic_num+1), round(prop_topic, 4), topic_keywords]), ignore_index=True)
                else:
                    break
        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(self.texts)
        assert len(contents) == len(sent_topics_df)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1).reset_index()
        sent_topics_df.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
        sent_topics_df = sent_topics_df.set_index('Document_No')
        print("After LDA format topics sentence-input file length:", len(sent_topics_df))

        return sent_topics_df

    def extract_index_per_topic(self, ldamodel,query):
        df_topic_sents_keywords = self.format_topics_sentences(ldamodel,query)

        # Group top 5 sentences under each topic
        sent_topics_sorteddf = pd.DataFrame()
        sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')

        for i, grp in sent_topics_outdf_grpd:
            best_grp = grp.sort_values(['Topic_Perc_Contrib'], ascending=False)

            sent_topics_sorteddf = pd.concat([sent_topics_sorteddf,
                                              best_grp.head(1)],
                                             axis=0)
        # Format
        sent_topics_sorteddf.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]
        print("After LDA extract index per topic -input file length:", len(sent_topics_sorteddf))
        return sent_topics_sorteddf



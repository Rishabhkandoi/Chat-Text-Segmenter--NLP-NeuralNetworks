import pyLDAvis as pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt
import numpy as np
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel, LsiModel, HdpModel, LdaModel
import os, re, operator, warnings
warnings.filterwarnings('ignore')


def comparison(texts):
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lsimodel = LsiModel(corpus=corpus, num_topics=2, id2word=dictionary)
    print('LSI Model output')
    print(lsimodel.show_topics())

    hdpmodel = HdpModel(corpus=corpus, id2word=dictionary)
    print('hdp model output')
    print(hdpmodel.show_topics())

    ldamodel = LdaModel(corpus=corpus, num_topics=2, id2word=dictionary)
    print('LDA Model output')
    print(ldamodel.show_topics())


    pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)

    lsitopics = [[word for word, prob in topic] for topicid, topic in lsimodel.show_topics(formatted=False)]

    hdptopics = [[word for word, prob in topic] for topicid, topic in hdpmodel.show_topics(formatted=False)]

    ldatopics = [[word for word, prob in topic] for topicid, topic in ldamodel.show_topics(formatted=False)]

    lsi_coherence = CoherenceModel(topics=lsitopics[:10], texts=texts, dictionary=dictionary,
                                   window_size=10).get_coherence()

    hdp_coherence = CoherenceModel(topics=hdptopics[:10], texts=texts, dictionary=dictionary,
                                   window_size=10).get_coherence()

    lda_coherence = CoherenceModel(topics=ldatopics, texts=texts, dictionary=dictionary, window_size=10).get_coherence()

    def evaluate_bar_graph(coherences, indices):
        assert len(coherences) == len(indices)
        n = len(coherences)
        x = np.arange(n)
        plt.bar(x, coherences, width=0.2, tick_label=indices, align='center')
        plt.xlabel('Models')
        plt.ylabel('Coherence Value')
        plt.show()

    evaluate_bar_graph([lsi_coherence, hdp_coherence, lda_coherence], ['LSI', 'HDP', 'LDA'])

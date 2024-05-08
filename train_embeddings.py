from multiprocessing import cpu_count
from gensim.models import Word2Vec, callbacks

def train_embeddings(df, sg=0, negative=5, window=8, min_count=5, size=300, epochs=10):
    sentences = df["body_clean"].to_list()
    
    class callback(callbacks.CallbackAny2Vec):
        def __init__(self):
            self.epoch = 0

        def on_epoch_end(self, model):
            loss = model.get_latest_training_loss()
            if self.epoch == 0:
                print('Loss after epoch {}: {}'.format(self.epoch, loss))
            elif self.epoch % 10 == 0:
#             else:
                print('Loss after epoch {}: {}'.format(self.epoch, loss - self.loss_previous_step))
            self.epoch += 1
            self.loss_previous_step = loss

    model = Word2Vec(sg=sg, negative=negative, window=window, min_count=min_count, vector_size=size, workers=cpu_count())
    model.build_vocab(corpus_iterable=sentences)
    model.train(corpus_iterable=sentences, compute_loss=True, callbacks=[callback()], epochs=epochs, total_examples=model.corpus_count)
    return model

from loader import load_dataset

def evaluate(ds, prefix="../data/embeddings/embeddings/"):
    model = Word2Vec.load(prefix + ds + ".bin")
    print(model.wv.most_similar("man", negative="woman", topn=5))

dataset_names = ["fourthwavewomen","incels", "braincels", "trufemcels", "mensrights", "incels_full","feminism_full","feminism_2015_2017","feminism_2017_2019","feminism_2019_2021","feminism_2021_2023"]
for name in dataset_names:
    print(name)
    ds = load_dataset(name,prefix = "../data/cleaned_corpora/clean/")
    model = train_embeddings(ds,epochs=100)
    model.save("../data/embeddings/embeddings/" + name + ".bin")
    evaluate(name, prefix="../data/embeddings/embeddings/")
from fastai import *
from fastai.text import * 
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

# Model of the trained neural network
parser.add_argument("model_name")
# Number of quotes to generate
parser.add_argument("number_of_quotes")
# Target CSV file 
parser.add_argument("output_file")

args = parser.parse_args()

PATH = Path('./data')
MODEL_NAME = args.model_name
NUMBER_OF_QUOTES_TO_GENERATE = int(args.number_of_quotes)
OUTPUT_FILE = PATH/args.output_file



def predict_one_quote(learner, text:str, n_words:int=1, no_unk:bool=True, temperature:float=1., min_p:float=None):
        """Return the `n_words` that come after `text`."""
        ds = learner.data.single_dl.dataset
        learner.model.reset()
        is_finished=False
        for _ in range(n_words):
            xb, yb = learner.data.one_item(text)
            if text == 'xxbos': text = ""
            res = learner.pred_batch(batch=(xb,yb))[0][-1]
            res[learner.data.vocab.stoi[UNK]] = 0.
            res[learner.data.vocab.stoi['https']] = 0.
            res[learner.data.vocab.stoi['t.co']] = 0.
            
            if min_p is not None: res[res < min_p] = 0.
            if temperature != 1.: res.pow_(1 / temperature)
            idx = torch.multinomial(res, 1).item()
            if learner.data.vocab.itos[idx] == 'xxbos': 
                break
            text += f' {learner.data.vocab.itos[idx]}'
           
        return text
           
    
def predict_quotes(learner, text:str, n_quotes=1, n_words:int=1, no_unk:bool=True, temperature:float=1., min_p:float=None, use_rand_temp=False):
    """ Generates quotes using a temperature defined by a normal law"""
    quotes = []
    for i in range(n_quotes):
        if use_rand_temp:
            temperature= np.random.normal(loc=1.0, scale=0.15, size=1)[0]
            print(f"Generated temp: {temperature}")
        quotes.append(predict_one_quote(learner, text, n_words, no_unk, temperature, min_p))
    return quotes



def generate_quotes_quantity(quantity, learn):
    """Function to generate N quotes """
    table_quotes = []
    for i in tqdm(range(quantity)):
        txt = predict_quotes(learn, "xxbos", n_quotes=1, n_words=200, use_rand_temp=True)
        table_quotes.append(txt[0])
    
    return table_quotes



learn = load_learner(PATH, fname=MODEL_NAME)

res = generate_quotes_quantity(NUMBER_OF_QUOTES_TO_GENERATE, learn)

df_gen = pd.DataFrame()
df_gen['text'] = res
df_gen.to_csv(OUTPUT_FILE)
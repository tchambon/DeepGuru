![GIF showing the widget](https://github.com/tchambon/DeepGuru/blob/master/media/screenDeepGuru.jpg "DeepGuru picture")

# DeepGuru AI

DeepGuru is a twitter bot generating inspirational quotes. It uses deep learning to generate tweets.

You can check it here: [https://twitter.com/DeepGuruAI](https://twitter.com/DeepGuruAI)

## Technology

The bot uses the [ULMFiT model](https://arxiv.org/abs/1801.06146).

It is trained on a corpus of tweets created for this task (2 corpora of ~4k tweets).
Because the ULMFiT model is pre-trained on an extract of Wikipedia, it is able to train well with a small dataset (~4k tweets for the first version).

## How it works

The process is the following:

- Create a dataset with tweets of the target style (in DeepGuru case, philosophical and zen tweets)
- Fine-train the ULMFiT english model on the corpus (Notebook "Model Training")
- Use the trained model to generate tweets (script "QuoteGenerator.py")
- Selection step: Filter the generated tweets (Notebook "Post-processing of generated quotes")
    - At the moment, there is a manual step of filtering the generated tweets. The tweets are not modified but around 30% are rejected
    - I am working on a second neural network to automatically select the best generated tweets
- Twitter bot: Tweet a few times a day using the generated data, with a cron task (script "bot.py")

## Next steps

- Write a technical post with an  in-depth explanation of the approach and technical parts
- Finalize the second neural network to automatically select the best generated tweets
- Experiment with data: new corpus and mixing  of corpus
- Experiment with the generation algorithm
- Experiment with model: test other models like google BERT

## Dependencies

The project uses:

- [Pytorch v1](https://github.com/pytorch/pytorch)
- [Fastai v1](https://github.com/fastai/fastai)
- [Tweepy](https://github.com/tweepy/tweepy)
- [LabelMyTextWidget](https://github.com/tchambon/LabelMyTextWidget)
- [Anaconda distribution](https://www.anaconda.com/): jupyter notebook, numpy, pandas, ...

To use it, you have to install:

- Anaconda distribution with Python 3
- Fastai (which is based on Pytorch)
- Tweepy
- LabelMyTextWidget

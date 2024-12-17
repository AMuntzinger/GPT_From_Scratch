# GPT Language Model From Scratch

This repo contains code to construct a character-level **GPT (Generative Pretrained Transformer)** model from scratch, following Andrej Karpathy's [Zero To Hero](https://karpathy.ai/zero-to-hero.html) series on GPT.
The model is trained on different texts, for example Shakespeare, Goethe's "Faust", the "Lord of the Rings" or books from Jane Austen, and is able to generate new text based on the text from the book.

The repo contains 3 interactive Jupyter notebooks, each in a 'student' and 'solution' version:

## 1_Bigram_Language_Model__student.ipynb / 1_Bigram_Language_Model__solution.ipynb
This notebook constructs a bigram language model from scratch. 
The model is trained on a text file containing names and will be able to generate new names based on what it has learned. 

## 2_MLP_Language_Model__student.ipynb / 2_MLP_Language_Model__solution.ipynb
This notebook extends the previous bigram model to a multi-layer perceptron to improve the name generation results.

## 3_Character_Level_GPT__student.ipynb / 3_Character_Level_GPT__solution.ipynb
Finally, the full GPT is implemented from scratch, trained on different texts, and generating new text.

## Dependencies

See `Pipfile` for an overview of required python packages.

## Author

This is an extended version of Andrej Karpathy's notebook in addition to his [Zero To Hero](https://karpathy.ai/zero-to-hero.html) video on GPT.

Adapted by: 

Prof. Dr.-Ing. Antje Muntzinger, University of Applied Sciences Stuttgart
antje.muntzinger@hft-stuttgart.de


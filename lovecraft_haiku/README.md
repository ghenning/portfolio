# Lovecraft's haikus: NLP haiku generator

H. P. Lovecraft approached me and asked if I could help him learn how to create haikus. I told him that if I could post the results here then I'd gladly help him. 

## How did Lovecraft learn to write haikus?

### Building the model

First we grab some works of Lovecraft from the `shakecraft` project in this repo. After cleaning up the texts from punctuations we create text sequences of equal lenghts. If our text was 'a b c d e f' we'd get these kind of sequences:
```
seq 1 : [a b c d]
seq 2 : [b c d e]
seq 3 : [c d e f]
```
Each sequence is then split into `X` and `y` for the model training in such a way that `X` conatins all the sequence words except the last one and `y` only contains the last word (e.g. `seq 1` would be split into `X = [a b c]` and `y = [d]`).

Now we shove these sequences into our Tensorflow model containing two gated recurrent unit and one dense hidden layers. Our model can now predict one word at a time from our Lovecraftian vocabulary.

### Generating text and writing haikus

With our model ready we can start generating some text. To do so we take a random text sequence as an input seed and the model predicts what the next word of that sequence would be. To generate more words we simply add the latest predicted word to the sequence and predict the next word based on our new sequence. We continue in this manner until we've predicted as many words as we want.

To make haikus from our generated text we need to teach Lovecraft some grammar. We do that using `spaCy` by creating `Matcher` objects that can search text for patterns such as nouns, verbs, adjectives. We use these `Matcher` objects to look for patterns "that make sense" from one to five words long.

The defining trait of haikus is the syllable count, where the typical haiku is 5-7-5 syllables long. To count syllables we can use `syllapy`. Our setup is now good to go and we can look through our generated text for pattern matches. First we create two empty lists earmarked for patterns with 5 and 7 syllables. For each pattern found we count the syllables, and if the pattern has 5 or 7 syllables we add it to our corresponding list.

Once our lists are full of patterns we can easily generate a silly amount of haikus by grabbing random samples from our syllable lists to make a 5-7-5 haiku.

## Results

Lovecraft has now learned the basics of writing haikus. He's still an amateur at this craft but can still make some decent haikus. To do better we can increase the amount of text we read in (which will cost a juicy amount of memory) or increase the complexity of the model by adding more nodes to the hidden layers and/or adding more hidden layers (which can take an exorbitant amount of time to train).

You'll find *Lovecraft's haikus Vol. 1* as a text file in this repo. Below I'll paste some examples of his writings.

```
awful purgation
to arkham john ward supposed
terrible and old

pawtuxet farmhouse
cliffs of glass overlooking
wholesome colours

beyond the river
drawer in the ancient line
rapidly coloured

lower falls i passed
same colour the library
reigns with curious

building harboured
scraps to any disposal
better do no use

scarcely escape
about by what appeared
from her own half part

of chalcedony
curious intensity
frenzy of hideous
```

*Note: The model and text sequences are too large to add here so if you want to try this out yourself you'll unfortunately have to train the model on your own (simply run the notebooks in this repo).*

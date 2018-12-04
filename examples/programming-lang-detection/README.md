# Programming Language Detection by MXNet 

This example uses the power of MXNet alongside Keras to detect the programming language based upon an input file passed in.

Currently, the @mxnet-label-bot uses this model to help both our contributors and new users by providing help which our users face
in an appropriate manner.

The script is able to take in a file name and detect the kind of programming language within the file as well as code snippets. Across the board we have found that it
offers >90% accuracy for languages which we currently support of the file which is provided.
## Usage ##

Run:

```
python2.7 test.py <filename>
```

You can download a pre-trained model from [here](). This model was trained on an AWS p3.16 instance and it took under 30 minutes to train.

## Purpose
The project is set up to demonstrate - in simple steps - how to use Keras to build a Deep Learning (DL) model to reconise programming language of a code file or snippet. This can be used to detect language of code snippets and has been trained for it by splitting the files into snippets.  

## Limitations
Small dataset is the main limitation of the project - for a powerful model, you would need at least x10 or x100 samples. Another problem is that the training has been done on full files (and their snippets) and not on snippets. 

## Languages
5 languages were chosen as below:
Clojure, Java, Scala, Python, C++

## Data
All the data was extracted from Github using its search feature. Common inert words used for search where the word is not a keyword in a language. The words used are:

> load, dump, write, stream, api, manage, broker, save, process, service
mapping, dispatch, copy, duplicate, sample, chunk, instrument
calculate, append, repository, facade, handler, message, invoke,
controller, locator, customer, view, model, nav, show, new, old, legacy

Data are separated into training (~2000 per language) and test (~1000 per language). In the new version, in order to train for snippets, larger files are broken down and the second and last third of the file are used in the training data. 

## Run the code
You need Keras-MXNet. The code is in python 2.7.

### Training

To train, simply run the `train.py` script:

```python
python train.py
```

If you have GPU enabled, it should automatically use it.

### Testing in batch mode

```python
python test_run.py
```

This tests all files in the test folder and output looks like below:

```
Final result: 7949/8016 (0.991641716567)
clojure - Precision:0.995991983968 Recall: 0.992015968064
java - Precision:0.990118577075 Recall: 1.0
scala - Precision:0.99001996008 Recall: 0.99001996008
python - Precision:0.976470588235 Recall: 0.994011976048
css - Precision:0.994011976048 Recall: 0.994011976048
java:   501/501 (1.0)
scala:    496/501 (0.99001996008)
python:   498/501 (0.994011976048)
cpp:    495/501 (0.988023952096)
```

### References
This work was orginally based of the work from this [repo](https://github.com/aliostad/deep-learning-lang-detection).
Approach for DL has been based on Zhang and LeCun's 2016 [paper](https://arxiv.org/pdf/1502.01710.pdf) "Text Understanding from Scratch". The main technique is that instead of using word2vec to create word embedding, characters are quantised (turned to one-hot-vector) and then the document is represented by a sequence of quantised characters (vectors). Currently the document is truncated at 2KB and smaller docs are padded by all zero vectors. 

### Applications
This model is currently being applied and used by the mxnet-label-bot. This bot is being currently being maintained on this
repository: [label bot repo](https://github.com/MXNetEdge/mxnet-infrastructure)

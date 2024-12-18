import docx
import numpy as np
import tensorflow.keras as keras
import nltk
import re
from itertools import permutations
from tika import parser
import pickle
import os
import chardet

current_path = os.path.realpath(__file__)
parent_path = os.path.dirname(current_path)
model_path = os.path.join(parent_path, "model/")
model_list = []


def loss(y_true, y_pred):
    return keras.losses.binary_crossentropy(
        y_true[:, 0], y_pred[:, 0]
    ) * 10000 + keras.losses.mean_absolute_error(y_true[:, 1], y_pred[:, 1])


for i in range(10):
    model_list.append(
        keras.models.load_model(
            model_path + "cnn_nouvelle_variable_50_" + str(i) + ".h5",
            custom_objects={"Functional": keras.models.Model, "loss": loss},
        )
    )


def tokenize_text(text):
    # Load the entity classifier:
    open_file = open(f"{model_path}vocabulary_light", "rb")
    vocab = pickle.load(open_file)
    open_file.close()

    max_size = 15509
    X = np.zeros((1, max_size))
    for i, word in enumerate(text[:max_size]):
        if word in vocab:
            X[0, i] = vocab[word]
        else:
            X[0, i] = vocab[
                "<UNK>"
            ]  # If the word isn't in the vocabulary, take the '<UNK>' token
    return X


def import_and_predict(raw_text):
    """ "Function wrapping up the prediction pipeline of the model."""
    # Text pre-processing:
    text_prediction = re.sub(r"[^\w\s]", " ", raw_text)
    text_prediction = re.sub("R D", "", text_prediction)
    text_prediction = nltk.word_tokenize(text_prediction, language="french")
    X_prediction = tokenize_text(text_prediction)

    predictions = []
    for model in model_list:
        predictions.append(model.predict(X_prediction))
    return np.mean(predictions, axis=0)


def find_technical_part_in_txt(contents, key_words):
    """ "Function to find the technical parts in a text file."""

    # Find matching pattern for the titles we are interested in:
    match = []
    for item in list(permutations(key_words, 2)):
        for m in re.finditer(
            rf"[0-9][.][0-9]\s.*{item[0]}.*{item[1]}", contents.lower()
        ):
            match.append((m.start(), m))

    # If we have some matchs and a even number of them (because of the summary), we proceed:
    if (len(match) > 0) & (len(match) % 2 == 0):
        idx_list = []
        for item in match:
            idx_list.append(item[0])

        set_idx = sorted(list(set(idx_list)))
        final_idx = set_idx[int(len(set_idx) / 2) :]

        text = []
        for item in final_idx:
            try:
                txt = contents[item:]
                try:
                    idx = txt.lower().index("annexes\n")
                    text.append(txt[:idx])
                except ValueError:
                    text.append(txt)
            except ValueError:
                continue
        new_text = []
        if len(text) > 1:
            for item in text[:-1]:
                int_idx = int(item[0])
                final_idx = item.lower().index("\n" + str(int_idx + 1))
                new_text.append(item[:final_idx])
            new_text.append(text[-1])
        else:
            new_text = text
    else:
        new_text = []
    return new_text


def read_file(file):
    """A function to read an inputed file, transform it into text and extract the parts of interest."""

    key_words = ["synopsis", "projet", "description", "travaux", "démarche", "réalisés"]
    texts_list = []

    # .txt:
    if ".txt" in file.name:
        content = file.read()
        encoding = chardet.detect(content)["encoding"]
        full_text = str(content, encoding=encoding)
        texts_list = find_technical_part_in_txt(full_text, key_words)

    # .pdf:
    elif ".pdf" in file.name:
        full_text = parser.from_file(file)["content"]
        texts_list = find_technical_part_in_txt(full_text, key_words)
    # .docx:
    elif ".docx" in file.name:
        # Read the docx file and initialize some variables:
        doc = docx.Document(file)
        full_text = ""
        current_text = ""
        is_technical_part = False
        biggest_heading_level = 0
        heading_level = 0
        # Go through every paragraph:
        for para in doc.paragraphs:
            # If it's a title..
            if para.style.name.split(" ")[0] == "Heading":
                # ..and we are in the technical part..
                if is_technical_part:
                    # ..and its title level is higher (1>2 for titles): it's the end of the technical part.
                    if int(para.style.name.split(" ")[1]) <= heading_level:
                        is_technical_part = False
                        texts_list.append(current_text)
                        current_text = ""
                    # if int(para.style.name.split(" ")[1]) > heading_level:
                    #     biggest_heading_level = int(para.style.name.split(" ")[1])
                    #     is_technical_part = True
                    #     texts_list.append(current_text)
                    #     current_text = ""

                # If we are not in the technical part: count the number of matches with our key words.
                else:
                    count_matchs = 0
                    for word in key_words:
                        if re.search(word, para.text.lower()):
                            count_matchs += 1
                    # If we have more than 2 matches, it is the beginning of the technical part:
                    if count_matchs > 1:
                        heading_level = int(para.style.name.split(" ")[1])
                        is_technical_part = True
            # If it is not a title, but we are in a technical part: add it to the text.
            if is_technical_part:
                current_text += para.text + "\n"
            full_text += para.text + "\n"

            # After the end of a technical part, add it to the list and proceed:
        if current_text != "":
            texts_list.append(current_text)
        if biggest_heading_level > heading_level:
            texts_list.pop(0)

        # If we haven't find the technical part, output the full inputed text

    technical_part_detected = len(texts_list)
    if technical_part_detected == 0:
        texts_list.append(full_text)
    return texts_list, technical_part_detected


def process_montant_pred(montant_pred, montant) -> bool:
    """Function to rework and display the second output of the model."""
    if (montant > montant_pred / 3) & (montant < montant_pred * 3):
        return True
    else:
        return False


def process_prob_cir(prob_cir) -> str:
    """Function to rework and display the first output of the model."""
    if prob_cir < 0.3:
        return "Très probablement innovation"
    elif prob_cir < 0.5:
        return "Innovation mais pourrait passer en R&D"
    elif prob_cir < 0.9:
        return "Probablement R&D"
    else:
        return "Très probablement R&D"

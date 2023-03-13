import spacy
from spacy.lang.es.stop_words import STOP_WORDS

nlp = spacy.load("es_core_news_sm")

def generate_summarize(text, n):
    doc = nlp(text)

    # Crear un diccionario de frecuencia de las palabras en el documento
    word_frequencies = {}
    for token in doc:
        if token.text.lower() not in STOP_WORDS and token.is_punct == False:
            if token.text.lower() not in word_frequencies.keys():
                word_frequencies[token.text.lower()] = 1
            else:
                word_frequencies[token.text.lower()] += 1

    # Normalizar la frecuencia de palabras
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    # Crear un diccionario de puntuación de oraciones
    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Ordenar las oraciones en función de su puntuación y seleccionar las n mejores
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]

    # Concatenar las oraciones seleccionadas para formar el resumen
    summarized_text = ""
    for sentence in summarized_sentences:
        summarized_text += sentence.text + " "

    return summarized_text

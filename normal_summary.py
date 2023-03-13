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

# Ejemplo de uso
text = '''
¿Quieres unirte al desafío de hacer más justo y accesible el sistema financiero para las pymes en Latinoamérica? ¡Postula para ser #Cumpler!

Estamos buscando un o una FrontEnd Developer, para trabajar de manera híbrida o remota para Cumplo (Chile, Perú o México) siendo parte del área de FrontEnd.

¿Qué estarás haciendo?

Analizar el problema de negocio y proponer una solución desde sus capacidades y el desafío, alineado al lenguaje, método y metodologías en consenso.
Interiorizarse en el negocio y la infraestructura de Cumplo.
Trabajar las soluciones en equipo, bajo la definición de negocio y centrado en las personas usuarias.
Eficientar el trabajo, buscar la calidad del código y su escalabilidad.
Sistematizar y documentar el trabajo realizado para el correcto traspaso de la información y conocimiento.
Requisitos:

Ing. Sistemas, Informática o afines.
Sólidos conocimientos en JS, CSS y HTML, además de React
Conocimiento de las características de ES6.
Experiencia utilizando bibliotecas de componentes (plus si es Material UI).
Entender y aplicar el concepto de Atomic Design.
Experiencia de 5 años mínimo trabajando en desarrollo de software y producto.
Beneficios de ser Cumpler:

Contratación directa, 100% nómina.
Días de vacaciones adicionales a las de ley al año.
Personal Days:Día libre por cumpleaños
Día libre por mudanza
Días libres por matrimonio, etc.

Bono para equipo de cómputo.
Sé parte de un equipo global de personas apasionadas y talentosas, con ganas de impactar a más pymes y familias de nuestro continente, para que puedan crecer y desarrollarse.

En Cumplo tenemos el compromiso de establecer un espacio laboral accesible, inclusivo y agradable, donde las y los Cumplers se sientan cómodos para poder desarrollarse profesionalmente y potenciar sus talentos. Promovemos un ambiente de respeto, compañerismo y apoyo para las y los colaboradores y clientes.

Tipo de puesto: Tiempo completo

Salario: $35,000.00 - $39,000.00 al mes

Horario:

Turno de 8 horas
Experiencia:

Frontend Developer: 3 años (Deseable)
Atomic Design: 3 años (Des
'''

smr = generate_summarize(text, 5)

print(smr)
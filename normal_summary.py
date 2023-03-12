import spacy
from spacy.lang.es.stop_words import STOP_WORDS
from collections import defaultdict

nlp = spacy.load('es_core_news_sm')

def generate_summarize(text, n):
    # Paso 2: Procesar el texto utilizando el modelo de lenguaje 'es_core_news_sm' de 'spacy'.
    doc = nlp(text)

    # Paso 3: Obtener las oraciones del texto procesado.
    sentences = [sent for sent in doc.sents]

    # Paso 4: Calcular la frecuencia de cada palabra en el texto y filtrar las palabras vacías.
    freq_words = defaultdict(int)
    for token in doc:
        if not token.is_stop:
            freq_words[token.text] += 1

    max_freq = max(freq_words.values())
    for word in freq_words.copy().keys():
        if freq_words[word] < 2 or freq_words[word] == max_freq:
            del freq_words[word]

    # Paso 5: Asignar una puntuación a cada oración en función de la frecuencia de las palabras que contiene.
    points = defaultdict(int)
    for i, sent in enumerate(sentences):
        for token in sent:
            if token.text in freq_words:
                points[i] += freq_words[token.text]

    # Paso 6: Seleccionar las oraciones con las puntuaciones más altas y concatenarlas para formar el resumen.
    best_sentences = sorted(points, key=points.get, reverse=True)[:n]
    summary = [sentences[i].text for i in best_sentences]
    return '\n'.join(summary)

text = '''
El Club Universidad Nacional, A.C. conocido popularmente como los Pumas de la UNAM,1​ es un equipo de fútbol profesional de la Primera División de México, fundado el 2 de agosto de 1954.8​ Es propiedad de la misma Universidad Nacional Autónoma de México tal cual cita su acta constitutiva,9​10​11​ pero es el patronato, desde 1977, quien administra y financia al club para no generar una carga para la misma universidad. Dicho patronato es una asociación civil conformada por universitarios destacados y empresarios, en donde el rector de la UNAM funge como presidente honorario.12​ La elección del presidente del club se decide por medio del patronato a través de la asamblea de socios del mismo club.13​ Juega sus partidos como local en el Estadio Olímpico Universitario de la Ciudad de México y sus colores tradicionales son el azul y el dorado.

El equipo ha ganado siete campeonatos de Liga, lo que lo ubica quinto en la historia, También ha obtenido tres Copas de Campeones de la Concacaf, siendo el quinto equipo mexicano que más veces la ha conseguido detrás de América, Cruz Azul, Pachuca y Monterrey. Además, acumula en sus logros un título de Copa México, dos de Campeón de Campeones, una Copa Interamericana y un subcampeonato en la Copa Sudamericana.

Fue el tercer equipo más popular de México detrás del Club América y el Club Deportivo Guadalajara, según las encuestas realizadas por Grupo Reforma y Consulta Mitofsky, desde el año 2013 al 2017; no obstante, considerando las mismas fuentes encuestadoras, cayó al cuarto y quinto lugar en 2018 y 2019 respectivamente.14​15​

Es uno de los cuatro clubes que aún permanecen en el máximo circuito, después de su primer ascenso (los otros son Toluca, Cruz Azul y Tijuana). Por lo cual cuenta con una trayectoria de 89 temporadas consecutivas en la división de honor, desde su ascenso en 1962.

Uno de los elementos que distingue al club, es el sistema de formación de futbolistas profesionales, la denominada "cantera"; esto ha permitido a la institución a través de los años haber sido cuna de destacados jugadores mexicanos, entre los que sobresalen: Enrique Borja, Aarón Padilla, Olaf Heredia, Adolfo Ríos, Leonardo Cuéllar, Luis Flores, Manuel Negrete, Miguel España, Alberto García-Aspe, Luis García Postigo, Jorge Campos, Claudio Suárez, Sergio Bernal, Braulio Luna, Israel López, Gerardo Torrado, Israel Castro, Efraín Juárez, Héctor Moreno, Pablo Barrera, Johan Vásquez y el considerado más grande jugador mexicano de todos los tiempos: el pentapichichi y miembro del once ideal histórico en el Real Madrid: Hugo Sánchez.

Universidad se le ha reconocido históricamente como una de las mejores canteras del fútbol mexicano, al igual, su fuerzas básicas han participado en los torneos internacionales de distintas partes del mundo.

El cuadro de la UNAM es uno de los equipos que no solo ha aportado o vendido más jugadores a otros clubes de México, también es el club mexicano que ha exportado más jugadores "canteranos" a ligas del extranjero como: Hugo Sánchez, Luis García Postigo, Manuel Negrete, Luis Flores, Gerardo Torrado, Héctor Moreno, Efraín Juárez, Pablo Barrera y Johan Vásquez; asimismo sus fuerzas básicas han contribuido con jugadores a las distintas selecciones nacionales de México.

Asimismo, directores técnicos de extracción puma han llegado a dirigir la Selección Mexicana: Bora Milutinovic, Mario Ve
'''

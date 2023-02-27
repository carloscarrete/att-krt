# ATT-KRT

ATT-KRT es un bot de Telegram que utiliza tecnología de procesamiento de lenguaje natural para generar resúmenes de archivos de audio en español.

## Requisitos

Antes de ejecutar el bot, necesitarás obtener una clave de API para OpenAI y un token de bot de Telegram.

### Clave de API de OpenAI

1. Crea una cuenta en [OpenAI](https://openai.com/)
2. Accede a tu [dashboard](https://beta.openai.com/dashboard/)
3. Copia tu clave de API

### Token de bot de Telegram

1. Abre Telegram y busca a [BotFather](https://telegram.me/BotFather)
2. Inicia una conversación y escribe `/newbot`
3. Sigue las instrucciones para crear un nuevo bot
4. Copia el token generado

## Configuración

Una vez que hayas obtenido la clave de API de OpenAI y el token de bot de Telegram, debes crear un archivo `.env` en la raíz del proyecto y agregar las siguientes variables de entorno:

API_KEY=tu_Token_OpenAI

API_SECRET=tu_Token_Telegram


También se proporciona un archivo `.env-example` que puedes usar como plantilla.

## Uso

1. Clona el repositorio: `git clone https://github.com/carloscarrete/att-krt.git`
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta el bot: `python telegram_bot.py`
4. En Telegram, busca a tu bot y envía un archivo de audio en español en formato mp3

## Tecnologías utilizadas

- Python
- OpenAI
- Telegram Bot API

## Contribuciones

¡Siéntete libre de contribuir al proyecto! Si tienes alguna idea o sugerencia, por favor abre un issue o envía un pull request.


import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Configurar el registro de logs
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# TOKEN de tu bot de Telegram (reemplázalo con tu token)
TOKEN = '7702108177:AAHLLwm7xDYwpOoLT2N46EmuYORYKr-RjQU'

# Lista de preguntas y respuestas
questions = [
    {"question": "¿Cuál es el propósito principal de la donación de plaquetas?", "options": [("Ayudar a pacientes con enfermedades", "incorrecto"), ("Ayudar a pacientes con enfermedades hematológicas", "correcto"), ("Ayudar a pacientes con enfermedades respiratorias", "incorrecto"), ("Ayudar a pacientes con enfermedades digestivas", "incorrecto")]},
    {"question": "¿Quién puede donar plaquetas?", "options": [("Personas de cualquier edad", "incorrecto"), ("Personas entre 18 y 60 años", "correcto"), ("Personas mayores de 60 años", "incorrecto"), ("Personas menores de 18 años", "incorrecto")]},
    {"question": "¿Cuánto tiempo dura la donación de plaquetas?", "options": [("30 minutos", "incorrecto"), ("1-2 horas", "correcto"), ("3-4 horas", "incorrecto"), ("5-6 horas", "incorrecto")]},
]

# Diccionario para almacenar el estado de cada usuario
user_scores = {}

# Comando /start para iniciar el examen
async def start(update: Update, context: CallbackContext) -> None:
    """Inicia el examen y envía la primera pregunta."""
    chat_id = update.message.chat_id
    logger.info(f"Comando /start recibido de {chat_id}")
    user_scores[chat_id] = {"score": 0, "index": 0}  # Inicializa el puntaje y el índice de preguntas
    await

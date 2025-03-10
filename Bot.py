import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Configuración de logging
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
    user_scores[chat_id] = {"score": 0, "index": 0}  # Inicializa el puntaje y el índice de preguntas
    await send_question(update, context, chat_id)

# Enviar una pregunta con botones interactivos
async def send_question(update: Update, context: CallbackContext, chat_id: int) -> None:
    """Envía la siguiente pregunta con botones de respuesta."""
    user_data = user_scores.get(chat_id)

    if user_data["index"] >= len(questions):
        await context.bot.send_message(chat_id=chat_id, text=f"🎉 ¡Examen terminado! Tu puntaje es {user_data['score']} de {len(questions)}.")
        return

    question_data = questions[user_data["index"]]
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in question_data["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=question_data["question"], reply_markup=reply_markup)

# Responder a los botones y avanzar al siguiente paso
async def button_callback(update: Update, context: CallbackContext) -> None:
    """Maneja las respuestas del usuario y avanza a la siguiente pregunta."""
    query = update.callback_query
    chat_id = query.message.chat_id
    user_data = user_scores.get(chat_id)

    if not user_data:
        await query.answer("Por favor, usa /start para comenzar el examen.")
        return

    if query.data == "correcto":
        user_data["score"] += 1
        await query.edit_message_text("✅ ¡Correcto!")
    else:
        await query.edit_message_text("❌ Incorrecto.")

    user_data["index"] += 1  # Avanza a la siguiente pregunta

    if user_data["index"] < len(questions):
        await send_question(query, context, chat_id)  # Enviar la siguiente pregunta
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"🎉 ¡Examen terminado! Tu puntaje es {user_data['score']} de {len(questions)}.")

# Manejar errores
def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Ocurrió un error: {context.error}")

# Configuración del bot
def main():
    """Función principal para configurar el bot y sus handlers."""
    # Crear la aplicación de Telegram
    application = Application.builder().token(TOKEN).build()

    # Añadir los handlers
    application.add_handler(CommandHandler("start", start))  # Comando /start
    application.add_handler(CallbackQueryHandler(button_callback))  # Responder a los botones

    # Configurar manejo de errores
    application.add_error_handler(error_handler)

    # Iniciar el bot con polling
    application.run_polling()

if __name__ == "__main__":
    main()

{"darkMode":false,"view":null,"customSize":{"flexibleWidth":{},"flexibleHeight":{},"width":{},"height":{}},"names":{"names":{},"customClassNames":{}},"selectedDevice":{"iPhone13Mini":{}},"cornerRadius":{},"connections":{},"orientation":{"portrait":{}}}
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# TOKEN de tu bot de Telegram (reemplázalo con el tuyo)
TOKEN = "7718095588:AAHT16RmZQpw4C2LvV10jThruSTPcyptsLY"

# Lista de preguntas y respuestas
questions = [
    {"question": "¿Cuál es el propósito principal de la donación de plaquetas?", "options": [("Ayudar a pacientes con enfermedades", "incorrecto"), ("Ayudar a pacientes con enfermedades hematológicas", "correcto"), ("Ayudar a pacientes con enfermedades respiratorias", "incorrecto"), ("Ayudar a pacientes con enfermedades digestivas", "incorrecto")]},
    {"question": "¿Quién puede donar plaquetas?", "options": [("Personas de cualquier edad", "incorrecto"), ("Personas entre 18 y 60 años", "correcto"), ("Personas mayores de 60 años", "incorrecto"), ("Personas menores de 18 años", "incorrecto")]},
    {"question": "¿Cuánto tiempo dura la donación de plaquetas?", "options": [("30 minutos", "incorrecto"), ("1-2 horas", "correcto"), ("3-4 horas", "incorrecto"), ("5-6 horas", "incorrecto")]}
    {"question": "¿Qué es el proceso de separación de las plaquetas de la sangre?", "options": [("Diálisis", "incorrecto"), ("Aféresis", "correcto"), ("Transfusión", "incorrecto"), ("Infusión", "incorrecto")]}
    {"question": "¿Por qué es importante donar plaquetas?", "options": [("Para ayudar a pacientes con enfermedades cardíacas", "incorrecto"), ("Para ayudar a pacientes con enfermedades hematológicas", "correcto"), ("Para ayudar a pacientes con enfermedades respiratorias", "incorrecto"), ("Para ayudar a pacientes con enfermedades digestivas", "incorrecto")]}
 
]

# Diccionario para rastrear la posición de cada usuario en el test
user_scores = {}

def start(update: Update, context: CallbackContext) -> None:
    """Inicia el examen y envía la primera pregunta."""
    chat_id = update.message.chat_id
    user_scores[chat_id] = {"score": 0, "index": 0}  # Inicializa el puntaje y el índice de preguntas
    send_question(update, context, chat_id)

def send_question(update: Update, context: CallbackContext, chat_id: int) -> None:
    """Envía la siguiente pregunta con botones de respuesta."""
    user_data = user_scores.get(chat_id)

    if user_data["index"] >= len(questions):
        update.message.reply_text(f"🎉 ¡Examen terminado! Tu puntaje es {user_data['score']} de {len(questions)}.")
        return

    question_data = questions[user_data["index"]]
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in question_data["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=chat_id, text=question_data["question"], reply_markup=reply_markup)

def button_callback(update: Update, context: CallbackContext) -> None:
    """Maneja las respuestas del usuario y avanza a la siguiente pregunta."""
    query = update.callback_query
    chat_id = query.message.chat_id
    user_data = user_scores.get(chat_id)

    if not user_data:
        query.answer("Por favor, usa /start para comenzar el examen.")
        return

    if query.data == "correcto":
        user_data["score"] += 1
        query.edit_message_text("✅ ¡Correcto!")
    else:
        query.edit_message_text("❌ Incorrecto.")

    user_data["index"] += 1  # Avanza a la siguiente pregunta

    if user_data["index"] < len(questions):
        send_question(query, context, chat_id)  # Enviar la siguiente pregunta
    else:
        context.bot.send_message(chat_id=chat_id, text=f"🎉 ¡Examen terminado! Tu puntaje es {user_data['score']} de {len(questions)}.")

# Configuración del bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

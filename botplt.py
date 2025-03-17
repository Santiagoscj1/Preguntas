from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext, Application, MessageHandler, filters
import os

# TOKEN de tu bot de Telegram (reemplázalo con el tuyo)
TOKEN = "7749919832:AAGeUSe3Us1Pc2exRjw59172Z2W-MbRpw6M"

# Lista de preguntas y respuestas
questions = [
    {"question": "¿Cuál es el propósito principal de la donación de plaquetas?", "options": [("Ayudar a pacientes con enfermedades", "incorrecto"), ("Ayudar a pacientes con enfermedades hematológicas", "correcto"), ("Ayudar a pacientes con enfermedades respiratorias", "incorrecto"), ("Ayudar a pacientes con enfermedades digestivas", "incorrecto")]},
    {"question": "¿Quién puede donar plaquetas?", "options": [("Personas de cualquier edad", "incorrecto"), ("Personas entre 18 y 60 años", "correcto"), ("Personas mayores de 60 años", "incorrecto"), ("Personas menores de 18 años", "incorrecto")]},
    {"question": "¿Cuánto tiempo dura la donación de plaquetas?", "options": [("30 minutos", "incorrecto"), ("1-2 horas", "correcto"), ("3-4 horas", "incorrecto"), ("5-6 horas", "incorrecto")]},
    {"question": "¿Qué es el proceso de separación de las plaquetas de la sangre?", "options": [("Diálisis", "incorrecto"), ("Aféresis", "correcto"), ("Transfusión", "incorrecto"), ("Infusión", "incorrecto")]},
    {"question": "¿Por qué es importante donar plaquetas?", "options": [("Para ayudar a pacientes con enfermedades cardíacas", "incorrecto"), ("Para ayudar a pacientes con enfermedades hematológicas", "correcto"), ("Para ayudar a pacientes con enfermedades respiratorias", "incorrecto"), ("Para ayudar a pacientes con enfermedades digestivas", "incorrecto")]}
]

# Diccionario para rastrear la posición de cada usuario en el test
user_scores = {}

async def start(update: Update, context: CallbackContext) -> None:
    """Inicia el examen y envía la primera pregunta."""
    chat_id = update.message.chat_id
    user_scores[chat_id] = {"score": 0, "index": 0}  # Inicializa el puntaje y el índice de preguntas
    await send_question(update, context, chat_id)

async def send_question(update: Update, context: CallbackContext, chat_id: int) -> None:
    """Envía la siguiente pregunta con botones de respuesta."""
    user_data = user_scores.get(chat_id)

    if user_data["index"] >= len(questions):
        await update.message.reply_text(f"🎉 ¡Examen terminado! Tu puntaje es {user_data['score']} de {len(questions)}.\n\nAhora, por favor responde a esta pregunta abierta:")
        await update.message.reply_text("¿Qué te motivó a donar plaquetas?")
        return

    question_data = questions[user_data["index"]]
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in question_data["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=question_data["question"], reply_markup=reply_markup)

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
        # Enviar la pregunta abierta al finalizar el examen
        await context.bot.send_message(chat_id=chat_id, text=f"🎉 ¡Examen terminado! Tu puntaje es {user_data['score']} de {len(questions)}.")
        await context.bot.send_message(chat_id=chat_id, text="Ahora, por favor responde a esta pregunta abierta:")
        await context.bot.send_message(chat_id=chat_id, text="¿Qué te motivó a donar plaquetas?")

async def open_answer(update: Update, context: CallbackContext) -> None:
    """Recibe la respuesta abierta del usuario."""
    user_data = user_scores.get(update.message.chat_id)
    if not user_data:
        await update.message.reply_text("Por favor, usa /start para comenzar el examen.")
        return

    # Guardar la respuesta abierta
    open_response = update.message.text
    # Aquí puedes guardar la respuesta a una base de datos o archivo si lo deseas
    await update.message.reply_text(f"Gracias por tu respuesta: {open_response}\n\n¡Tu participación ha sido registrada!")

# Configuración del bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, open_answer))  # Maneja la respuesta abierta

    # Ejecutar el bot sin pasar el puerto, ya que esto se maneja por Render
    application.run_polling()

# Ejecutar main directamente sin asyncio.run
if __name__ == "__main__":
    main()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ContextTypes
import os

# TOKEN del bot
TOKEN = os.getenv("TELEGRAM_TOKEN", "7749919832:AAGeUSe3Us1Pc2exRjw59172Z2W-MbRpw6M")  # Mejor si lo pones como variable de entorno

# Lista de preguntas y respuestas
questions = {
    "¿Qué son las plaquetas y cuál es su función en la sangre?": "Son fragmentos celulares que ayudan en la coagulación de la sangre.",
    "¿Cuáles son los requisitos para donar plaquetas?": "Tener entre 18 y 60 años, buen estado de salud y peso adecuado.",
    "¿Cuánto tiempo debe pasar entre una donación de plaquetas y otra?": "Generalmente, al menos 15 días.",
    "¿Cómo se extraen las plaquetas del donante?": "Mediante un proceso llamado aféresis.",
    "¿Qué beneficios tiene la donación de plaquetas para los pacientes?": "Ayuda a pacientes con enfermedades como leucemia y otros trastornos hematológicos.",
    "¿Si sufro de alguna enfermedad puedo donar?": "Depende de la enfermedad, algunas condiciones pueden impedir la donación.",
    "¿Cada cuánto se renuevan mis plaquetas?": "Las plaquetas se regeneran en aproximadamente 48 horas.",
    "¿Cuánto dura el proceso de donación?": "El proceso dura entre 1 y 2 horas dependiendo del método utilizado.",
    "¿Qué requisitos tiene?": "Ser mayor de 18 años, pesar más de 50 kg y estar en buen estado de salud.",
    "¿Qué es la donación de plaquetas?": "Es un procedimiento en el que se extraen plaquetas de un donante mediante aféresis para ayudar a pacientes necesitados."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra el menú de preguntas como botones."""
    keyboard = []
    for question in questions.keys():
        keyboard.append([InlineKeyboardButton(text=question, callback_data=question)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    greeting = (
        "Hola, soy *PlasmaBot* 🩸\n\n"
        "Selecciona una pregunta sobre la donación de plaquetas y te daré la respuesta:"
    )
    await update.message.reply_text(greeting, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra la respuesta a la pregunta seleccionada."""
    query = update.callback_query
    await query.answer()

    question = query.data
    answer = questions.get(question, "Lo siento, no tengo respuesta para esa pregunta.")

    await query.edit_message_text(f"*{question}*\n\n{answer}", parse_mode="Markdown")

# Configuración del bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_question))

    print("✅ Bot iniciado correctamente")
    application.run_polling()

if __name__ == "__main__":
    main()


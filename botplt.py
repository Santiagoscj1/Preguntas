from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Token de tu bot
TOKEN = "7749919832:AAGeUSe3Us1Pc2exRjw59172Z2W-MbRpw6M"

# Diccionario de preguntas y respuestas
questions = {
    "q1": ("¿Qué son las plaquetas y cuál es su función en la sangre?",
           "Las plaquetas son fragmentos de células que ayudan a la coagulación de la sangre. Juegan un papel crucial en la detención del sangrado."),
    "q2": ("¿Cuáles son los requisitos para donar plaquetas?",
           "Debes tener entre 18 y 60 años, estar en buen estado de salud, y tener un peso adecuado."),
    "q3": ("¿Cuánto tiempo debe pasar entre una donación de plaquetas y otra?",
           "Normalmente, debes esperar al menos 15 días entre donaciones."),
    "q4": ("¿Cómo se extraen las plaquetas del donante?",
           "Mediante un procedimiento llamado aféresis, a través de una máquina especializada."),
    "q5": ("¿Qué beneficios tiene la donación de plaquetas para los pacientes?",
           "Ayuda a pacientes con leucemia y otros trastornos hematológicos a prevenir hemorragias."),
    "q6": ("¿Si sufro de alguna enfermedad puedo donar?",
           "Depende del tipo de enfermedad. Se realiza una evaluación médica antes de cada donación."),
    "q7": ("¿Cada cuánto se renuevan mis plaquetas?",
           "Las plaquetas se regeneran aproximadamente cada 48 horas."),
    "q8": ("¿Cuánto dura el proceso de donación?",
           "Entre 1 y 2 horas, dependiendo del procedimiento."),
    "q9": ("¿Qué requisitos tiene?",
           "Ser mayor de 18 años, pesar más de 50 kg y gozar de buena salud."),
    "q10": ("¿Qué es la donación de plaquetas?",
            "Es un procedimiento donde se extraen plaquetas de un donante mediante aféresis para ayudar a pacientes necesitados.")
}

# Enviar saludo y botones como mensajes separados
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Saludo
    await update.message.reply_text(
        "👋 ¡Hola! Soy *PlasmaBot*, tu asistente sobre donación de plaquetas.",
        parse_mode="Markdown"
    )

    # Mostrar menú de preguntas
    keyboard = [
        [InlineKeyboardButton(text=question, callback_data=qid)]
        for qid, (question, _) in questions.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Selecciona una pregunta para conocer la respuesta:",
        reply_markup=reply_markup
    )

# Mostrar la respuesta y volver a mostrar el menú
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    qid = query.data
    question, answer = questions.get(qid, ("Pregunta no encontrada", "No tengo una respuesta para eso."))

    await query.edit_message_text(f"*{question}*\n\n{answer}", parse_mode="Markdown")

    # Volver a mostrar el menú
    keyboard = [
        [InlineKeyboardButton(text=q, callback_data=key)]
        for key, (q, _) in questions.items()
    ]
    await query.message.reply_text(
        "¿Deseas saber algo más? Elige otra pregunta:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Configuración principal
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_answer))

    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

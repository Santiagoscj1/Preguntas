from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ContextTypes

# Tu TOKEN del bot
TOKEN = "7749919832:AAGeUSe3Us1Pc2exRjw59172Z2W-MbRpw6M"

# Preguntas y respuestas con IDs cortos
questions = {
    "q1": ("¿Qué son las plaquetas y cuál es su función en la sangre?", 
           "Son fragmentos celulares que ayudan en la coagulación de la sangre."),
    "q2": ("¿Cuáles son los requisitos para donar plaquetas?", 
           "Tener entre 18 y 60 años, buen estado de salud y peso adecuado."),
    "q3": ("¿Cuánto tiempo debe pasar entre una donación de plaquetas y otra?", 
           "Generalmente, al menos 15 días."),
    "q4": ("¿Cómo se extraen las plaquetas del donante?", 
           "Mediante un proceso llamado aféresis."),
    "q5": ("¿Qué beneficios tiene la donación de plaquetas para los pacientes?", 
           "Ayuda a pacientes con enfermedades como leucemia y otros trastornos hematológicos."),
    "q6": ("¿Si sufro de alguna enfermedad puedo donar?", 
           "Depende de la enfermedad, algunas condiciones pueden impedir la donación."),
    "q7": ("¿Cada cuánto se renuevan mis plaquetas?", 
           "Las plaquetas se regeneran en aproximadamente 48 horas."),
    "q8": ("¿Cuánto dura el proceso de donación?", 
           "El proceso dura entre 1 y 2 horas dependiendo del método utilizado."),
    "q9": ("¿Qué requisitos tiene?", 
           "Ser mayor de 18 años, pesar más de 50 kg y estar en buen estado de salud."),
    "q10": ("¿Qué es la donación de plaquetas?", 
            "Es un procedimiento en el que se extraen plaquetas de un donante mediante aféresis para ayudar a pacientes necesitados.")
}

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra el menú de preguntas como botones."""
    keyboard = [
        [InlineKeyboardButton(text=question, callback_data=qid)]
        for qid, (question, _) in questions.items()
    ]

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

    qid = query.data
    question, answer = questions.get(qid, ("Pregunta no encontrada", "No tengo una respuesta para eso."))

    await query.edit_message_text(f"*{question}*\n\n{answer}", parse_mode="Markdown")

def main():
    """Configuración del bot con long polling"""
    application = Application.builder().token(TOKEN).build()

    # Se agrega el comando de inicio del menú
    application.add_handler(CommandHandler("start", show_menu))

    # Se maneja la respuesta de las preguntas
    application.add_handler(CallbackQueryHandler(handle_question))

    # Inicia el bot con long polling (sin webhook)
    application.run_polling()

if __name__ == "__main__":
    main()

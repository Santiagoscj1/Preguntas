from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Token de tu bot
TOKEN = "7749919832:AAGeUSe3Us1Pc2exRjw59172Z2W-MbRpw6M"

# Diccionario de preguntas y respuestas
questions = {
    "q1": ("¿Qué son las plaquetas y cuál es su función en la sangre?",
           "Las plaquetas son fragmentos de células que ayudan a la coagulación de la sangre. Juegan un papel crucial en la detención del sangrado."),
    "q2": ("¿Cuáles son los requisitos para donar plaquetas?",
           "Para donar plaquetas, debes tener entre 18 y 60 años, estar en buen estado de salud, y tener un peso adecuado según la normativa."),
    "q3": ("¿Cuánto tiempo debe pasar entre una donación de plaquetas y otra?",
           "Normalmente, debes esperar al menos 15 días entre donaciones de plaquetas."),
    "q4": ("¿Cómo se extraen las plaquetas del donante?",
           "Las plaquetas se extraen mediante un procedimiento llamado aféresis, que se realiza a través de una máquina especializada."),
    "q5": ("¿Qué beneficios tiene la donación de plaquetas para los pacientes?",
           "Las plaquetas son esenciales para tratar a pacientes con leucemia y otros trastornos hematológicos, ayudando a prevenir hemorragias peligrosas."),
    "q6": ("¿Si sufro de alguna enfermedad puedo donar?",
           "Depende de la enfermedad. Algunas condiciones de salud pueden hacerte inelegible para donar, pero se realiza una evaluación antes de cada donación."),
    "q7": ("¿Cada cuánto se renuevan mis plaquetas?",
           "Las plaquetas se regeneran en un plazo aproximado de 48 horas después de la donación."),
    "q8": ("¿Cuánto dura el proceso de donación?",
           "El proceso de donación puede durar entre 1 y 2 horas, dependiendo del método utilizado y la condición del donante."),
    "q9": ("¿Qué requisitos tiene?", 
           "Ser mayor de 18 años, pesar más de 50 kg y estar en buen estado de salud."),
    "q10": ("¿Qué es la donación de plaquetas?",
            "Es un proceso en el cual se extraen plaquetas de un donante, las cuales son utilizadas para tratar a personas con condiciones médicas que afectan la coagulación de la sangre.")
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra el menú con las preguntas disponibles."""
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

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra la respuesta de la pregunta seleccionada."""
    query = update.callback_query
    await query.answer()
    
    qid = query.data
    question, answer = questions.get(qid, ("Pregunta no encontrada", "No tengo una respuesta para eso."))

    # Responder con la respuesta a la pregunta seleccionada
    await query.edit_message_text(f"*{question}*\n\n{answer}", parse_mode="Markdown")

    # Volver a mostrar el menú de preguntas
    await query.message.reply_text(
        "¿Te gustaría saber algo más? Selecciona otra pregunta:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=q, callback_data=key)]
            for key, (q, _) in questions.items()
        ])
    )

def main():
    """Configuración del bot."""
    application = Application.builder().token(TOKEN).build()

    # Agregar los controladores
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_answer))

    # Iniciar el bot
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

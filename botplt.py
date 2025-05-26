from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import asyncio

TOKEN = "7749919832:AAGeUSe3Us1Pc2exRjw59172Z2W-MbRpw6M"  # 🔁 Reemplaza por tu token

# Diccionario de preguntas y respuestas
questions = {
    "q1": ("¿Qué son las plaquetas y cuál es su función?", "Ayudan en la coagulación de la sangre."),
    "q2": ("¿Requisitos para donar plaquetas?", "Edad entre 18 y 60 años, buena salud y peso adecuado."),
    "q3": ("¿Tiempo entre donaciones?", "Al menos 15 días."),
    "q4": ("¿Cómo se extraen las plaquetas?", "Mediante aféresis."),
    "q5": ("¿Beneficios para los pacientes?", "Ayuda a tratar leucemia y otros trastornos sanguíneos."),
    "q6": ("¿Puedo donar si tengo enfermedades?", "Depende de la enfermedad, algunas lo impiden."),
}

# Mostrar menú de preguntas
def get_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=q, callback_data=key)]
        for key, (q, _) in questions.items()
    ])

# Manejador de cualquier mensaje
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola, soy *PlasmaBot* 🩸\nElige una pregunta:",
        parse_mode="Markdown"
    )
    await update.message.reply_text("Preguntas frecuentes:", reply_markup=get_menu())

# Manejador de selección de pregunta
async def question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    qid = query.data
    question, answer = questions.get(qid, ("Pregunta no encontrada", "No tengo una respuesta para eso."))
    await query.edit_message_text(f"*{question}*\n\n{answer}", parse_mode="Markdown")
    await query.message.reply_text("¿Otra pregunta?", reply_markup=get_menu())

# Main
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start_handler))
    app.add_handler(CallbackQueryHandler(question_handler))
    
    # 🔁 Eliminar Webhook y usar polling (para Render como worker)
    asyncio.run(app.bot.delete_webhook(drop_pending_updates=True))
    app.run_polling()

if __name__ == "__main__":
    main()

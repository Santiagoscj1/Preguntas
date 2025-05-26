from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio

# TOKEN del bot (¡NO LO COMPARTAS públicamente en producción!)
TOKEN = "7749919832:AAGeUSe3Us1Pc2exRjw59172Z2W-MbRpw6M"

# Preguntas y respuestas
questions = {
    "q1": ("¿Qué son las plaquetas y cuál es su función?", "Son fragmentos celulares que ayudan en la coagulación de la sangre."),
    "q2": ("¿Requisitos para donar plaquetas?", "Tener entre 18 y 60 años, buen estado de salud y peso adecuado."),
    "q3": ("¿Cuánto tiempo entre donaciones?", "Generalmente, al menos 15 días."),
    "q4": ("¿Cómo se extraen las plaquetas?", "Mediante un proceso llamado aféresis."),
    "q5": ("¿Beneficios para los pacientes?", "Ayuda a pacientes con leucemia y otros trastornos hematológicos.")
}

# Mostrar saludo y preguntas
async def send_greeting_and_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Soy *PlasmaBot*, tu asistente sobre donación de plaquetas.", parse_mode="Markdown")
    await send_menu(update, context)

# Mostrar menú de preguntas
async def send_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text=question, callback_data=qid)]
        for qid, (question, _) in questions.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("📌 Selecciona una pregunta:", reply_markup=reply_markup)

# Manejar selección de pregunta
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    qid = query.data
    question, answer = questions.get(qid, ("Pregunta no encontrada", "No tengo una respuesta para eso."))

    await query.edit_message_text(f"*{question}*\n\n{answer}", parse_mode="Markdown")
    await query.message.reply_text("❓ ¿Deseas saber algo más?")
    await send_menu(update, context)

# Main
async def main():
    application = Application.builder().token(TOKEN).build()

    # Elimina cualquier webhook existente antes de usar polling (evita conflicto)
    await application.bot.delete_webhook(drop_pending_updates=True)

    # Manejadores
    application.add_handler(CommandHandler("start", send_greeting_and_menu))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_greeting_and_menu))
    application.add_handler(CallbackQueryHandler(handle_question))

    print("✅ Bot iniciado en modo polling...")
    await application.run_polling()

# Ejecutar
if __name__ == "__main__":
    asyncio.run(main())

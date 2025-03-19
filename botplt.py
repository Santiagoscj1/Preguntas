from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, Application
import os
import difflib

# TOKEN de tu bot de Telegram
TOKEN = "7749919832:AAGeUSe3Us1Pc2exRjw59172Z2W-MbRpw6M"

# Lista de preguntas y respuestas correctas
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

# Diccionario para rastrear la posición de cada usuario en el test
user_scores = {}

def check_answer(user_answer, correct_answer):
    """Compara la respuesta del usuario con la correcta usando similitud."""
    similarity = difflib.SequenceMatcher(None, user_answer.lower(), correct_answer.lower()).ratio()
    if similarity > 0.7:
        return "correcto"
    elif similarity > 0.4:
        return "parcialmente correcto"
    else:
        return "incorrecto"

async def start(update: Update, context: CallbackContext) -> None:
    """Envía un saludo y la primera pregunta."""
    chat_id = update.message.chat_id
    user_scores[chat_id] = {"score": 0, "index": 0}  # Inicializa el puntaje y el índice de preguntas
    
    greeting = "Hola, mi nombre es PlasmaBot. Bienvenido a este espacio donde yo seré tu asistente virtual y juntos resolveremos todas las dudas que tengas al respecto."
    await update.message.reply_text(greeting)
    await send_question(update, context, chat_id)

async def send_question(update: Update, context: CallbackContext, chat_id: int) -> None:
    """Envía la siguiente pregunta."""
    user_data = user_scores.get(chat_id)
    
    question_list = list(questions.keys())
    if user_data["index"] >= len(question_list):
        await update.message.reply_text(f"🎉 ¡Examen terminado! Tu puntaje es {user_data['score']} de {len(questions)}.")
        return
    
    question_text = question_list[user_data["index"]]
    await context.bot.send_message(chat_id=chat_id, text=question_text)

async def receive_answer(update: Update, context: CallbackContext) -> None:
    """Recibe y evalúa la respuesta del usuario."""
    chat_id = update.message.chat_id
    user_data = user_scores.get(chat_id)
    
    if not user_data:
        await update.message.reply_text("Por favor, usa /start para comenzar el examen.")
        return
    
    question_list = list(questions.keys())
    correct_answer = questions[question_list[user_data["index"]]]
    user_answer = update.message.text
    
    result = check_answer(user_answer, correct_answer)
    if result == "correcto":
        user_data["score"] += 1
        await update.message.reply_text("✅ ¡Correcto!")
    elif result == "parcialmente correcto":
        await update.message.reply_text(f"⚠️ Parcialmente correcto. Considera esta respuesta: {correct_answer}")
    else:
        await update.message.reply_text(f"❌ Incorrecto. Una posible respuesta sería: {correct_answer}")
    
    user_data["index"] += 1  # Avanza a la siguiente pregunta
    await send_question(update, context, chat_id)

# Configuración del bot
def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_answer))  # Maneja respuestas abiertas
    
    application.run_polling()

# Ejecutar main directamente
if __name__ == "__main__":
    main()

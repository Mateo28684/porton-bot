import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8510199817:AAHpMK__hZQMz56VEk4s9ILNoarbIjupxU8'
estado_porton = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_menu_control(update)

async def enviar_menu_control(update_or_query):
    keyboard = [
        [InlineKeyboardButton("🔓 Abrir Portón", callback_data='abrir')],
        [InlineKeyboardButton("🔒 Cerrar Portón", callback_data='cerrar')],
        [InlineKeyboardButton("🔄 Actualizar", callback_data='estado')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    texto_estado = "ABIERTO 🟢" if estado_porton == 1 else "CERRADO 🔴"
    mensaje = f"🤖 *Control de Portón Digital*\n\nEstado actual: {texto_estado}"

    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text(mensaje, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update_or_query.edit_message_text(mensaje, reply_markup=reply_markup, parse_mode='Markdown')

async def gestionar_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global estado_porton
    query = update.callback_query
    await query.answer()

    if query.data == 'abrir':
        if estado_porton == 0:
            await query.edit_message_text("⏳ Abriendo portón...")
            await asyncio.sleep(2)
            estado_porton = 1
            await enviar_menu_control(query)
        else:
            await query.answer("⚠️ El portón ya está abierto", show_alert=True)
    elif query.data == 'cerrar':
        if estado_porton == 1:
            await query.edit_message_text("⏳ Cerrando portón...")
            await asyncio.sleep(2)
            estado_porton = 0
            await enviar_menu_control(query)
        else:
            await query.answer("⚠️ El portón ya está cerrado", show_alert=True)
    elif query.data == 'estado':
        await enviar_menu_control(query)

if __name__ == '__main__':
    print("Bot iniciado!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(gestionar_botones))
    app.run_polling()

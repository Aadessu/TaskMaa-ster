from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. The Welcome Message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! I am TaskMaa-ster. \n"
        "Send /task <chore> to start nagging."
    )

# 2. The Nagging Function (This runs on a loop)
async def nag_routine(context: ContextTypes.DEFAULT_TYPE):
    # Grab the chat_id and task from the job's context data
    chat_id = context.job.chat_id
    task = context.job.data

    # We will replace this static test with AI-generated Hindi 
    # scoldings later
    scolding = f"Maa is asking: Why haven't you finished '{task}' yet?! Get up and do it!"
    await context.bot.send_message(chat_id, scolding)

# 3. Starting the Task and Timer
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id

    # Grab the words sent after the / task command
    task = " ".join(context.args) if context.args else "the pending work"

    # Schedule the nag_routine to run every 15 seconds (for testing purposes)
    context.job_queue.run_repeating(
        nag_routine,
        interval=15,
        chat_id=chat_id,
        name=str(chat_id), # I named the job so I can find it and stop it later
        data=task
    )
    await update.message.reply_text(f"Task '{task}' registered. The nagging has officially begun...")

# 4. The Sweet Relief (Stopping the Nag)
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    
    # Cancel the running nag job
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()
        await update.message.reply_text("Task completed! You can sit in peace now... until Maa finds something else.")
    else:
        await update.message.reply_text("No active tasks found.")

# 5. Booting up the Bot
if __name__ == '__main__':
    app = (
        Application.builder()
        .token("YOUR_TELEGRAM_BOT_TOKEN")
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .pool_timeout(30)
        .build()
    )
    
    # These three lines tell the bot how to respond to commands:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", add_task))
    app.add_handler(CommandHandler("done", done))
    
    print("TaskMaa-ster is running...")
    app.run_polling()
import asyncio
from telethon import TelegramClient, events

api_id = '28260542'
api_hash = '5b0c43a7468e5382b66cc885cf8ccb17'
session_name = 'spiderman'

client = TelegramClient(session_name, api_id, api_hash)

group_list = []
spam_message = ""
spam_interval = 5  # Secondi
spam_task = None

async def group_spam():
    while True:
        for group in group_list:
            await client.send_message(group, spam_message)
        await asyncio.sleep(spam_interval)

@client.on(events.NewMessage(pattern=r'\.gadd'))
async def add_group(event):
    group_list.append(event.chat_id)
    group_name = (await client.get_entity(event.chat_id)).title
    await event.respond(f"✅ Gruppo {group_name} aggiunto alla lista di spam.")
    await event.delete()

@client.on(events.NewMessage(pattern=r'\.grem'))
async def remove_group(event):
    if event.chat_id in group_list:
        group_list.remove(event.chat_id)
        group_name = (await client.get_entity(event.chat_id)).title
        await event.respond(f"✅ Gruppo {group_name} rimosso dalla lista di spam.")
    await event.delete()

@client.on(events.NewMessage(pattern=r'\.gsetmex'))
async def set_spam_message(event):
    global spam_message
    if event.is_reply:
        reply = await event.get_reply_message()
        spam_message = reply.message
        await event.respond("✅ Messaggio di spam impostato.")
    await event.delete()

@client.on(events.NewMessage(pattern=r'\.gspam'))
async def start_spam(event):
    global spam_task
    if spam_task is None:
        spam_task = asyncio.create_task(group_spam())
        await event.respond("🔄 Spam nei gruppi avviato.")
    await event.delete()

@client.on(events.NewMessage(pattern=r'\.gstop'))
async def stop_spam(event):
    global spam_task
    if spam_task is not None:
        spam_task.cancel()
        spam_task = None
        await event.respond("⏹️ Spam fermato nei gruppi.")
    await event.delete()

@client.on(events.NewMessage(pattern=r'\.gtime (\d+)'))
async def set_interval(event):
    global spam_interval
    spam_interval = int(event.pattern_match.group(1))
    await event.respond(f"⏱️ Intervallo di spam impostato a {spam_interval} secondi.")
    await event.delete()

@client.on(events.NewMessage(pattern=r'\.glist'))
async def show_groups(event):
    await event.delete()
    if group_list:
        group_list_str = "\n".join([(await client.get_entity(group)).title for group in group_list])
        await client.send_message(event.chat_id, f"📋 Gruppi configurati per lo spam:\n{group_list_str}")
    else:
        await client.send_message(event.chat_id, "📋 Nessun gruppo configurato per lo spam.")

@client.on(events.NewMessage(pattern=r'\.cmd'))
async def show_commands(event):
    await event.respond("""🛠️ Comandi dello SpamBot

Ecco i comandi che puoi usare:
📎 Clicca qui per la guida dettagliata → https://telegra.ph/SPAMBOT-07-03-2

🔍 Come usarli:
1️⃣ Leggi la documentazione
2️⃣ Esegui i comandi secondo le istruzioni
3️⃣ Se incontri problemi, contatta il supporto

💬 Supporto:
Per assistenza extra, scrivi a @erpumba 👤""")
    await event.delete()

@client.on(events.NewMessage(pattern=r'\.grestart'))
async def restart_bot(event):
    await event.respond("♻️ Riavvio del bot...")
    await event.delete()
    asyncio.create_task(restart())

async def restart():
    await client.disconnect()
    await asyncio.sleep(1)
    await client.connect()
    print("Userbot riavviato.")

async def main():
    await client.start()
    print("Userbot in esecuzione...")
    await client.run_until_disconnected()

asyncio.run(main())

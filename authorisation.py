from pyrogram import Client, filters
from pyrogram.types import Message
from config import auth_users, sudo_users

# Auth command
@Client.on_message(filters.command("auth"))
async def auth_command(client, message: Message):
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id not in auth_users:
        await message.reply("❌ You are not authorized to use this command.")
        return
    
    try:
        # Get the user ID to authorize
        args = message.text.split()
        if len(args) < 2:
            await message.reply("❌ Usage: /auth user_id")
            return
            
        target_user_id = int(args[1])
        
        # Check if user already authorized
        if target_user_id in sudo_users:
            await message.reply("✅ User is already authorized!")
            return
            
        sudo_users.append(target_user_id)
        await message.reply(f"✅ User {target_user_id} has been authorized to use the bot!")
        
    except (IndexError, ValueError):
        await message.reply("❌ Usage: /auth user_id\n\nExample: /auth 6966002582")

# Remove user command
@Client.on_message(filters.command("remove"))
async def remove_command(client, message: Message):
    user_id = message.from_user.id
    
    if user_id not in auth_users:
        await message.reply("❌ You are not authorized to use this command.")
        return
    
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.reply("❌ Usage: /remove user_id")
            return
            
        target_user_id = int(args[1])
        
        if target_user_id not in sudo_users:
            await message.reply("❌ User is not in authorized list!")
            return
            
        sudo_users.remove(target_user_id)
        await message.reply(f"✅ User {target_user_id} has been removed from authorized list!")
        
    except (IndexError, ValueError):
        await message.reply("❌ Usage: /remove user_id\n\nExample: /remove 6966002582")

# List users command
@Client.on_message(filters.command("users"))
async def list_users(client, message: Message):
    user_id = message.from_user.id
    if user_id not in auth_users:
        await message.reply("❌ You are not authorized to use this command.")
        return
    
    if not sudo_users:
        await message.reply("📝 No authorized users yet!")
        return
    
    users_list = "\n".join([f"👤 {uid}" for uid in sudo_users])
    await message.reply(f"Authorized Users:\n{users_list}")

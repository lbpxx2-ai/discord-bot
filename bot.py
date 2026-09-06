import os
import discord
import discord.app_commands as app_commands
import hashlib
import aiohttp

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

SECRET_SALT = "MySecretCode1234"
# Webhook สำหรับเก็บบันทึก HWID ลง list
HWID_LIST_WEBHOOK = "https://discordapp.com/api/webhooks/1545998608082542733/LSNoDK9W8M649b666W6xyTHqu8eGCvvBff5Bs3TmxOecRQ9OZ89q5FY2tGzIBSuHlvLA"

@tree.command(name="genkey", description="สร้าง Key สำหรับ HWID และบันทึกลงระบบอัตโนมัติ")
@app_commands.describe(hwid="วาง HWID ของเพื่อนที่นี่")
async def genkey(interaction: discord.Interaction, hwid: str):
    clean_hwid = hwid.strip()
    
    # 1. คำนวณ Key
    raw_data = clean_hwid + SECRET_SALT
    hash_bytes = hashlib.md5(raw_data.encode('ascii')).digest()
    generated_key = "".join(f"{b:02X}" for b in hash_bytes)
    
    # 2. ส่ง HWID ไปบันทึกในห้อง hwid_list ผ่าน Webhook
    async with aiohttp.ClientSession() as session:
        payload = {"content": f"`{clean_hwid}`"}
        async with session.post(HWID_LIST_WEBHOOK, json=payload) as resp:
            pass

    # 3. ตอบกลับใน Discord
    await interaction.response.send_message(f"🔑 **HWID:** `{clean_hwid}`\n🎁 **Key:** `{generated_key}`\n✅ **ระบบได้บันทึก HWID ลง list สำเร็จแล้ว**")

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot Login สำเร็จ : {client.user}")

# ดึง Token จากระบบ Railway (Environment Variables) เพื่อความปลอดภัย
client.run(os.getenv("TOKEN"))
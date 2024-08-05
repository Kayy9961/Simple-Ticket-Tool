import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

canal_id = int(input("Por favor, ingresa el ID del canal donde deseas enviar el botón de crear ticket: "))

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    canal = bot.get_channel(canal_id)
    if canal is None:
        print("Canal no encontrado. Asegúrate de que el ID es correcto.")
        return

    boton = Button(label="Crear Ticket", style=discord.ButtonStyle.primary)

    async def crear_ticket(interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True)
        }
        ticket_channel = await guild.create_text_channel(f"ticket-{member.name}", overwrites=overwrites)
        await ticket_channel.send(f"Hola {member.mention}, este es tu ticket.")
        await interaction.response.send_message(f"Ticket creado: {ticket_channel.mention}", ephemeral=True)

    boton.callback = crear_ticket

    vista = View()
    vista.add_item(boton)

    await canal.send("Haz clic en el botón para crear un ticket.", view=vista)
    print(f"Botón de creación de ticket enviado al canal: {canal.name}")

bot.run('EL TOKEN DE TU BOT')

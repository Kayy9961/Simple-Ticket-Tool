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

    boton_crear = Button(label="Crear Ticket", style=discord.ButtonStyle.primary)

    async def crear_ticket(interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True)
        }
        ticket_channel = await guild.create_text_channel(f"ticket-{member.name}", overwrites=overwrites)
        await ticket_channel.send(f"Hola {member.mention}, este es tu ticket.")

        boton_cerrar = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger)

        async def cerrar_ticket(interaction: discord.Interaction):
            await interaction.channel.delete()
            await interaction.response.send_message("El ticket ha sido cerrado.", ephemeral=True)

        boton_cerrar.callback = cerrar_ticket

        embed = discord.Embed(
            title="Cierra tu Ticket",
            description="Presiona el botón de abajo para cerrar este ticket.",
            color=discord.Color.blue()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        vista_cerrar = View()
        vista_cerrar.add_item(boton_cerrar)

        await ticket_channel.send(embed=embed, view=vista_cerrar)

        await interaction.response.send_message(f"Ticket creado: {ticket_channel.mention}", ephemeral=True)

    boton_crear.callback = crear_ticket

    vista_crear = View()
    vista_crear.add_item(boton_crear)

    await canal.send("Haz clic en el botón para crear un ticket.", view=vista_crear)
    print(f"Botón de creación de ticket enviado al canal: {canal.name}")

bot.run('EL TOKEN DE TU BOT')

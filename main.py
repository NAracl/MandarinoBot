import discord
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
TOKEN = 'secreto pa'
intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(
    command_prefix= '-m ', intents=intents
)
#LISTAS
img_mandarino = [
    "mandarino1.webp",
    "mandarino2.webp",
    "mandarino3.webp",
    "mandarino4.webp",
]
#EN LISTO
@client.event
async def on_ready():
    print(f'Conectado como {client.user}')

#MANEJO DE ERRORES
@client.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.errors.RoleNotFound):
        await ctx.send('`El rol no pudo ser encontrado`')
    elif isinstance(error,commands.errors.MissingRequiredArgument):
        await ctx.send("`Argumento faltante, ¿Estás seguro que el comando va así?`")
    elif isinstance(error,commands.errors.MemberNotFound):
        await ctx.send("`Parece que no puedo encontrar la persona, asegurate de escribir tal cual el nombre con mayúsculas o minúsculas!`")
    elif isinstance(error,commands.errors.MissingPermissions):
        await ctx.send("`Parece que los permisos para usar este comando no coinciden`")
    else:
        print(error)
        await ctx.send('`Error y reporte mandado automáticamente!`')

#COMANDOS
@client.command(aliases=['p'])
async def saludo(ctx):
    img = random.choice(img_mandarino)
    file = discord.File(img, filename=img)
    Embed = discord.Embed(title=None,description=None)
    Embed.set_image(url=f'attachment://{img}')
    if img == "mandarino1.webp":
        Embed.set_footer(text="Créditos a @satorinya (Satori)")
    elif img == "mandarino2.webp":
        Embed.set_footer(text="Créditos a @smylk (Esmaili666)")
    elif img == "mandarino3.webp":
        Embed.set_footer(text="Créditos a @staryomi (StaryPro888)")
    elif img == "mandarino4.webp":
        Embed.set_footer(text="Créditos a @prek69 (Prek)")
    await ctx.send(file=file,embed=Embed)

#COMANDOS DE ROL
@client.command(aliases=['role','addrole','rol','añadirrol'])
async def nuevo_rol(ctx, color):
    color = color.replace("#","")
    member = ctx.message.author
    serv = ctx.guild
    roles = await serv.fetch_roles()
    listado = len(roles)
    print(f"Roles actuales: {listado}")
    if get(serv.roles,name=f"{member.name}"):
        await ctx.send(f"```{member.name} ya tienes un rol a tu nombre, eliminalo primero para hacer otro```")
    else:
        if color == None:
            await ctx.send(f'```Ey {member.name}, te faltó el color, usalo como -m rol (tu color en hex)```')
        hex_color = f"0x{color}"
        nuevo_rol = await serv.create_role(name=f'{member.name}', colour=discord.Colour(int(hex_color,base=16)))
        await nuevo_rol.edit(position=listado - 11)
        await member.add_roles(nuevo_rol)
        await ctx.send('```Rol creado con éxito!```')


@client.command(aliases=['eliminar',"eliminarrol"])
async def eliminar_rol(ctx):
    author = ctx.message.author
    rol = discord.utils.get(ctx.guild.roles, name=author.name)
    if rol:
        await rol.delete()
        await ctx.send(f'```Rol {rol.name} eliminado!```')
    else:
        await ctx.send(f'```No se encontró un rol con el nombre {author.name}```')

@client.command(aliases=['arol','asignarrol'])
@has_permissions(manage_roles=True)
async def asignar_rol(ctx, rol : discord.Role = None, member : discord.Member = None):
    author= ctx.message.author
    if rol == None:
        await ctx.send(f'```Nuh uh {author.name}```')
    elif member == None:
        await ctx.send(f'```Nuh uh {author.name}```')
    else:
        await member.add_roles(rol)
        await ctx.send(f'```El rol {rol.name} se ha añadido sin excepción a {member.name}```')

@client.command(aliases=['qrol','quitarrol'])
@has_permissions(manage_roles=True)
async def quitar_rol(ctx, member :discord.Member=None):
    author= ctx.message.author
    rol = get(ctx.guild.roles, name=member.name)
    if rol == None:
        await ctx.send(f'```No se encontró{author.name}```')
    elif member == None:
        await ctx.send(f'No mencionaste un usuario {author.name}')
    else:
        await member.remove_roles(rol)
        await ctx.send(f'```El rol {rol.name} se ha retirado sin excepción```')      

#COMANDO DE HELP
client.remove_command("help")

@client.group(aliases=["ayuda"])
async def help(ctx):
    file = discord.File("banner1.png", filename= 'banner1.png')
    Embed = discord.Embed(title="Menú de Ayuda",description="Aquí hay una lista completa de todos los comandos de Mandarino actualmente, puedes encontrar más información con -m help (comando de tu elección)" )
    Embed.add_field(name='Roles', value='Añadir rol (rol), Eliminar rol (Eliminar)')
    Embed.set_image(url="attachment://banner1.png")
    Embed.set_footer(text="Créditos a @smylk (Esmaili666)")
    await ctx.send(file=file,embed=Embed)

@help.command(aliases=['Añadir rol','añadir rol','rol','addrole'])
async def rol_help(ctx):
    file = discord.File("colorhex.png", filename= 'colorhex.png')
    Embe = discord.Embed(title='Añadir Rol', description='Este comando sirve para añadir el rol al servidor, únicamente un usuario puede tener uno propio.')
    Embe.add_field(name='Otros nombres: addrole', value='El uso correcto de este comando es ```-m rol (código hex del color)```')
    Embe.add_field(name='¿Cómo saber el valor hex de un color?', value='[Aquí](https://www.color-hex.com/) podrás encontrar una página en donde podrás encontrar los códigos hex para cada color, en caso que sea uno distinto, en la parte superior aparece una ventana en la cual podrás seleccionar el color de tu elección.', inline=False)
    Embe.set_image(url="attachment://colorhex.png")
    await ctx.send(file=file,embed=Embe)
@help.command(aliases=['Eliminar','eliminar','erol','eliminarrol'])
async def eliminar_help(ctx):
    Embe = discord.Embed(title='Eliminar Rol', description='Este comando sirve para eliminar el rol de color del servidor.')
    Embe.add_field(name='Otros nombres: eliminarrol', value='El uso correcto de este comando es ```-m eliminar```')
    await ctx.send(embed=Embe)
@help.command(aliases=['arol','qrol','asignarrol','quitarrol'])
async def arol_qrol(ctx):
    Embe = discord.Embed(title='Quitar Roles', description='(SOLO MOD) Este comando sirve para quitar roles del mismo nombre a un miembro del servidor.')
    Embe.add_field(name='Quitar rol (qrol, quitarrol)', value='El uso correcto de este comando es ```-m qrol (nombre de rol) (nombre de usuario)```')
    await ctx.send(embed=Embe)
#CORRER TOKEN
client.run(TOKEN)

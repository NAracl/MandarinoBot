import discord
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
TOKEN = 'MTE3NzgwNTU4MDYzMTU0ODAwNQ.GotYz0.6xEutGykLDPtem0tBg2DwhHIM6PrQH4-zh6YMk'
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
@client.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.errors.RoleNotFound):
        await ctx.send('`El rol no pudo ser encontrado`')
    elif isinstance(error,commands.errors.MissingRequiredArgument):
        await ctx.send("`Argumento faltante, ¿Estás seguro que el comando va así?`")
    elif isinstance(error,commands.errors.MemberNotFound):
        await ctx.send("`Parece que no puedo encontrar la persona, asegurate de escribir tal cual el nombre con mayúsculas o minúsculas!`")
    elif isinstance(error,commands.errors.MissingPermissions):
        await ctx.send("`Mis permisos no pueden hacer la acción dicha, quizás falta que mi rol tenga mayor prioridad`")
    else:
        print(error)
        await ctx.send('`Error y reporte mandado automáticamente!`')

#COMANDOS
@client.command(aliases=['p'])
async def saludo(ctx):
    img = random.choice(img_mandarino)
    file = discord.File(img)
    await ctx.send(file= file)

#COMANDOS DE ROL
@client.command(aliases=['role','addrole','rol','añadirrol'])
@has_permissions(manage_roles=True)
async def nuevo_rol(ctx, color):
    color = color.replace("#","")
    member = ctx.message.author
    serv = ctx.guild
    if get(serv.roles,name=f"{member.name}"):
        await ctx.send(f"```{member.name} ya tienes un rol a tu nombre, eliminalo primero para hacer otro```")
    else:
        if color == None:
            await ctx.send(f'```Ey {member.name}, te faltó el color, usalo como -m rol (tu color en hex)```')
        hex_color = f"0x{color}"
        await serv.create_role(name=f'{member.name}', colour=discord.Colour(int(hex_color,base=16)))
        await ctx.send('```Rol creado con éxito!```')

@client.command(aliases=['eliminar',"eliminarrol"])
@has_permissions(manage_roles=True)
async def eliminar_rol(ctx, rol : discord.Role = None):
    author = ctx.message.author
    if rol == None:
        await ctx.send(f'```Nuh uh{author.name}, tienes que mencionar un rol o tu mismo nickname```')
    else:
        try:
            await rol.delete()
            await ctx.send(f'```Rol {rol.name} eliminado```')
        except:
            await ctx.send('```No se pudo joven```')

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
async def quitar_rol(ctx, rol: discord.Role = None, member :discord.Member=None):
    author= ctx.message.author
    if rol == None:
        await ctx.send(f'```Nuh uh {author.name}```')
    elif member == None:
        await ctx.send(f'Nuh uh {author.name}')
    else:
        await member.remove_roles(rol)
        await ctx.send(f'```El rol {rol.name} se ha retirado sin excepción de {member.name}```')      

#COMANDO DE HELP
client.remove_command("help")

@client.group(aliases=["ayuda"])
async def help(ctx):
    Embed = discord.Embed(title="Menú de Ayuda",description="Aquí hay una lista completa de todos los comandos de Mandarino actualmente, puedes encontrar más información con -m help (comando de tu elección)" )
    Embed.add_field(name='Roles', value='Añadir rol (rol), Eliminar rol (Eliminar), Asignar rol (arol), Quitar rol (qrol)')
    await ctx.send(embed=Embed)

@help.command(aliases=['Añadir rol','añadir rol','rol','addrole'])
async def rol_help(ctx):
    Embe = discord.Embed(title='Añadir Rol', description='Este comando sirve para añadir nuevos roles al servidor.')
    Embe.add_field(name='Otros nombres: addrole, rol', value='El uso correcto de este comando es ```-m rol (código hex del color)```')
    Embe.add_field(name='¿Cómo saber el valor hex de un color?', value='Debes ir al buscador de tu preferencia (Google especialmente) y buscar "color hex", de ahí te aparecerá una ventana para seleccionar tu color y debajo aparecerá el color hex, lo copiarás y después lo incluiras en el comando como se menciono arriba', inline=False)
    await ctx.send(embed=Embe)
#CORRER TOKEN
client.run(TOKEN)
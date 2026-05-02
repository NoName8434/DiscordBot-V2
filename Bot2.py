import os
import discord
from discord.ext import commands
import datetime
import random
from dotenv import load_dotenv
from google import genai
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_KEY')

# Khởi tạo Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # đọc lệnh !prefxi
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
client = genai.Client(api_key=GEMINI_API_KEY)



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        user_prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()

        if user_prompt:
            async with message.channel.typing():
                try:

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_prompt
                    )

                    if response.text:
                        await message.reply(response.text)
                    else:
                        await message.reply("Tôi không biết trả lời sao nữa...")
                except Exception as e:
                    await message.reply(f"Đầu óc đang 'vật lộn' với tí lỗi: {e}")
        else:
            await message.reply("Gọi gì tôi thế? Tag kèm câu hỏi nhé!")

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'Đã đăng nhập thành công: {bot.user.name}')
    # Hiển thị trạng thái trên Discord
    await bot.change_presence(activity=discord.Game(name="Dùng !help để xem lệnh"))


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1210222998083215472)
    if channel:
        embed = discord.Embed(
            title="Chào mừng thành viên mới!",
            description=f"Chào mừng {member.mention} đã tham gia server!",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)



@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Không có lý do"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"Đã đuổi **{member.display_name}** khỏi server. Lý do: {reason}")
    except Exception as e:
        await ctx.send(f"Không thể đuổi người này: {e}")



@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Không có lý do"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f" Đã cấm **{member.display_name}** vĩnh viễn. Lý do: {reason}")
    except Exception as e:
        await ctx.send(f"Không thể cấm người này: {e}")



@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    try:

        banned_users = [entry async for entry in ctx.guild.bans()]


        for ban_entry in banned_users:
            user = ban_entry.user
            if (f"{user.name}#{user.discriminator}" == member_name) or (user.name == member_name):
                await ctx.guild.unban(user)
                await ctx.send(f" Đã gỡ cấm cho **{user.name}**. Chào mừng quay trở lại!")
                return

        await ctx.send(f"Không tìm thấy ai tên `{member_name}` trong danh sách bị ban.")

    except Exception as e:
        await ctx.send(f" Lỗi gỡ cấm: {e}")


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Danh sách lệnh hỗ trợ",
        description=(
            "**!about**: Giới thiệu bot\n"
            "**!kick @user**: Đuổi thành viên\n"
            "**!ban @user**: Cấm thành viên\n"
            "**!timeout @user <giây>**: Tạm khóa thành viên\n"
            "**!meme**: Gửi ảnh chế\n"
            "**!nguoiphanxu**: Video đặc biệt"
            "có vài command ẩn, tự tìm đi :))))"
        ),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


@bot.command()
async def nguoiphanxu(ctx):
    embed = discord.Embed(title="Người Phán Xử", color=discord.Color.dark_red())

    video_path = r"C:\Users\Admin\Videos\537529894_10013025562136594_2339383991757626406_n.mp4"

    try:
        await ctx.send(embed=embed)
        await ctx.send(file=discord.File(video_path))
    except Exception as e:
        await ctx.send(f"Lỗi gửi file: {e}")


@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, seconds: int, *, reason="Không có lý do"):
    try:
        duration = datetime.timedelta(seconds=seconds)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"Đã tạm khóa {member.mention} trong {seconds} giây. Lý do: {reason}")
    except Exception as e:
        await ctx.send(f"Không thể timeout: {e}")


@bot.command()
async def meme(ctx):
    list_meme = [
        "https://i.postimg.cc/htZPDcfF/ff8bd9e5-60d8-4d00-bd3f-f2d6c3e9d242.jpg",
        "https://i.postimg.cc/XYYY6p7W/f94f1a77-f8c3-4b9b-b94e-130465a673b8.jpg",
        "https://i.postimg.cc/Z5sKb4CZ/e99bd92d-d378-4fda-b56a-76bb61231ae0.jpg",
        "https://i.postimg.cc/x111VcT0/dc18d045-5ea9-4fe0-8596-61d71be86886.jpg",
        "https://i.postimg.cc/BnnnfXZd/dadbab2b-e2fe-40ae-b519-7c93d89d5495.jpg",
        "https://i.postimg.cc/Njjjv5fw/ce7f610d-b096-46b1-92f3-aee8dea7afe4.jpg",
        "https://i.postimg.cc/MpppJvZs/c858b9dd-7c85-420e-9041-a6ce6cf21608.jpg",
        "https://i.postimg.cc/htZPDcf4/c4810db2-193d-4c09-be55-0d50acffad44.jpg",
        "https://i.postimg.cc/MpppJvZ9/bc3bd0f0-9b0e-4637-8f53-89f0b95851b6.jpg",
        "https://i.postimg.cc/y888CkYY/b5968b69-3fec-4509-9bab-a44e4ca7f707.jpg",
        "https://i.postimg.cc/3xxxQdrz/aa7e0a4d-a7c7-4a8a-9595-17d133ab4fbf.jpg",
        "https://i.postimg.cc/T333vpYf/a7e85f89-aeb6-40e0-84be-5e5af3c13d3f.jpg",
        "https://i.postimg.cc/Bn7QS4XG/9196847c-ca2d-4d09-96ea-007192155085.jpg",
        "https://i.postimg.cc/BnnnfXQs/9186c6b7-80d7-4342-bd00-dff68adfd568.jpg",
        "https://i.postimg.cc/3xfJ8YdR/80a863e5-637e-4626-9d2f-46a4093cf14b.jpg",
        "https://i.postimg.cc/FHHHX7sX/8025459e-c2a5-46b5-b35c-ffd9eb488c44.jpg",
        "https://i.postimg.cc/T333vpY2/7e122364-4e0a-4cc4-b686-4acbb13c86bd.jpg",
        "https://i.postimg.cc/P5VrXTNg/7d092fd0-3b40-4af2-a291-f0340d77abcd.jpg",
        "https://i.postimg.cc/K8pvGxRb/7cb579b7-f77e-4cc0-bcff-0f1315d12754.jpg",
        "https://i.postimg.cc/HkvsYdVp/7264fc60-262e-4f61-9d94-b56413bc1f99.jpg",
        "https://i.postimg.cc/T3NYdfpd/65c2de1d-f1f8-406d-9a8f-b1c458fd72b5.jpg",
        "https://i.postimg.cc/W1YbNThs/642c7430-2347-4ac8-b534-83ff07dad936.jpg",
        "https://i.postimg.cc/JzY4rMGh/4f355cd1-9dae-4a41-ae6d-830baa5add16.jpg",
        "https://i.postimg.cc/sgggCvf0/4bac4f96-fbaa-49c2-beff-c9a7b8abc80b.jpg",
        "https://i.postimg.cc/y888Ck6Q/43b20de0-edfd-4fc5-bdd0-8ea7590e0648.jpg",
        "https://i.postimg.cc/4x2NfsmN/3adce3ba-7485-4d39-ad85-7614344bb034.jpg",
        "https://i.postimg.cc/wj4Tqg7g/0c8a523e-ad5d-4f31-abed-f8c192e6c7ec.jpg",
        "https://i.postimg.cc/XYYY6p7M/0c111f4b-930e-4ecd-b644-da7351dea239.jpg",
    ]

    if not list_meme:
        await ctx.send("Kho meme đang trống")
        return

    #random link
    meme_url = random.choice(list_meme)

    embed = discord.Embed(
        title="Meme tươi từ rừng Pác Bó ! 🔥",
        color=discord.Color.random()
    )
    embed.set_image(url=meme_url)
    embed.set_footer(text=f"Yêu cầu bởi: {ctx.author.display_name}")

    await ctx.send(embed=embed)


@bot.command()
async def mingking(ctx):
    embed = discord.Embed(title="Nà ná na na Anh mingking", color=discord.Color.dark_red())

    video_path = r"C:\Users\Admin\Downloads\170ce291-7cf4-4165-83da-ae49e2779409.mp4"

    try:
        await ctx.send(embed=embed)
        await ctx.send(file=discord.File(video_path))
    except Exception as e:
        await ctx.send(f"Lỗi gửi file: {e}")


@bot.command()
async def saygex(ctx):
    video_folder = r"C:\Users\Admin\Videos\SayGex4botdiscord"
    try:

        all_videos = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.mov', '.mkv'))]

        if not all_videos:
            await ctx.send("Thư mục không có video")
            return


        random_video = random.choice(all_videos)
        video_path = os.path.join(video_folder, random_video)

        with open(video_path, 'rb') as f:
            picture = discord.File(f)
            await ctx.send(content=f"Đừng nhìn, yêu đấy🫦🫦👅👅: **{random_video}**", file=picture)

    except FileNotFoundError:
        await ctx.send("Không tìm thấy thư mục")
    except Exception as e:
        await ctx.send(f"Có lỗi xảy ra: {e}")



bot.run(TOKEN)
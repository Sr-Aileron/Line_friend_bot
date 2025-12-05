import discord
import markovify
import MeCab
import configparser
from discord.ext import commands

# config.iniの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
cfg = config_ini['DEFAULT']

# 変数の宣言
bot_state = 'active'
command_list = ['!help', '!active', '!only_mentioned', '!passive', '!state']

# 入力した文字のうち特定の品詞のものを抽出
def analyze_message(message, pos_list):
	tagger = MeCab.Tagger()
	nodes = tagger.parseToNode(message)
	tokens = []
	while nodes:
		if nodes.surface != "":
			tokens.append((nodes.surface, nodes.feature.split(',')[0]))
		nodes = nodes.next
	
	return [token for token, pos in tokens if pos in pos_list]

# 返信の生成
def generate_replys(model, number_of_generation, keywords):
	reply_list = []
	point_list = [0 for _ in range(10)]

	for _ in range(int(number_of_generation)):
		reply_list.append(model.make_sentence())

	for index, sentence in enumerate(reply_list):
		if sentence == None:
			continue
		for keyword in keywords:
			if keyword in sentence:
				point_list[index] += 1
			
	return reply_list[point_list.index(max(point_list))]

DISCORD_TOKEN = cfg['DISCORD_TOKEN']
BOT_USERNAME = cfg['BOT_USERNAME']

# botの生成
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 学習用データの読み込み
with open(cfg['save_path'], 'r') as file:
    vocab = file.read()
model = markovify.NewlineText(vocab, state_size=int(cfg['state_size']), well_formed=False)

@bot.event
async def on_ready():
	print(f"ログインしました: {bot.user.name}")
	print("-----")

@bot.command()
async def state(ctx):
	global bot_state
	await ctx.send(f'現在の状態は {bot_state} です')

@bot.command()
async def start(ctx):
	global bot_state
	bot_state = 'active'
	await ctx.send(f'現在の状態を {bot_state} に設定します\n全てのメッセージに対して返信します')

@bot.command()
async def only_mentioned(ctx):
	global bot_state
	bot_state = 'only_mentioned'
	await ctx.send(f'現在の状態を {bot_state} に設定します\nメンション時のみ返信します')

@bot.command()
async def stop(ctx):
	global bot_state
	bot_state = 'passive'
	await ctx.send(f'現在の状態を {bot_state} に設定します\n返信を行いません')

@bot.event
async def on_message(message):
	if message.content in command_list:
		await bot.process_commands(message)
		return
	if message.author == bot.user or bot_state == 'stop':
		return
	if bot_state == 'only_mentioned' and bot.user not in message.mentions:
		return

	keywords = analyze_message(message.content, ['名詞', '代名詞', '形容詞', '副詞'])
	reply = generate_replys(model, cfg['number_of_generation'], keywords)
	
	await message.channel.send(reply.replace(' ', ''))
	await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
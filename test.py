import discord
import asyncio
import random
import os
import time
import datetime
from urllib.request import urlopen, Request
import urllib
import urllib.request
import bs4
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('jego-972d19158581.json', scope)
client = gspread.authorize(creds)
doc = client.open_by_url('https://docs.google.com/spreadsheets/d/15p6G4jXmHw7Z_iRCYeFwRzkzLxqf-3Pj0c6FeVuFYBM')


client = discord.Client()



@client.event
async def on_ready():
	print("login")
	print(client.user.name)
	print(client.user.id)
	print("----------------")
	await client.change_presence(game=discord.Game(name='업무외지원', type=1))




@client.event
async def on_message(message):
	global gc #정산
	global creds	#정산
	global ladder
    
	if message.content.startswith('!나이'):
		SearchID = message.content[len('!나이')+1:]
		gc = gspread.authorize(creds)
		wks = gc.open('오전재고').worksheet('만나이계산기')
		
		wks.update_acell('C8', SearchID)
		result1 = wks.acell('H8').value
		result2 = wks.acell('J8').value
           
		embed = discord.Embed(
			title = ' 오늘기준 ' + SearchID + ' 나이! ',
			description= '```md\n' + SearchID + result1 + result2 + '```',
			color=0x5ABEFF
			)
		await client.send_message(message.channel, embed=embed)
		
		
	if message.content.startswith('!유지기간'):
		SearchID = message.content[len('!유지기간')+1:]
		gc = gspread.authorize(creds)
		wks = gc.open('오전재고').worksheet('유지기간')
		wks.update_acell('a1', SearchID)
		result = wks.acell('b1').value
		
		embed = discord.Embed(
			title = ' 오늘기준 ' + SearchID + ' 개통자 남은 유지일수는 ',
			description= '```md\n' + SearchID + result + '```',
			color=0x5ABEFF
			)
		await client.send_message(message.channel, embed=embed)
		
		
		
		
		
		
		
		
 #           
#	if message.content.startswith('!모델명'):
#		SearchID = message.content[len('!모델명')+1:]
#		gc = gspread.authorize(creds)
#		wks = gc.open('오전재고').worksheet('시트2')
#		wks.update_acell('A1', SearchID)
#		result = wks.acell('B1').value
#		
#		embed = discord.Embed(
#			title = ' :printer:  모델명 코드 리스트 ',
#			description= '```' + SearchID + ' 모델명 코드는 ' + result + ' ```',
#			color=0x0000ff
#			)
#		await client.send_message(message.channel, embed=embed)


	if message.content.startswith('!영화순위'):
        # http://ticket2.movie.daum.net/movie/movieranklist.aspx
		i1 = 0 # 랭킹 string값
		embed = discord.Embed(
			title = "영화순위",
			description = "영화순위입니다.",
			colour= discord.Color.red()
			)
		hdr = {'User-Agent': 'Mozilla/5.0'}
		url = 'http://ticket2.movie.daum.net/movie/movieranklist.aspx'
		print(url)
		req = Request(url, headers=hdr)
		html = urllib.request.urlopen(req)
		bsObj = bs4.BeautifulSoup(html, "html.parser")
		moviechartBase = bsObj.find('div', {'class': 'main_detail'})
		moviechart1 = moviechartBase.find('ul', {'class': 'list_boxthumb'})
		moviechart2 = moviechart1.find_all('li')

		for i in range(0, 20):
			i1 = i1+1
			stri1 = str(i1) # i1은 영화랭킹을 나타내는데 사용됩니다
			print()
			print(i)
			print()
			moviechartLi1 = moviechart2[i]  # ------------------------- 1등랭킹 영화---------------------------
			moviechartLi1Div = moviechartLi1.find('div', {'class': 'desc_boxthumb'})  # 영화박스 나타내는 Div
			moviechartLi1MovieName1 = moviechartLi1Div.find('strong', {'class': 'tit_join'})
			moviechartLi1MovieName = moviechartLi1MovieName1.text.strip()  # 영화 제목
			print(moviechartLi1MovieName)

			moviechartLi1Ratting1 = moviechartLi1Div.find('div', {'class': 'raking_grade'})
			moviechartLi1Ratting2 = moviechartLi1Ratting1.find('em', {'class': 'emph_grade'})
			moviechartLi1Ratting = moviechartLi1Ratting2.text.strip()  # 영화 평점
			print(moviechartLi1Ratting)

			moviechartLi1openDay1 = moviechartLi1Div.find('dl', {'class': 'list_state'})
			moviechartLi1openDay2 = moviechartLi1openDay1.find_all('dd')  # 개봉날짜, 예매율 두개포함한 dd임
			moviechartLi1openDay3 = moviechartLi1openDay2[0]
			moviechartLi1Yerating1 = moviechartLi1openDay2[1]
			moviechartLi1openDay = moviechartLi1openDay3.text.strip()  # 개봉날짜
			print(moviechartLi1openDay)
			moviechartLi1Yerating = moviechartLi1Yerating1.text.strip()  # 예매율 ,랭킹변동
			print(moviechartLi1Yerating)  # ------------------------- 1등랭킹 영화---------------------------
			print()
			embed.add_field(name='---------------랭킹'+stri1+'위---------------', value='\n영화제목 : '+moviechartLi1MovieName+'\n영화평점 : '+moviechartLi1Ratting+'점'+'\n개봉날짜 : '+moviechartLi1openDay+'\n예매율,랭킹변동 : '+moviechartLi1Yerating, inline=False) # 영화랭킹


		await client.send_message(message.channel, embed=embed)


	if message.content.startswith('!주사위'):
		randomNum = random.randrange(1, 7) # 1~6까지 랜덤수
		print(randomNum)
		if randomNum == 1:
			await client.send_message(message.channel, embed=discord.Embed(description=':game_die: '+ ':one:'))
		if randomNum == 2:
			await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':two:'))
		if randomNum ==3:
			await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':three:'))
		if randomNum ==4:
			await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':four:'))
		if randomNum ==5:
			await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':five:'))
		if randomNum ==6:
			await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':six: '))
			
			
			
			
	if message.content.startswith("!복권"):
		Text = ""
		number = [1, 2, 3, 4, 5, 6, 7]
		count = 0
		for i in range(0, 7):
			num = random.randrange(1, 46)
			number[i] = num
			if count >= 1:
				for i2 in range(0, i):
					if number[i] == number[i2]:  # 만약 현재랜덤값이 이전숫자들과 값이 같다면
						numberText = number[i]
						print("작동 이전값 : " + str(numberText))
						number[i] = random.randrange(1, 46)
						numberText = number[i]
						print("작동 현재값 : " + str(numberText))
						if number[i] == number[i2]:  # 만약 다시 생성한 랜덤값이 이전숫자들과 또 같다면
							numberText = number[i]
							print("작동 이전값 : " + str(numberText))
							number[i] = random.randrange(1, 46)
							numberText = number[i]
							print("작동 현재값 : " + str(numberText))
							if number[i] == number[i2]:  # 만약 다시 생성한 랜덤값이 이전숫자들과 또 같다면
								numberText = number[i]
								print("작동 이전값 : " + str(numberText))
								number[i] = random.randrange(1, 46)
								numberText = number[i]
								print("작동 현재값 : " + str(numberText))

			count = count + 1
			Text = Text + "  " + str(number[i])
			
		print(Text.strip())
		embed = discord.Embed(
			title="복권 숫자!",
			description=Text.strip(),
			colour=discord.Color.red()
		)
		await client.send_message(message.channel, embed=embed)
		
		
	if message.content.startswith('!사다리'):
		ladder = []
		ladder = message.content[len('!사다리') + 1:].split(" ")
		num_cong = int(ladder[0])
		del (ladder[0])
		if num_cong < len(ladder):
			result_ladder = random.sample(ladder, num_cong)
			result_ladderSTR = ','.join(map(str, result_ladder))
			embed = discord.Embed(
				title="----- 당첨! -----",
				description='```' + result_ladderSTR + '```',
				color=0xff00ff
				)
			await client.send_message(message.channel, embed=embed, tts=False)
		else:
			await client.send_message(message.channel, '```추첨인원이 총 인원과 같거나 많습니다. 재입력 해주세요```', tts=False)

	if message.content.startswith('!타이머'):

		Text = ""
		learn = message.content.split(" ")
		vrsize = len(learn)  # 배열크기
		vrsize = int(vrsize)
		for i in range(1, vrsize):  # 띄어쓰기 한 텍스트들 인식함
			Text = Text + " " + learn[i]
			
		secint = int(Text)
		sec = secint
		
		for i in range(sec, 0, -1):
			print(i)
			await client.send_message(message.channel, embed=discord.Embed(description='타이머 작동중 : '+str(i)+'초'))
			time.sleep(1)

		else:
			print("땡")
			await client.send_message(message.channel, embed=discord.Embed(description='타이머 종료'))

		

		
		

	

		
			
			
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)

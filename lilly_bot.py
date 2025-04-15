from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import discord
import asyncio

# 디스코드 봇 정보 입력하기
DISCORD_TOKEN = ''
CHANNEL_ID = 1361583939663302717  # 디스코드 채널 ID 숫자로 바꾸기

# 최근 글 링크 저장용
latest_link = None

# 셀레니움 브라우저 설정
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

def get_latest_article():
    global latest_link
    url = 'https://cafe.naver.com/trickcal?iframe_url=/ArticleList.nhn?search.clubid=30282220&search.userDisplay=GM릴리'
    driver.get(url)
    time.sleep(2)

    driver.switch_to.frame('cafe_main')
    articles = driver.find_elements('css selector', 'div.article-board.m-tcol-c > table tbody tr')

    for article in articles:
        try:
            link = article.find_element('css selector', 'a.article').get_attribute('href')
            title = article.find_element('css selector', 'a.article').text
            if link != latest_link:  # 최신 글을 찾았을 때만
                latest_link = link
                return title, link
        except:
            continue
    return None, None

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        channel = self.get_channel(CHANNEL_ID)
        while True:
            title, link = get_latest_article()
            if title and link:
                if link != latest_link:  # 중복 전송 방지
                    # "▶바로가기"를 사용해서 링크를 텍스트로 보내기
                    await channel.send(f"📝 @everyone 공지가 올라왔어요! : **{title}**\n[▶바로가기]({link})")
                else:
                    print("새 글 없음")
            await asyncio.sleep(300)  # 5분마다 체크

client = MyClient(intents=discord.Intents.default())
client.run(DISCORD_TOKEN)
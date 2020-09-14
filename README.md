# instagram_bot
Instagram automation with remote contol using Telegram bot

Instagram bot that takes recent posts in a given hashtag, and interacts on those posts.

This bot can follow a given user's followers.

Everything can be controlled using your own telegram bot.


PREREQUISITES - 
1. Python 3
2. Selenium (pip install selenium)
3. Google chrome
4. Chromedriver for your corresponding Chrome version
5. python-telegram-bot (pip install python-telegram-bot)
	
Check chrome version by going to chrome://version/ on your chrome browser.

Download chromedriver.exe for your chrome version from https://chromedriver.chromium.org/

Copy the chromedriver.exe file to the scripts folder. (or change the path for CHROMEDRIVER_PATH in config.py)

Talk to 'https://t.me/BotFather' to create your own bot, copy it's token to 'BOT_ID' in config.py

Type instagram username and password in config.py.

Feel free to add more comments in config.py

USAGE 

After everything is properly configured in config.py simply run bot.py

	cd instagram_bot/scripts/
	
	python bot.py
	
Now you can control your instagram activities from your mobile phone through your telegram bot.

Commands for the telegram bot - 

	/follow <user> <No-of-people-to-follow>
	
		eg - /follow cristiano 10 - This follows the latest 10 followers of the instagram account with username 'cristiano'
		
	/interact <hashtag> <total_posts> <max-likes> <max-comments>
	
	   	eg - /interact likeforlike 10 5 3 - this command will take the latest 10 posts from #likeforlike and like 5 of them and comments on 3 of them.

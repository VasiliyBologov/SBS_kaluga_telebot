
cd C:\TELEBOT\Kaluga_sbs_bot

git init

heroku git:remote -a powerful-scrubland-42210

git add .

git commit -am "make it better"

git push heroku master

heroku ps:scale worker=1
pause

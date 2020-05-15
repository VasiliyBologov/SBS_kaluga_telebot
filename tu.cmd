
git add .

git commit -am "make it better"

git push heroku master

heroku ps:scale worker=1
pause

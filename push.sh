#!/bin/sh

git config --global user.email "victorgau@gmail.com"
git config --global user.name "Victor Gau"
git add docs/*.html
git commit -m "Upload from Travis"
# git remote add origin https://${GH_TOKEN}@github.com/victorgau/MultiStrategies.git > /dev/null 2>&1
# git remote add origin https://github.com/victorgau/MultiStrategies.git
git push --quiet origin master
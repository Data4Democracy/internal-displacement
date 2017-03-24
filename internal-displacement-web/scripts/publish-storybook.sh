#!/bin/bash

# make sure working directory is clean
DIRTY=$(git status | grep modified -c)
let DIRTY+=$(git status | grep Untracked -c)

if [ $DIRTY -gt 0 ] && [ "$1" != "-f" ]; then
  echo "\033[0;31m"Refusing to operate on unclean working directory"\033[0m"
  echo Use \"git status\" to see which files have been modified
  exit 1
fi

# delete gh-pages branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$BRANCH" == "gh-pages" ]; then
  git checkout master
fi
git branch -D gh-pages
git push origin :gh-pages

# build examples
npm run build:storybook

# remove superfluous files
find . -type f | egrep -v ".git/|storybook-build/" | xargs rm
find . -type d -empty -delete
rm -rf node_modules

# move example files to root
mv storybook-build/* ./
rm -rf storybook-build/

# add jekyll config
# echo "include: [__build__]" > _config.yml

# create gh-pages branch
git checkout -b gh-pages
git rm -rf .
git add .
git commit -m "updating gh-pages"
git push -f origin gh-pages
git checkout $BRANCH

# restore node modules
npm install

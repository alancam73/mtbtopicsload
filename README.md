# mtbtopicsload

## Overview
Simple python code to load new MTB articles by topic into a DynamoDB table
This repository is part of the https://www.articles.mtbtopics.com/ overall functionality

## Dependencies
This code can standalone and be re-used & modified for any use-case in updating DynamoDB tables with JSON input files.

However it is part of the functionality of the MTB Topics app which also has the following repositories: -
* https://github.com/alancam73/mtbarticlesapp - Amplify app with Auth & Lambda. UI via Figma
* https://github.com/alancam73/mtbtopicsarticles - Lambda to send new MTB article via AWS SES to active users every 24h

## Versions
This code was tested with python 3.8

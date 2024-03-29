# Loads up the DynamoDB Articles table with new articles from our JSON file

from __future__ import with_statement
import boto3
import json
import os
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import argparse



client=boto3.client('dynamodb')
articles_table = 'mtbTopics-Articles-Topics'


# main lambda function handler
def lambda_handler(event, context):
   
   # allow local Python execution testing as well as Lambda env
   execEnv = str(os.getenv('AWS_EXECUTION_ENV'))
   if execEnv.startswith("AWS_Lambda"):
      articlesFile = str(os.getenv('articlesFile'))
   else:
      parser = argparse.ArgumentParser()
    
      # Adding positional arguments
      parser.add_argument("articlesFile", help = "JSON file with article details")
      args = parser.parse_args()
      articlesFile = args.articlesFile
    
   print ("Articles File: ", articlesFile)
   
   try: 
      with open(articlesFile, 'r') as myfile:
         data=myfile.read()
   except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
       print(articlesFile, " does not exist")
       return
   
   # parse file
   objects = json.loads(data)
   
   response = client.scan(TableName=articles_table,
                          ProjectionExpression='articleId')['Items']
   articleIdList = []
   for i in response:
      articleIdList.append(int(i['articleId']['N']))
                          
   fresh_articles = []
   for obj in objects:
      if obj["articleId"] not in articleIdList:
         fresh_articles.append(obj)
                          
   # print (fresh_articles)
   
   # we create a dynamodb table resource because its easier to put items (no types required)
   # put NEW items in Articles table
   dynamodbtbl=boto3.resource('dynamodb')
   artTblRes = dynamodbtbl.Table(articles_table)
   for obj in fresh_articles:
      articleId = obj["articleId"]
      try:
         artTblRes.put_item(Item=obj)
         print("put_item: articleId=", articleId, " succeeded")
      except ClientError as e:
         print("put_item: articleId=", articleId, " failed")
   
   return None
   


# allow local Python execution testing
if __name__ == '__main__':
    lambda_handler(None,None)

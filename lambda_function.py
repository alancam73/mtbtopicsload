# Loads up the DynamoDB Articles table with new articles from our JSON file

from __future__ import with_statement
import boto3
import json
import os
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import argparse



dynamodbtbl=boto3.resource('dynamodb')
articles_table = dynamodbtbl.Table('mtbTopics-Articles-Topics')

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
   
   for object in objects:
      articleId = object["articleId"]
      try:
         articles_table.put_item(Item=object,
                               ConditionExpression=Attr('articleId').ne(articleId) | Attr('articleId').not_exists()
                              )
         print("put_item: articleId=", articleId, " succeeded")
      except ClientError as e:
         if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
             print("put_item: articleId=", articleId, " failed (or duplicate)")
   
   return None       


# allow local Python execution testing
if __name__ == '__main__':
    lambda_handler(None,None)

import logging

import azure.functions as func
from shared_code import Math
import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function "Add" processed a request.')

    
    num1:float = float(req.params.get('num1'))
    num2:float = float(req.params.get('num2'))
    
    sum=Math.add(num1,num2)
    logging.info(f"Result of addition is {sum}")
    return func.HttpResponse(f"Hello, sum={sum}. This HTTP triggered function executed successfully. Current time ={datetime.datetime.now()} . Version=v2")

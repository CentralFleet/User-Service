import azure.functions as func
from src import *
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ping", methods=['GET','POST'])
async def ping(req: func.HttpRequest) -> func.HttpResponse:
    logger.info(f'Request received from {req.url}')
    return func.HttpResponse("Service is up", status_code=200)


@app.route(route="v1/accounts",methods=['POST'])
async def account_registration(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Request received from {req.url}')

    try:
        response =  await register_account(req=req)

        logger.info(response)

        return func.HttpResponse(json.dumps(response))
  
    except Exception as e:
        logging.error(f'Error processing request: {str(e)}')
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)
    

@app.route(route="v1/carriers",methods=['POST'])
async def carrier_registration(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Request received from {req.url}')

    try:
        response =  await register_carriers(req=req)

        logger.info(response)

        return func.HttpResponse(json.dumps(response))
    
    except Exception as e:
        logging.error(f'Error processing request: {str(e)}')
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)



@app.route(route="v1/contacts",methods=['POST'])
async def contact(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Request received from {req.url}')

    try:
        if req.params.get('action') == 'update':
            resp = await update_contact(req=req)
            return func.HttpResponse(json.dumps(resp), status_code=200)
        
        elif req.params.get('action') == 'create':
            resp = await register_contact(req=req)
            return func.HttpResponse(json.dumps(resp), status_code=200)
        
        else:
            return func.HttpResponse(f"Invalid action: {req.params.get('action')}", status_code=400)
    
    except Exception as e:
        logging.error(f'Error processing request: {str(e)}')
        return func.HttpResponse(f"Internal server error :{str(e)}", status_code=500)

#src/funcmain.py
from utils.helpers import *
from utils.model import *
import azure.functions as func
import os
from pyzohocrm import ZohoApi, TokenManager
from dotenv import load_dotenv
load_dotenv()

logger = get_logger(__name__)


TEMP_DIR = "/tmp"


TOKEN_INSTANCE =  TokenManager(
                                domain_name="Canada",
                                refresh_token=os.getenv("REFRESH_TOKEN"),
                                client_id=os.getenv("CLIENT_ZOHO_ID"),
                                client_secret=os.getenv("CLIENT_ZOHO_SECRET"),
                                grant_type="refresh_token",
                                token_dir=TEMP_DIR
                                )

ZOHO_API = ZohoApi(base_url="https://www.zohoapis.ca/crm/v2")


async def register_account(req : func.HttpRequest):
    """ Register new account """
    try:

        # Get the access token
        token=TOKEN_INSTANCE.get_access_token()

        # Get the json data
        body = req.get_json()
        logging.info(f"received form data: {body}")

        # Create a Company Instance
        company = Company(
            Account_Name=body.get('Account_Name'),
            Dealer_License_Number=body.get('Dealer_License_Number'),
            Category=body.get('Dealership_Type'),
            Address=body.get('Address'),
            ExpiryDate=body.get('ExpiryDate'),
            Business_Number=body.get('Business_Number'),
            CRA_HST_GST_Number=body.get('CRA_HST_GST_Number'),
            SK_PST_Number=body.get('SK_PST_Number'),
            Email=body.get("Email"),
            Dealer_Phone=body.get("Phone"),
            BC_PST_Number=body.get('BC_PST_Number'),
            Website = body.get('Website','')

        )
        payload = {"data":[dict(company)]}

        # Add Company in the CRM
        response = ZOHO_API.create_record(moduleName="Accounts",data=payload,token=token)
        logger.info(response.json())

        if response.status_code == 201:
            ## means account register sucessfully
            customer_id = response.json()["data"][0]["details"]["id"]
            slack_msg = F"""🎉 New User Registration! 🎉 \n *Details* \n - Name: `{body.get('Account_Name')}` \n - Email: `{body.get("Email")}` \n - Type: `Customer` \n - Sign-Up Date: `{datetime.datetime.now()}` \n <https://crm.zohocloud.ca/crm/org110000402423/tab/Accounts/{customer_id}|View Customer Details>"""
            send_message_to_channel(os.getenv("BOT_TOKEN"),os.getenv("USER_CAHNNEL_ID"),slack_msg)
        
            resp = {
                "status":"success",
                "message":"Account created successfully",
                "code":201,
                "CustomerID":customer_id,
            }
        elif response.status_code == 202:
            query = f"Email:equals:{body.get("Email")}"
            search_response = ZOHO_API.search_record(moduleName="Accounts",query=query,token=token)
            logger.info(search_response.json())
            if search_response.status_code == 200 or search_response.status_code == 201:
                data = search_response.json()
                if data["data"]:
                    existing_details = data["data"][0]
                    existing_account_id = existing_details["id"]
            transport_user = existing_details['Central_Fleet_User'] 

            if not transport_user:
                updated_response = ZOHO_API.update_record(moduleName="Accounts",id=existing_account_id,data={"data":[{**dict(company),"Central_Fleet_User":True}]},token=token)
                logger.info(f"Updated User {existing_account_id} with Central Fleet User Response : {updated_response.json()}")
                resp = {
                    "status":"success",
                    "message":"Overwrite Data, User registered as Central Fleet User",
                    "code":200,
                    "CustomerID":existing_account_id
                }
            else:
                resp = {
                    "status":"Duplicate Error",
                    "message":"User already registered",
                    "code":202,
                    "CustomerID":existing_account_id,
                }
        else:
            resp = {
             "status":response.status_code,
             "message":response.text,   
            }
    

        return resp


    except Exception as e:
        logging.error(f"Error adding submitted company in zoho {e}")
        return {
            "status":"Internal Server Error",
            "message":str(e),
            "code":500
        }
    
    


async def register_carriers(req : func.HttpRequest):
    """ Register new Carriers """
    try:
        # Get the access token
        access_token=TOKEN_INSTANCE.get_access_token()

        # Get the json data
        body = req.get_json()
        carrierObj = Vendor(
            Vendor_Name=body.get('CarrierName'),
            Carrier_Type=body.get('CarrierType'),
            OperatingRegions=body.get('OperatingRegions'),
            Phone = body.get("Phone"),
            Email = body.get("Email"),
            Address = body.get('Address'),
            Website = body.get('Website')
        )


        create_response = ZOHO_API.create_record(moduleName="Vendors",data={"data":[dict(carrierObj)]},token=access_token)
        logger.info(create_response.json())


        if create_response.status_code == 201:
            carrier_id = create_response.json()["data"][0]["details"]["id"]

            slack_msg = F"""🎉 New Carrier Registration! 🎉 \n *Details* \n - Carrier: `{body.get('CarrierName')}` \n - Email: `{body.get("Email")}` \n - Type: `Vendor` \n - Sign-Up Date: `{datetime.datetime.now()}` \n <https://crm.zohocloud.ca/crm/org110000402423/tab/Vendors/{carrier_id}|View Carrier Details>"""
            send_message_to_channel(os.getenv("BOT_TOKEN"),os.getenv("USER_CAHNNEL_ID"),slack_msg)
        
            resp = {
                "status":"success",
                "message":"Carrier created successfully",
                "code":201,
                "CarrierID":carrier_id
            }

        elif create_response.status_code == 202:
            search_response = ZOHO_API.search_record(moduleName="Vendors",query=f"Email:equals:{body.get('Email')}",token=access_token)
            if search_response.status_code == 200 or search_response.status_code == 201:
                data = search_response.json()
                if data["data"]:
                    existing_details = data["data"][0]
                    existing_carrier_id = existing_details["id"]
            transport_user = existing_details['Central_Fleet_User']   

            if not transport_user:
                ZOHO_API.update_record(moduleName="Vendors",id=existing_carrier_id,data={"data":[{**dict(carrierObj),"Central_Fleet_User":True}]},token=access_token) 
                logger.info(f"Updated Vendor {existing_carrier_id} with Central Fleet User Response : {create_response.json()}")     
                resp = {
                    "status":"success",
                    "message":"Overwrite Data, User registered as Central Fleet User",
                    "code":200,
                    "CarrierID":existing_carrier_id
                }
            else:
                resp = {
                    "status":"Duplicate Error",
                    "message":"Carrier already registered",
                    "code":202,
                    "CarrierID":existing_carrier_id
                }
        else:
            resp = {
             "status":create_response.status_code,
             "message":create_response.text,   
            }
        return resp

    except Exception as e:
        logging.error(f"Error adding submitted Carrier in zoho {e}")

        return {
            "status":"Internal Server Error",
            "message":str(e),
            "code":500
        }

async def update_contact(req : func.HttpRequest):
    """ Update Contact in Zoho """
    try:
        # Get access token
        access_token=TOKEN_INSTANCE.get_access_token()

        # Get raw data
        body = req.get_json()

        payload = dict(body)
        del payload["ContactID"]
        
        update_contact_response = ZOHO_API.update_record(moduleName="Contacts",id=body.get("ContactID"),data={"data":[payload]},token=access_token)

        if update_contact_response.status_code == 200:
            resp = {
                "status":"success",
                "message":"Contact updated successfully",
                "code":200
            }
        else:
            resp = {
             "status":update_contact_response.status_code,
             "message":update_contact_response.text,   
            }
    
        return resp

    except Exception as e:
        logging.error(f"Error adding submitted contact in zoho {e}")

        return {
            "status":"Internal Server Error",
            "message":str(e),
            "code":500
        }

async def register_contact(req : func.HttpRequest):
    """ Rgister Contact in Zoho """
    try:
        # Get access token
        access_token=TOKEN_INSTANCE.get_access_token()

        # Get form data
        body = req.get_json()
        logging.info(f"received json data: {body}")


        contact = Contact(
            Dealership = None if body.get('Account_ID') == "null" else body.get('Account_ID'),
            Last_Name=body.get('Contact_Name'),
            Email=body.get('Contact_Email'),
            Phone=body.get('Contact_Phone'),
            Title=body.get('Title'),
            Vendor_ID= None if body.get('Carrier_ID') == "null" else body.get('Carrier_ID'),
            
        )

        create_contact_response = ZOHO_API.create_record(moduleName="Contacts",data={"data":[dict(contact)]},token=access_token)

        # Call Add Contact Api
        if create_contact_response.status_code == 201:
                carrier_id = create_contact_response.json()["data"][0]["details"]["id"]

                resp = {
                    "status":"success",
                    "message":"Contact created successfully",
                    "code":201,
                    "ContactID":carrier_id
                }

        elif create_contact_response.status_code == 202:
            resp = {
                "status":"Duplicate Error",
                "message":"Duplicate Contact found",
                "code":202
            }
        else:
            resp = {
            "status":create_contact_response.status_code,
            "message":create_contact_response.text,   
            }
        return resp
    
    except Exception as e:
        logging.error(f"Error adding submitted contact in zoho {e}")
        return {
            "status":"Internal Server Error",
            "message":str(e),
            "code":500
        }

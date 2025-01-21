# User-Service
User-Service is an API designed to facilitate the integration between a business application and Zoho CRM. This service provides multiple endpoints for managing accounts, carriers, and contacts in Zoho CRM, as well as sending notifications via Slack.


## Environment Variables

The following environment variables are required for the integration:

- `REFRESH_TOKEN`: OAuth refresh token for Zoho CRM
- `CLIENT_ZOHO_ID`: Zoho CRM client ID
- `CLIENT_ZOHO_SECRET`: Zoho CRM client secret
- `BOT_TOKEN`: Slack bot token for sending notifications
- `USER_CHANNEL_ID`: Slack user channel ID for notifications

Create a `.env` file in the project root directory and include the following:

```env
REFRESH_TOKEN=your_refresh_token
CLIENT_ZOHO_ID=your_client_id
CLIENT_ZOHO_SECRET=your_client_secret
BOT_TOKEN=your_slack_bot_token
USER_CHANNEL_ID=your_slack_user_channel_id
```

## Endpoints
#### `GET /ping`
**Description**: A health check endpoint to verify the service is up and running.  
**Response**:  
```json
{
  "message": "Service is up"
}
```

#### `POST /v1/accounts`
**Description**: This endpoint is used to register a new account in Zoho CRM.
**Response**:  
```json
{
    "Account_Name": "Example Account",
    "Dealer_License_Number": "12345",
    "Dealership_Type": "Car Dealership",
    "Address": "1234 Example St, Toronto, ON",
    "ExpiryDate": "2025-01-01",
    "Business_Number": "123456789",
    "CRA_HST_GST_Number": "GST12345",
    "SK_PST_Number": "PST12345"
}

```

#### `POST /v1/carriers`
**Description**: This endpoint registers a new carrier in Zoho CRM.
**Response**:
```json
{
    "Carrier_Name": "Example Carrier",
    "Carrier_ID": "54321",
    "Address": "5678 Carrier Rd, Toronto, ON",
    "Contact": "John Doe",
    "Phone": "123-456-7890",
    "Email": "contact@carrier.com"
}

```

#### `POST /v1/contacts?action=create`
**Description**: This endpoint registers a new contact in Zoho CRM.
**Response**:
```json
{
    "Account_ID": "12345",
    "Carrier_ID": "54321",
    "Contact_Name": "John Doe",
    "Contact_Phone": "123-456-7890",
    "Contact_Email": "contact@carrier.com"
}
```

#### `POST /v1/contacts?action=update`
**Description**: This endpoint updates an existing contact in Zoho CRM.
**Response**:
```json
{
    "Contact_ID": "12345",
    "Contact_Name": "New John Doe",
    "Contact_Phone": "123-456-7890",

}
```
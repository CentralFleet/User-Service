import pytest
from unittest.mock import patch, MagicMock
from src.main import register_account, register_carriers, register_contact, update_contact
import azure.functions as func
import json

@pytest.fixture
def mock_request():
    def _mock_request(body):
        req = MagicMock(spec=func.HttpRequest)
        req.get_json.return_value = body
        return req
    return _mock_request

@pytest.mark.asyncio
@patch("src.main.TOKEN_INSTANCE.get_access_token")
@patch("src.main.ZOHO_API.create_record")
async def test_register_account(mock_zoho, mock_token, mock_request):
    mock_token.return_value = "fake_token"
    mock_zoho.return_value.status_code = 201
    mock_zoho.return_value.json.return_value = {"data": [{"details": {"id": "12345"}}]}
    req = mock_request({
        "Account_Name": "Test Account",
        "Dealer_License_Number": "DL12345",
        "Dealership_Type": "Independent",
        "Address": "123 Test St",
        "Email": "test@example.com",
        "Phone": "123-456-7890"
    })
    response = await register_account(req)
    assert response["status"] == "success"
    assert response["CustomerID"] == "12345"

@pytest.mark.asyncio
@patch("src.main.TOKEN_INSTANCE.get_access_token")
@patch("src.main.ZOHO_API.create_record")
async def test_register_carriers(mock_zoho, mock_token, mock_request):
    mock_token.return_value = "fake_token"
    mock_zoho.return_value.status_code = 201
    mock_zoho.return_value.json.return_value = {"data": [{"details": {"id": "67890"}}]}
    req = mock_request({
        "CarrierName": "Test Carrier",
        "CarrierType": ["Freight"],
        "OperatingRegions": "North America",
        "Email": "carrier@example.com",
        "Phone": "987-654-3210"
    })
    response = await register_carriers(req)
    assert response["status"] == "success"
    assert response["CarrierID"] == "67890"

@pytest.mark.asyncio
@patch("src.main.TOKEN_INSTANCE.get_access_token")
@patch("src.main.ZOHO_API.update_record")
async def test_update_contact(mock_zoho, mock_token, mock_request):
    mock_token.return_value = "fake_token"
    mock_zoho.return_value.status_code = 200
    req = mock_request({
        "ContactID": "54321",
        "Title": "Manager",
        "Phone": "111-222-3333"
    })
    response = await update_contact(req)
    assert response["status"] == "success"
    
@pytest.mark.asyncio
@patch("src.main.TOKEN_INSTANCE.get_access_token")
@patch("src.main.ZOHO_API.create_record")
async def test_register_contact(mock_zoho, mock_token, mock_request):
    mock_token.return_value = "fake_token"
    mock_zoho.return_value.status_code = 201
    mock_zoho.return_value.json.return_value = {"data": [{"details": {"id": "98765"}}]}
    req = mock_request({
        "Contact_Name": "John Doe",
        "Contact_Email": "johndoe@example.com",
        "Contact_Phone": "555-555-5555",
        "Title": "Sales Rep"
    })
    response = await register_contact(req)
    assert response["status"] == "success"
    assert response["ContactID"] == "98765"

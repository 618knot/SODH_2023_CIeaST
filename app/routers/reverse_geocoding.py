"""
リバースジオコーディング
"""
import pprint
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from .util.sqlite_util import *
import requests

load_dotenv(verbose=True)
DOTENV_PATH: str = join(dirname(__file__), '.env')
load_dotenv(DOTENV_PATH)

GCP_API_KEY: str = os.environ.get("GCP_API_KEY")

RESOURCE_NAME: str = "reverse_geocoding"

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class LatLanProps(BaseModel):
    lat: float
    lng: float

@router.post("/")
async def reverse_geocoding(props: LatLanProps):
    headers = {
        "Accept-Language": "ja"
    }
    result = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?latlng={props.lat},{props.lng}&key={GCP_API_KEY}", headers=headers)
    address = result.json()["results"][0]["formatted_address"]

    return address
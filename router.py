import os

from fastapi import Request, Response, APIRouter
import httpx
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

TARGET_BACKEND_URL = "https://akademia-profi.bitrix24.ru/rest/"
client = httpx.AsyncClient(base_url=TARGET_BACKEND_URL)
courses_webhook = {
    "id": 38,
    "token": os.environ.get("COURSE_TOKEN")
}
lead_webhook = {
    "id": 38,
    "token": os.environ.get("LEAD_TOKEN")
}

router = APIRouter(
    prefix="/api",
    tags=["Курсы"],
)


class CourseBody(BaseModel):
    category_id: int
    name: str
    count: int


@router.post("/get-courses")
async def get_courses(request: Request, course: CourseBody):

    url = httpx.URL(path=f"{courses_webhook["id"]}/{courses_webhook["token"]}/crm.product.list.json", query=request.url.query.encode("utf-8"))

    body = {
        "filter": {
            "%NAME": f"{course.name}",
            "PROPERTY_106": f"{course.category_id}"
        },
        "select": [
            "ID",
            "NAME",
            "ACTIVE",
            "PRICE",
            "SORT",
            "PROPERTY_112"

        ],
        "order": {
            "ID": "ASC"
        },
        "start": f"{course.count*50}"
    }

    try:
        rp = await client.request(
            method=request.method,
            url=url,
            json=body,
            timeout=30.0
        )

        response_headers = dict(rp.headers)

        response_headers.pop("content-encoding", None)
        response_headers.pop("transfer-encoding", None)

        return Response(
            content=rp.content,
            status_code=rp.status_code,
            headers=response_headers,
            media_type=rp.headers.get("content-type")
        )

    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        return Response(f"Proxy error: Could not reach upstream server.", status_code=500)
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        return Response(f"Proxy error: An unexpected error occurred.", status_code=500)


class Lead(BaseModel):
    name: str
    lastname: str
    secondname: str
    phone: str
    email: str
    course: str
    cost: int


@router.post("/add-lead")
async def add_lead(request: Request, lead: Lead):

    url = httpx.URL(path=f"{lead_webhook["id"]}/{lead_webhook["token"]}/crm.lead.add.json", query=request.url.query.encode("utf-8"))

    body = {
        "fields": {
            "TITLE": "Новая заявка с сайта Akademia Profi",
            "NAME": f"{lead.name}",
            "SECOND_NAME": f"{lead.secondname}",
            "LAST_NAME": f"{lead.lastname}",
            "STATUS_ID": "NEW",
            "SOURCE_ID": "BOOKING",
            "COMMENTS": f"{lead.course}",
            "OPENED": "Y",
            "ASSIGNED_BY_ID": 1,
            "CURRENCY_ID": "RUB",
            "OPPORTUNITY": f"{lead.cost}",
            "PHONE": [
                {
                    "VALUE": f"{lead.phone}",
                    "VALUE_TYPE": "WORK"
                }
            ],
            "EMAIL": [
                {
                    "VALUE": f"{lead.email}",
                    "VALUE_TYPE": "WORK"
                }
            ],
        },
        "params": {
            "REGISTER_SONET_EVENT": "Y"
        }
    }

    try:

        rp = await client.request(
            method=request.method,
            url=url,
            json=body,
            timeout=30.0
        )

        response_headers = dict(rp.headers)

        response_headers.pop("content-encoding", None)
        response_headers.pop("transfer-encoding", None)

        return Response(
            content=rp.content,
            status_code=rp.status_code,
            headers=response_headers,
            media_type=rp.headers.get("content-type")
        )

    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        return Response(f"Proxy error: Could not reach upstream server.", status_code=500)
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        return Response(f"Proxy error: An unexpected error occurred.", status_code=500)

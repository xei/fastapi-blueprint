from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/")
async def get_home_page():
    html_content = """
    <html>
        <head>
            <title>Blueprint Service</title>
        </head>
        <body>
            <h1>Blueprint Service</h1>
            Check the service health status <a href="/healthz">here</a>
            <br>
            Check out the documentation <a href="/docs">here</a>
            <br>
            Developed by DataScience team
            <br>
            Be in touch with hamidreza@hosseinkhani.me in case of any problem.
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
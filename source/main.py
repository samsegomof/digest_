from fastapi import FastAPI

from source.api.veiws import router

app = FastAPI()

app.include_router(router)

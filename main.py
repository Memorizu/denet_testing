from fastapi import FastAPI
import uvicorn

from source.api.views import router


app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080, reload=True)

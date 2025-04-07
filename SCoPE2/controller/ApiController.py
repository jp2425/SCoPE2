import uvicorn
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi import FastAPI
import json

from fastapi.middleware.cors import CORSMiddleware

from controller.ProcessCodeController import ProcessCodeController

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Defina aqui a origem que deseja permitir, ou use "*" para permitir qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Defina os métodos que deseja permitir (por exemplo, ["GET", "POST"])
    allow_headers=["*"],  # Defina os cabeçalhos que deseja permitir
)

@app.post("/process/")
async def process(request: Request):

        data = json.loads(await request.body())
        print("###################")

        print("Request:", data)
        print("###################")
        controller = ProcessCodeController()
        out = controller.processCode(data)
        return JSONResponse(content=json.dumps({"result":out}))


def main():


    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
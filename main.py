import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
file_path = os.environ.get("SAVE_FILE_PATH")

from fastapi import FastAPI, File, Depends, UploadFile
from fastapi.exceptions import HTTPException
from starlette.responses import FileResponse

from sqlalchemy.orm import Session

from sql_app import crud, models
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/file/")
async def upload_file(uploaded_file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and save file data to DB.

    :param uploaded_file: file
    :param db:
    :return: file data
    """
    file = await (uploaded_file.read())
    file_location = f"{file_path}/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file)
    file_data = {"name": uploaded_file.filename, "size": len(file)}
    return crud.create_file(db=db, file=file_data)


@app.get("/file/{file_id}")
def get_file(file_id: int, db: Session = Depends(get_db)):
    """
    Get file data by ID

    :param file_id: int
    :param db:
    :return: dict
    """
    return crud.get_file(db=db, file_id=file_id)


@app.get("/file/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    """
    Download file by ID

    :param file_id: int
    :param db:
    :return: file
    """

    try:
        file = crud.get_file(db=db, file_id=file_id)
        file_location = f"{file_path}/{file.name}"
        return FileResponse(file_location, media_type='application/octet-stream', filename=file.name)
    except Exception as e:
        raise HTTPException(404, detail="file not found")


@app.get("/files/all/")
def list_files(db: Session = Depends(get_db)):
    """
    Return list of all files

    :param db:
    :return: list of dict
    """
    return crud.get_all_files(db=db)


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

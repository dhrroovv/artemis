from fastapi import APIRouter

router = APIRouter(tags=["Auth"])  # prefix is already set to "/auth" in root router


@router.get("/")
def hello_world():
    return "hello world"

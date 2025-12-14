from pydantic import BaseModel, HttpUrl

class RepoAnalyzeRequest(BaseModel):
    repo_url: HttpUrl

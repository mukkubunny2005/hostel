from pydantic import BaseModel, Field

# class UserCreate(BaseModel):
# 	username: str = Field(..., min_length=3, max_length=50)
# 	email: EmailStr = Field(...,)
# 	first_name: Optional[str] = Field(None, max_length=200)
# 	last_name: Optional[str] = Field(None, max_length=200)
# 	password: str = Field(..., min_length=6)
# 	ph_no: Optional[str] = Field(None, max_length=50)

# 	class Config:
# 		anystr_strip_whitespace = True
# 		extra = "forbid"
# 		orm_mode = True

class Token(BaseModel):
	access_token: str = Field(..., )
	token_type: str = Field(...,)
	username: str = Field(...,)
	user_id: str = Field(...,)
	class Config:
		anystr_strip_whitespace = True
		extra = "forbid"
		orm_mode = True

class UserVerification(BaseModel):
	old_password: str = Field(..., min_length=6)
	new_password: str = Field(..., min_length=6)
	class Config:
		anystr_strip_whitespace = True
		extra = "forbid"
		orm_mode = True


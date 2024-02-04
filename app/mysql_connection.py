from sqlalchemy  import create_engine  
from urllib.parse import quote_plus



username = "admin"
password = "root1234"
endpoint = "mytesting-dbinstance.clescgcoec5z.ap-south-1.rds.amazonaws.com:3306"
db_name = "MyFirstTestDatabase"

engine_connect = create_engine(f"mysql+pymysql://{username}:{quote_plus(password)}@{endpoint}/{db_name}") 


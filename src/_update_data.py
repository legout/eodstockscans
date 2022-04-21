from findata.update_db import run
from datetime import datetime

run(region="na", year=str(datetime.now().year), forexpros=True)
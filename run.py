# from app import app
# app.run(debug=True)

# Cloud9 app run
import os
from app import app
app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), 
        debug=True)


---


# Advanced Middleware for FastAPI

This project demonstrates a custom middleware for FastAPI, which includes:

- **Rate-limiting**: Blocks multiple requests from the same IP within a 5-second window.
- **Request Logging**: Logs incoming requests and their processing times.
- **Custom Headers**: Adds `X-Process-Time` to the response to indicate how long the request took to process.

## Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn (for running the server)

Install the required libraries:

```bash
pip install fastapi uvicorn
```


## Step-by-Step Implementation

1. **Project Structure**

   Create the following project structure:

   ```
   /your_project
   │
   ├── main.py
   ├── middleware.py
   ├── README.md
   ```

2. **Create the Middleware (`middleware.py`)**

   Copy the following code into the `middleware.py` file:

   ```python
   from collections import defaultdict
   import time
   from typing import Dict
   from fastapi import Request, status
   from starlette.middleware.base import BaseHTTPMiddleware
   from starlette.responses import Response

   class AdvancedMiddleware(BaseHTTPMiddleware):
       def __init__(self, app):
           super().__init__(app)
           self.rate_limit_records: Dict[str, float] = defaultdict(float)

       async def log_message(self, message: str):
           print(message)

       async def dispatch(self, request: Request, call_next):
           client_ip = request.client.host
           current_time = time.time()

           if current_time - self.rate_limit_records[client_ip] < 5:
               return Response(
                   content="Rate Limit exceeded.",
                   status_code=status.HTTP_429_TOO_MANY_REQUESTS,
               )

           self.rate_limit_records[client_ip] = current_time

           path = request.url.path
           await self.log_message(f"Request to {path}")

           start_time = time.time()
           response = await call_next(request)
           process_time = time.time() - start_time

           response.headers.append("X-Process-Time", str(process_time))
           await self.log_message(f"Response for {path} took {process_time} second")

           return response
   ```

3. **Create the FastAPI App (`main.py`)**

   In the `main.py` file, create a simple FastAPI app and apply the middleware:

   ```python
   from fastapi import FastAPI
   from middleware import AdvancedMiddleware

   app = FastAPI()

   # Add the middleware
   app.add_middleware(AdvancedMiddleware)

   @app.get("/")
   async def root():
       return {"message": "Welcome to the FastAPI app!"}
   ```

4. **Run the FastAPI App**

   Use Uvicorn to run the server:

   ```bash
   uvicorn main:app --reload
   ```

   The `--reload` flag enables hot-reloading, so the server restarts automatically on code changes.

5. **Test the Middleware**

   - Open your browser or use tools like **Postman** to access `http://127.0.0.1:8000/`.
   - Try making multiple requests within 5 seconds from the same IP to see the **rate-limit** message.
   - Check the logs in the console to view the **request logs and processing times**.

6. **Expected Output**

   - If you make multiple requests within 5 seconds, you'll see:

     ```json
     {
       "detail": "Rate Limit exceeded."
     }
     ```

   - On normal requests, the response will include the `X-Process-Time` header:

     ```json
     {
       "message": "Welcome to the FastAPI app!"
     }
     ```

     **Headers:**
     ```
     X-Process-Time: 0.0012454986572265625
     ```

---

## Conclusion

This middleware provides basic rate-limiting, request logging, and custom headers for your FastAPI app. You can further enhance it by:
- Adding IP whitelisting.
- Customizing the rate-limit duration.
- Storing logs in a file or external logging service.

Enjoy building with FastAPI!
```

---


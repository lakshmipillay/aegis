FROM python:3.11
WORKDIR /app
ARG GEMINI_API_KEY
ENV GEMINI_API_KEY=${GEMINI_API_KEY}
ARG GEMINI_MODEL_NAME="gemini-3-flash-preview"
ENV GEMINI_MODEL_NAME=${GEMINI_MODEL_NAME}
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8080"]
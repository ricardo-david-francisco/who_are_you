FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir gradio wordcloud transformers
EXPOSE 7860
CMD ["python", "webapp.py"]

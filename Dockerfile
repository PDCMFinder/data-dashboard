FROM python:3.9.6
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt && pip install git+https://github.com/hshhrr/plotly-upset.git
EXPOSE 8050/tcp
ENV NAME World
CMD ["python", "main.py"]

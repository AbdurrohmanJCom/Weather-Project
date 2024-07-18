FROM python:3.11

# Set the working directory
WORKDIR /weather_project


COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh


# Install dependencies
COPY requirements.txt /weather_project/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /weather_project/

# Expose the port
EXPOSE 8000

# Command to run the server
CMD ["./wait-for-it.sh", "db:5432", "--", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

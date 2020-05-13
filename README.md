## FACE DETECTION API

This is an API made in Django, to integrate face detection app built with opencv.

Send a post request to this endpoint https://apidetect.herokuapp.com/attendance/detect/ along with raw image or url to the image to get response.

## Steps for installation.

- Create a virtual environment using following command.
    for linux and mac -

    ```python
    python3 -m venv env
    ```

    or in windows

    ```python
    py -m venv env
    ```

- Install all the required packages.

    ```python
    pip install -r requirements.txt
    ```

- Run the Django Test Server.

    ```python
    python manage.py runserver
    ```

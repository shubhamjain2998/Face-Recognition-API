## FACE DETECTION API

This is an API made in Django, to integrate face detection app built with opencv.

Send a post request to this endpoint https://apidetect.herokuapp.com/attendance/detect/ along with raw image or url to the image to get response.

## Steps for installation.

- Create a virtual environment using following command.
    for linux and mac -

    ```console
    python3 -m venv env
    ```

    or in windows

    ```console
    py -m venv env
    ```
- Activate the virtual environment.

    ```console
    source venv/bin/activate
    ```
    
- Install all the required packages.

    ```console
    pip install -r requirements.txt
    ```

- Run the Django Test Server.

    ```console
    python manage.py runserver
    ```

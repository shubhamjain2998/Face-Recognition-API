## FACE DETECTION API

This is an API made in Django, to integrate face detection app built with opencv.

Send a post request to this endpoint https://apidetect.herokuapp.com/attendance/detect/ along with raw image or url to the image to get response.

## Developed By - 
- [Shubham Jain](https://github.com/shubhamjain2998)
- [Jatin Sahu](https://github.com/JatinSahu0506)

## Steps for installation.

1. Create a virtual environment using following command.
    for linux and mac -

    ```console
    python3 -m venv env
    ```

    or in windows

    ```console
    py -m venv env
    ```
2. Activate the virtual environment.

    ```console
    source venv/bin/activate
    ```
    
3. Install all the required packages.

    ```console
    pip install -r requirements.txt
    ```

4. Run the Django Test Server.

    ```console
    python manage.py runserver
    ```

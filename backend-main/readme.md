<div align="center">
    <h1>SAM Backend Software</h1>
    <h3>Used stacks :</h3>
        ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
    ![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    ![flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
    ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
    ![Stripe](https://img.shields.io/badge/Stripe-626CD9?style=for-the-badge&logo=Stripe&logoColor=white)
    ![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
    ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
    <h3>Possible databases :</h3>
    ![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
    ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
    ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
    ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
</div>

## QuickStart

How to quickly run the app on your laptop ? 

There are two way to run the app, with Docker or Python.

For all of the following QuickStart you need to have a `.env` file in your app root folder. (see [environement variables](#env) section)

| ⚠️ WARNING: Without environement variables the app will not work |
| --- |

During your first deployment it's PRIMORDIAL to perform following cmd from a working environment on the prod database to init the first deployment.

```bash
flask db upgrade
```

If you use stripe related endpoint remind you to use [Stripe CLI](https://stripe.com/docs/stripe-cli?locale=en-EN) forwarder : 

```bash
stripe listen --forward-to 127.0.0.1:5000/api/v1/webhook
```

### Docker QuickStart

On a local environement you can use the `docker-compose.test.yml` file whith : 

```shell
docker-compose -f docker-compose.test.yml up
```

### Python

Install python dependencies with

```shell
pip install -r requirements.txt
python -m nltk.downloader punkt
```

Then you can run the app with :

```
flask run
```

With VScode you can just use the native python debugger.

## <a name="env"></a> Environement variables

This section describes the required environment variables for the application to function properly. You should set these variables according to your specific setup.

- `TEST_MODE`: Set this variable to enable test mode for the application, it bypass SMPT vars (deactivate mails).
- `CORS_ORIGINS`: The allowed origins for Cross-Origin Resource Sharing (CORS). Use `*` to allow all origins.
- `DATABASE_URI`: The connection URI for the application database (exemples : sqlite:////absolute_path.sqlite, postgresql://postgres:postgres@database:5432/database_name ).
- `DEFAULT_CREDIT`: The default credit amount for new users.

    #### Email conf (not required if test_mode)

    - `SMTP_HOST`: The hostname of the SMTP server for sending emails.
    - `SMTP_PORT`: The port number for the SMTP server.
    - `SMTP_USER`: The username or email address to authenticate with the SMTP server.
    - `SMTP_PASSWORD`: The password for authenticating with the SMTP server.
    - `DISABLE_EMAIL_TLS`: Set this variable to disable TLS encryption for email communication.
    - `EMAIL_TEST`: Set this variable to enable email testing mode (The mails will not be sended).

    #### Stripe conf

    - `STRIPE_API_KEY`: The API key for accessing the Stripe payment gateway.
    - `STRIPE_SECRET_KEY`: The secret key for validating Stripe webhooks.

    #### Security

    - `SECRET_KEY` : the key used for token signature.
    - `FRENET_KEY`: The frenet key used to encrypt the users files.

    #### Redirections

    - `FRONTEND_URL`: The URL of the frontend application.
    - `BACKEND_URL`: The URL of the backend application.
    - `SUCCESS_URL`: The URL to redirect to after a successful payment.
    - `CANCEL_URL`: The URL to redirect to after a canceled payment.

    #### Documentation
    - `SWAGGER`: Set this variable to enable the Swagger documentation UI.

## How to contribute

The app ad been thinked for modularity and easy improvment. Then, the AI part is indepent from the **web** part : find everything in `app/ai/` .

> Note : the trained models are under `app/ai/model/` folder and this path name must not be changed.

## How to integrate in frontend

You can find everything you need in the app/openapi.yml file. Or at http://backend_url/swagger (only if activated)

## How to add new product in stripe

Remember : All non archived Stripe product will be avaibles.

It's ‼️ PRIMORDIAL ‼️ to add the following metadata to stripe product : 
- `subscription_credit` for recurent credit = number of credited credit
- `credit` = number of credit to add to account (one time payments)

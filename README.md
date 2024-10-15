SOCIAL_ANIMO

- Requirement : Python 3

- Change your email settings in settings.py
    - EMAIL_HOST_USER = 'add_your_gmail@gmail.com'
    - EMAIL_HOST_PASSWORD = 'add_your_password'

- create python 3 environment and install requirements.txt
    - pip install -r requirements.txt

- run local server
    - python manage.py runserver

- For regestration 
    - /accounts/signup/

- For login
    - /accounts/login/ or use swagger

- For logout
    - /accounts/logout/ or use swagger


- API structure followes : <app_name>/api/<url_end_point>


Create a social media backend using Django and DRF. Following are the use cases to consider
1. User should register and verify their email.
    - For regestration used default django auth urls
    - For email confirmation check(authentication not required for this) - /users/api/email-verification/ inside users app as EmailVerification
        - Required body for send a mail with unique OTP
            {
                "email": "abc@gmail.com"
            }
        - Required body for verify email with given otp
            {
                "email":"abc@gmail.com",
                "otp":"15NJ51"
            }

2. User should be able to find and add their friends - 
    - For find and search check API : /friends/api/search-friends/?q=<string>
    - For add friends check : /friends/api/add-friends/ (for add friend, profile should be created in Profile(prfl_profile) table)
        - Required body for add any other profile as friend
            {
                "profile_id":<pk_of_profile>
            }

3. User should be able to update status and upload photos
    - API to add status - /content/api/status-add-update/ (POST method), API to updated status call PUT method
        - Required body for add status
            {
                "status" :<char>,
            }

        - Required body for update status
            {
                "status" :<char>,
                "status_id" : <pk>,
            }

    - API to add photos - /content/api/pic-add-update/ (POST method), API to updated photo call PUT method
        - Required body for add picture
            {
                "picture" :<file obj>,
                "is_current_profile_status":<send true if user want to set as profile picture else send false>
            }

        - Required body for update picture
            {
                "picture" :<char>,
                "picture_id" : <pk>,
            }

4. User should be able to like and comment on pictures
    - Save method of comment(cntnt_comments) and like(cntnt_likes) model overriden for calculate number of likes and comments.
    - API to add comments on picture/status/comments : /content/api/add-comment/
        - required body for add comments for picture : 
            {
                "picture" : <picture id>,
                "comment" : <text field>
            }
        - required body for add comments for status
            {
                "status" : <status id>,
                "comment" : <text field>
            }
        - required body for add comments for other comments
            {
                "parent_comment" : <comment id>,
                "comment" : <text field>
            }

5. User should be able to update profile picture
    - API to add/update profile picture : /content/api/pic-add-update/
        - Required body for add profile picture
            {
                "picture" :<file obj>,
                "is_current_profile_status": "true"
            }

Tech requirements for above assignment:
1. API authentication and Authorization using OAuth
    - Used default django's allauth views for regestration/login/logout also we can use swagger
    - added authetication class in required apis

2. Create models and serializers for request validation
    - Each app having respected models and serializers.

3. use of middlewares for exception handling

4. appropriate use of loggers
    - Check settings.py, Added django default logger for each app, log will be available in project_root/app_logs/

5. Use of cache to speed up the system
    - Used database caching
    - Created social_animo_caching cache table - check in settings.py
    - Added for /friends/api/search-friends/ : In friends app as SearchFriends view
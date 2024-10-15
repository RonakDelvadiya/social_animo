# SOCIAL_ANIMO

## Requirements
- Python 3

## Setup

1. **Change Email Settings in `settings.py`:**
   - `EMAIL_HOST_USER = 'add_your_gmail@gmail.com'`
   - `EMAIL_HOST_PASSWORD = 'add_your_password'`

2. **Create Python 3 environment and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Local Server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication Endpoints:
- **Registration:** `/accounts/signup/`
- **Login:** `/accounts/login/` (or use Swagger)
- **Logout:** `/accounts/logout/` (or use Swagger)

### API Structure:
- `<app_name>/api/<url_end_point>`

## Use Cases

1. **User Registration & Email Verification:**
   - Registration uses Django's default auth URLs.
   - Email verification API: `/users/api/email-verification/` (inside `users` app as `EmailVerification`).
     - **Request body to send email with unique OTP:**
       ```json
       {
         "email": "abc@gmail.com"
       }
       ```
     - **Request body to verify email with OTP:**
       ```json
       {
         "email": "abc@gmail.com",
         "otp": "15NJ51"
       }
       ```

2. **Find and Add Friends:**
   - Search for friends: `/friends/api/search-friends/?q=<string>`
   - Add friends: `/friends/api/add-friends/`
     - **Required body to add a friend:**
       ```json
       {
         "profile_id": <pk_of_profile>
       }
       ```

3. **Update Status and Upload Photos:**
   - Add/update status: `/content/api/status-add-update/`
     - **POST request to add status:**
       ```json
       {
         "status": <char>
       }
       ```
     - **PUT request to update status:**
       ```json
       {
         "status": <char>,
         "status_id": <pk>
       }
       ```
   - Add/update photos: `/content/api/pic-add-update/`
     - **POST request to add picture:**
       ```json
       {
         "picture": <file obj>,
         "is_current_profile_status": <true/false>
       }
       ```
     - **PUT request to update picture:**
       ```json
       {
         "picture": <char>,
         "picture_id": <pk>
       }
       ```

4. **Like and Comment on Pictures:**
   - Model methods for comments (`cntnt_comments`) and likes (`cntnt_likes`) are overridden to track counts.
   - Add comment on picture/status/comment: `/content/api/add-comment/`
     - **Request body for picture comment:**
       ```json
       {
         "picture": <picture id>,
         "comment": <text field>
       }
       ```
     - **Request body for status comment:**
       ```json
       {
         "status": <status id>,
         "comment": <text field>
       }
       ```
     - **Request body for comment on another comment:**
       ```json
       {
         "parent_comment": <comment id>,
         "comment": <text field>
       }
       ```

5. **Update Profile Picture:**
   - Add/update profile picture: `/content/api/pic-add-update/`
     - **Required body to add profile picture:**
       ```json
       {
         "picture": <file obj>,
         "is_current_profile_status": "true"
       }
       ```

## Tech Requirements

1. **API Authentication & Authorization using OAuth:**
   - Uses Django's allauth views for registration/login/logout.
   - Authentication classes added for required APIs.

2. **Models and Serializers for Request Validation:**
   - Each app contains respective models and serializers.

3. **Use of Middlewares for Exception Handling.**

4. **Appropriate Use of Loggers:**
   - Django's default logger configured in `settings.py`.
   - Logs are stored in `project_root/app_logs/`.

5. **Use of Cache to Optimize Performance:**
   - Database caching is used.
   - `social_animo_caching` cache table created (configured in `settings.py`).
   - Caching added to `/friends/api/search-friends/` in the `SearchFriends` view inside the `friends` app.

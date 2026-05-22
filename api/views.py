from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class GoogleOAuth2CallbackView(APIView):
    def post(self, request):
        code = request.data.get('code')

        if not code:
            return Response({'error': 'Authorization code not provided'}, status=status.HTTP_400_BAD_REQUEST)

        token_url = settings.GOOGLE_TOKEN_URL
        payload = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_OAUTH2_REDIRECT_URI, # This must match the one used to get the code
            'grant_type': 'authorization_code',
        }

        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            token_data = response.json()

            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token') # May be None if not requested or already granted
            expires_in = token_data.get('expires_in')
            # id_token = token_data.get('id_token') # Contains user info

            # For now, just return the tokens.
            # In a real app, you'd typically:
            # 1. Verify the id_token.
            # 2. Get user info from Google using the access_token.
            # 3. Create or update a local user record.
            # 4. Store the access_token and refresh_token securely, associated with the user.
            # 5. Generate a session or a JWT for your application.

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_in': expires_in,
                # 'id_token': id_token, # Optionally return for client-side decoding
                'message': 'Tokens obtained successfully.'
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            error_response = e.response.json() if e.response else {}
            error_description = error_response.get('error_description', str(e))
            return Response({
                'error': 'Failed to exchange authorization code for tokens.',
                'details': error_description
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


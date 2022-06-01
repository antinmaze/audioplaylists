from curses.ascii import NUL
from termios import TIOCPKT_DOSTOP
from urllib import request
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session, TokenUpdated
#from oauthlib.oauth2 import TokenExpiredError
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, InvalidClientError
#from django.urls import include, path
from django.core.exceptions import PermissionDenied, SuspiciousOperation
import logging
from django.shortcuts import redirect
from django.conf import settings

"""
Vous pouvez supprimer cet accès à tout moment à l'adresse spotify.com/account.
Pour plus d'informations sur l'utilisation de vos données personnelles par Diwido Audio, consultez la Politique de confidentialité de Diwido Audio.
"""

#https://accounts.spotify.com/authorize?response_type=code&
# client_id=e95695969638fshqcb678e35d65a2646&
# redirect_uri=https%3A%2F%2Faudio-playlist.com%2Fcallback&
# scope=user-read-email+playlist-read-collaborative+playlist-read-private&
# state=JAdUUHnmBX3MSBFPVEDbitvBfu9YQT
def authorizationRequest(_request, _client_id, _scope, _redirect_uri, _authorization_base_url):
    """Step 1: User Authorization.
    Forge the Authorization request and Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    #response_type implicitly set to 'code' in OAuth2Session
    oauth_session = OAuth2Session(_client_id, scope=_scope, redirect_uri=_redirect_uri)
    authorization_url, _state= oauth_session.authorization_url(_authorization_base_url, show_dialog='false')

    # Store Session using an ID store in a Cookie
    # State is stored in session DB to prevent CSRF, keep this for later.
    saveSession(_request, state=_state, client_id=_client_id)
    return authorization_url


#https://audio.diwido.com/callback?code=AQC3l35_m9Av8fzPf102Mq3KXMbsZI48bQt8gE383YF3lbRPcOqErBclAHj
# ugn8jo_4WSZDsxRGbo_guQAXG1UW7hOMTfM7i3uhTDHYNP7VxIv75QFBIKjdPgooKEm7obdG8FobIDIYiBAzYxgRj0ZNxrRPz
# hos9HGV5bl5Kucsi3errXC7m9Z4AcxXcR8gCeFPYgg8JgkM4A53-DlJ_UdNjc7WEFQYsK1yr7G3XBmSS8IhzIFpkPQtffoJaM
# xOwan9KKMjy9GhHHw&
# state=JAdUUHnmBX3MSBFPVEDbitvBfu9YQT
def accessRequest(_request, _client_id, _client_secret, _scope, _redirect_uri, _token_url):

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('oauth')
 
    """Step 2: Request access and refresh tokens Authorization."""
    #Retrieve state from Session 
    stored_state = _request.session.get('state', None)
    #Get state from request 
    req_state = _request.GET.get('state','')
    #InvalidGrantError implement req_authcode control using the authorization_response which 
    # includes the the authorization verifier code from the callback url
    # By consequences 'code' is not stored in session
    # req_authcode = request.GET.get('code','')
        
    #Implement OAuth2 csrf protection testing state
    if (stored_state != req_state): 
        raise PermissionDenied

    #Prepare Client Secret
    client_auth = HTTPBasicAuth(_client_id, _client_secret)
    """ Step 3: Retrieving an access token.
        The user has been redirected back from the provider to the registered
        callback URL. With this redirection comes an authorization code included
        in the redirect URL. We will use that to obtain an access token.
    """
    oauth_session = OAuth2Session(_client_id, scope=_scope, redirect_uri=_redirect_uri)
    """fetch_token: (token_url, code=None, authorization_response=None, 
        body="", auth=None, username=None, password=None, method="POST", 
        force_querystring=False, timeout=None, headers=None, verify=True, 
        proxies=None, include_client_id=None, client_secret=None, **kwargs) 
    """
    try:
        _token = oauth_session.fetch_token(_token_url, auth=client_auth,
        authorization_response=_request.build_absolute_uri())
    #Manage error on navigator resfresh using same token
        """ TODO manage 
        Requests.exceptions.ConnectionError
        requests.exceptions.ConnectionError: 
        HTTPSConnectionPool(host='accounts.spotify.com', port=443): Max retries exceeded with url: /api/token (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x1061d4c40>: Failed to establish a new connection: [Errno 60] Operation timed out'))
        """
    except requests.exceptions.ConnectionError:
        return None #Error can happen with poor connexion
    except InvalidGrantError :
        raise SuspiciousOperation

    #String Token in session DB, keep this for later.
    saveSession(_request, token=_token)
    #Implement OAuth2 csrf protection testing existing client
    #return the Oauth2 Session token
    return _token


def ressourceRequest(_request, resource_url, _client_id, _token_url):
    """Step 4: Accessing to the Ressource
        Fetching a protected resource using an OAuth 2 token.
    """
    #Get Token from Session
    stored_token = _request.session.get('token')
    try:
        #Create Oauth Session
        oauth_session = OAuth2Session(_client_id, token=stored_token, auto_refresh_kwargs=None, auto_refresh_url=_token_url)
        #Fetch a protected resource, i.e. user profile
        api = oauth_session.get(resource_url)
    #Refreshing the token when required
    #Implementing (Second) Define automatic token refresh automatic but update manually
    # See https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html?highlight=TokenUpdated#second-define-automatic-token-refresh-automatic-but-update-manually
    ### TODO implement automatic_refresh(): see https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html?highlight=TokenUpdated#third-recommended-define-automatic-token-refresh-and-update   
    except TokenUpdated as e:
        # Save the refreshed token into the session 
        saveSession(_request, token=e.token)
    except InvalidClientError as e:
        return redirect(settings.OAUTH_ENDPOINT)
    return api.content


"""Save the session into Database"""
def saveSession(request, state=None, client_id=None, token=None):
    # Set Session 
    if (state!=None):
        request.session['state']=state
    if (client_id!=None):
        request.session['client_id']=client_id
    if (token!=None):
        request.session['token']=token

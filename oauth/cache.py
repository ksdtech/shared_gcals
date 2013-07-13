"""
ALL CODE IN THIS FILE IS A DERIVED WORK OF THE SDK EXAMPLE CODE.

Based on code Copyright 2012 Thomas Dignan <tom@tomdignan.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from apiclient.discovery import build
import httplib2
import pickle
import simple_cli

def get_stored_credentials_path():
    return "./.oauth_secrets"

def store_credentials(scopes):
    credentials = simple_cli.authenticate(scopes)
    pickled_creds_path = get_stored_credentials_path()
    pickle.dump(credentials, open(pickled_creds_path, "wb"))

def get_credentials():
    pickled_creds_path = get_stored_credentials_path()
    return pickle.load(open(pickled_creds_path, "rb"))

def build_service(credentials, api, version):
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build(api, version, http=http)

def authenticate(scopes):
    store_credentials(scopes)

def get_service_object(api, version):
    credentials = get_credentials()
    return build_service(credentials, api, version)


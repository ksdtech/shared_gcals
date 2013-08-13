""" 
Copyright 2012 Peter Zingg <pzingg@kentfieldschools.org>

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
from oauth import cache, simple_cli
import gdata.sites.client
import sys

def list_sites(client, all_sites=False):
    param = { }
    if all_sites:
        param['include-all-sites'] = 'true'
    feed = client.GetSiteFeed(**param)
    
    for entry in feed.entry:
        print '%s (%s)' % (entry.title.text, entry.site_name.text)
        if entry.summary.text:
            print 'description: ' + entry.summary.text
        print 'theme: ' + entry.theme.text
        if entry.FindSourceLink():
            print 'this site was copied from site: ' + entry.FindSourceLink()
        acl_feed_url = entry.FindAclLink()
        # print 'acl feed: %s' % acl_feed_url
        acl_feed = client.GetAclFeed(acl_feed_url)
        public_role = None
        domain_role = None
        for acl_entry in acl_feed.entry:
            role = acl_entry.role
            if role is not None:
                role = role.value
            scope = acl_entry.scope
            if str(scope.type) == 'default':
                public_role = role
            elif str(scope.type) == 'domain':
                domain_role = role
        if public_role is not None:
            print "site is PUBLIC, anyone on the internet - %s" % public_role
        if domain_role is not None:
            print "anyone in %s - %s" % (client.domain, domain_role)
        if public_role is None and domain_role is None:
            print "site is PRIVATE"
        print "user and group roles:"
        for acl_entry in acl_feed.entry:
            scope = acl_entry.scope
            if str(scope.type) != 'default' and str(scope.type) != 'domain':
                role = acl_entry.role
                if role is not None:
                    role = role.value
                print '    %s (%s) - %s' % (scope.value, scope.type, role)
        print "\n"

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="List sites information for a domain.")
    parser.add_argument('-a', '--authenticate', action='store_true',
                       help='(re-)authenticate via OAuth2')
    parser.add_argument('-f', '--full', action='store_true', 
                        help='show all sites in domain, not just those shared with user')
    parser.add_argument('domain', help='domain for client')
    args = parser.parse_args()
    
    if args.authenticate:
        cache.authenticate('https://sites.google.com/feeds/')
    
    client = gdata.sites.client.SitesClient(source='sites-manager-v1', site='', domain=args.domain)
    cache.authorize_gdata_client(client)
    list_sites(client, args.full)

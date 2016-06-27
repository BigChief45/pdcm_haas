import urllib2
import urllib
import base64

# Get the new tenant username and password from Horizon
# ...

# Zenoss administrator username and password
zHost = '100.67.130.76:8080'
zUsername = 'admin'
zPassword = 'zenoss'
encoded_auth = base64.encodestring('%s:%s' % (zUsername, zPassword)).replace('\n', '')


# New Tenant User values
username = 'brian'
password = 'openstack'
email = 'jalvarez@itri.org.tw'

parameters = { 'userid': username, 'password': password, 'email': email, 'roles': [] } 
data = urllib.urlencode(parameters)

# Request to create a new user
try:
    req = urllib2.Request('http://' + zHost + '/zport/dmd/ZenUsers/manage_addUser', data)
    req.add_header('Authorization', 'Basic %s' % encoded_auth)
    response = urllib2.urlopen(req)
    result = response.read()

    # After user is created, remove the default ZenUser role
    parameters = {'role_id': 'ZenUser', 'principal_id': username}
    data = urllib.urlencode(parameters)

    req = urllib2.Request('http://' + zHost + '/zport/dmd/acl_users/roleManager/removeRoleFromPrincipal', data)
    req.add_header('Authorization', 'Basic %s' % encoded_auth)
    response = urllib2.urlopen(req)
except Exception as e:
    print e.message

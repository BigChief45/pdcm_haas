import urllib
import urllib2
import base64

# Zenoss administrator username and password
zHost = '100.67.130.76:8080'
zUsername = 'admin'
zPassword = 'zenoss'
encoded_auth = base64.encodestring('%s:%s' % (zUsername, zPassword)).replace('\n', '')

devices = {
    '62-maas2-compute': 'Group 1', # 100.67.130.160
    '68-maas2-controller': 'Group 2',   # 100.67.130.153
    '69-maas2-compute': 'Group 2', # 100.67.130.154
    '70-maas2-compute': 'Group 3' # 100.67.130.155
    }

# This array will handle non-duplicated groups from the list
groups = []


# Create the user groups from the dictionary obtained
for device, group in devices.iteritems():
    # First, add the group to the non-duplicated list
    if group not in groups : groups.append(group)

    try:
        print "Creating user group '%s'..." % group
        
        parameters = {'groupid': group}
        data = urllib.urlencode(parameters)
        
        # Create a USER GROUP with the same name as the DEVICE GROUP
        req_url = 'http://' + zHost + '/zport/dmd/ZenUsers/manage_addGroup'
        req = urllib2.Request(req_url, data)
        req.add_header('Authorization', 'Basic %s' % encoded_auth)
        response = urllib2.urlopen(req)
        result = response.read()
        
    except urllib2.HTTPError, err:
        if err.code == 404:
            print 'ERROR 404: Page not found.'
        elif err.code == 403:
            print 'ERROR 403: Access denied.'
        else:
            print 'ERROR: Error Code ', err.code
            
    except urllib2.URLError, err:
        print 'ERROR: Unknown Error: ', err.reason

# Assign the device groups to the user groups as administered objects
for group in groups:
    try:
        parameters = {'newId': group}
        data = urllib.urlencode(parameters)
                
        print "Assigning USER GROUP '%s' to DEVICE GROUP '%s'" % (group, group)
                        
        req_url = urllib.quote('http://%s/zport/dmd/Groups/%s/manage_addAdministrativeRole' % (zHost, group), safe="%/:=&?~#+!$,;'@()*[]")
               
        req = urllib2.Request(req_url, data)
        req.add_header('Authorization', 'Basic %s' % encoded_auth)
        req.add_header('accept','*/*')
        response = urllib2.urlopen(req)
        result = response.read()
    except urllib2.HTTPError, err:
        if err.code == 404:
            print 'ERROR 404: Page not found.'
        elif err.code == 403:
            print 'ERROR 403: Access denied.'
        else:
            print 'ERROR: Error Code ', err.code
                                                            
                                                                        

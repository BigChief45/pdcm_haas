import urllib2
import urllib
import base64

# Get the device:group data from HaaS portal
# For now, we assume the data is in dictionary form with format:
# device_hostname : group_name
devices = {
    '62-maas2-compute': 'Group 1', # 100.67.130.160
    '68-maas2-controller': 'Group 2',   # 100.67.130.153
    '69-maas2-compute': 'Group 2', # 100.67.130.154
    '70-maas2-compute': 'Group 3' # 100.67.130.155
    }

# Zenoss administrator user name and password
zHost = '100.67.130.76:8080'
zUsername = 'admin'
zPassword = 'zenoss'
encoded_auth = base64.encodestring('%s:%s' % (zUsername, zPassword)).replace('\n', '')


# Place every device (should also exist in Zenoss) into the corresponding group
# If the group does not exist, it will be created automatically
for device, group in devices.iteritems():
    parameters = {'groupPaths': group}
    data = urllib.urlencode(parameters)
    
    try:
        print "Adding device %s to group %s..." % (device, group)

        req_url = 'http://' + zHost + '/zport/dmd/Devices/Server/SSH/Linux/NovaHost/devices/' + device + '/setGroups'
        req = urllib2.Request(req_url, data)
        req.add_header('Authorization', 'Basic %s' % encoded_auth)
        response = urllib2.urlopen(req)
        result = response.read()
        
        print "Successfully added device %s to group %s." % (device, group)
    except Exception as e:
        print e.message


# After all the devices have been assigned to the corresponding groups,
# The device group must be assigned to a user group

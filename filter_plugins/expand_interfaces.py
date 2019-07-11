#!/usr/bin/python

import re

class FilterModule(object):
    '''
    Define custom Jinja2 Filters
    '''

    def filters(self):
        return {
            'expand_interfaces': self.expand_interfaces
        }

    def expand_interfaces(self, interfaces):
        '''
        Takes an interface range and expands it
        Example: ['Ethernet1-3'] with be exapanded to ['Ethernet1','Ethernet2','Ethernet3']
        '''
        items = set()
        if type(interfaces) is list:
            for group in [x.strip() for x in interfaces]:
                ranges = [x.strip() for x in group.split('-')]
                if len(ranges) == 2:
                    [start, end] = [x.lower() for x in ranges]
                    new_start = re.sub("\D", "", start)
                    start_index = int(new_start)
                    end_index = int(end)
                    for index in range(start_index, end_index + 1):
                        items.add('{0}{1}'.format('Ethernet','/'.join([str(index)])))

        else:
            #Ansible doesn't like this for some reason
    #    elif type(interfaces) is str:
            ranges = [x.strip() for x in interfaces.split('-')]
            if len(ranges) == 2:
                [start, end] = [x.lower() for x in ranges]
                new_start = re.sub("\D", "", start)
                start_index = int(new_start)
                end_index = int(end)
                for index in range(start_index, end_index + 1):
                    items.add('{0}{1}'.format('Ethernet',str(index)))
            elif len(ranges) == 1:
                intf_no = re.sub("\D", "", ranges[0])
                prefix = 'Ethernet'
                items.add('{0}{1}'.format(prefix, intf_no))

        return sorted(items)

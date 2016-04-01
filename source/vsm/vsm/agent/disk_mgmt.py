# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# pylint: disable=W0212
# pylint: disable=R0913
# pylint: disable=W0233
# pylint: disable=W0231

"""
Tools for disk mgmt.
"""


from vsm import flags
from vsm.openstack.common import log as logging
from vsm import utils

LOG = logging.getLogger(__name__)

FLAGS = flags.FLAGS



class DiskPartitionMgmt(object):

    def __init__(self,disk_name=None):
        self.disk_name = disk_name
        self.size = ''
        self.disk_type = ''
        self.sector_physical_size = 512
        self.sector_logical_size = 512
        self.parts = []
        self.refresh_attrs()

    def get_disk_info(self):
        self.refresh_attrs()
        disk_info = {'disk_type':self.disk_type,
                     'size':self.size,
                     'disk_name':self.disk_name,
                     'parts':self.parts,
                     'sector_physical_size':self.sector_physical_size,
                     'sector_logical_size':self.sector_logical_size,
        }
        return disk_info

    def refresh_attrs(self):
        contents = self.show_partition_table()
        lines = contents.split('\n')
        partition_begin = -1
        i = 0
        for line in lines:
            if partition_begin > -1 and i > partition_begin:
                line_list = line.split()
                if len(line_list) >= 5:
                    part_dict = {'number':int(line_list[0]),
                                 'start':line_list[1],
                                 'end':line_list[2],
                                 'size':line_list[3],
                                 'type':line_list[4],
                                }
                    self.parts.append(part_dict)
            else:
                if line.startswith('Model') and len(line.split(':'))>1:
                    self.disk_type = line.split('Model:')[1]
                elif line.startswith('Disk /') and len(line.split(':'))>1:
                    size_str = line.split(':')[1]
                    self.size = size_str.strip()
                elif line.startswith('Number'):
                    partition_begin = i
                elif line.startswith('Sector') and len(line.split(':'))>1:
                    sector_size_list = line.split(':')[1].replace('B','').split('/')
                    self.sector_physical_size = int(sector_size_list[0])
                    self.sector_logical_size = int(sector_size_list[1])
            i = i+1

    def add_part(self,  part):
        ret, err = utils.execute("parted", "-s", self.disk_name, "mkpart", \
                              part['type'], part['start'], part['end'])
        self.parts.append(part)

    def delete_part(self,  part):
        utils.execute("parted", "-s", self.disk_name, "rm", \
                              part['number'])
        for p in self.parts:
            if p['number'] == part['number']:
                self.parts.remove(p)
                break

    def show_partition_table(self):
        table , err = utils.execute("parted", "-s", self.disk_name, "print")
        return table

    def get_partition_dict(self):
        self.refresh_attrs()
        return self.parts

    def rebulid_partition_table(self):
        utils.execute("parted", "-s", self.disk_name, "mklabel", "msdos")
        self.parts = []

    def add_parts(self,partitions=[]):
        for part in partitions:
            self.add_part(part)

if __name__ == '__main__':
    rebuild_partition_table=True
    disk_name='/dev/vdc'
    partitions=[{
                'number':1,
                'start':0,
                'end':'1G',
                'size':'1G',
                'type':'primary',
    },
    {
                'number':2,
                'start':1000,
                'end':2000,
                'size':1000,
                'type':'primary',
    },
    {
                'number':3,
                'start':'2000MB',
                'end':'4000MB',
                'size':'2000MB',
                'type':'extended',
    },
    {
                'number':5,
                'start':2000,
                'end':3000,
                'size':1000,
                'type':'logical',
    },
    ]
    disk = DiskPartitionMgmt(disk_name)
    #print '111>>>',disk.show_partition_table()
    #
    # disk.rebulid_partition_table()
    # print '222>>>',disk.show_partition_table()
    #
    # disk.add_parts(partitions)
    # print '333>>>',disk.show_partition_table()
    #
    # disk.delete_part(partitions[0])
    # print '444>>>',disk.show_partition_table()
    #
    # print '555>>>',disk.get_disk_info()




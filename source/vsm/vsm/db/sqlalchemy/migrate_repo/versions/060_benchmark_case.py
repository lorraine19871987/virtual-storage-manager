# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Inc.
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

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String, Table


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    benchmark_cases = Table(
        'benchmark_cases', meta,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('name', String(length=255), nullable=False),
        Column('direct', Boolean, default=True, nullable=False),
        Column('time_based', Boolean, default=True, nullable=False),
        Column('readwrite', String(length=255), nullable=False),
        Column('blocksize', String(length=255), nullable=False),
        Column('iodepth', Integer, nullable=False),
        Column('ramp_time', Integer, nullable=False),
        Column('runtime', Integer, nullable=False),
        Column('ioengine', String(length=255), nullable=False),
        Column('clientadmin', String(length=255), nullable=False),
        # Column('pool', String(length=255)),
        # Column('rbdname', String(length=255)),
        Column('iodepth_batch_submit', Integer, nullable=False),
        Column('iodepth_batch_complete', Integer, nullable=False),
        Column('norandommap', Boolean),
        Column('randrepeat', Boolean),
        Column('rate_iops', Integer),
        Column('random_distribution', String(length=255)),
        Column('rate', String(length=255)),
        Column('rwmixread', Integer),
        Column('additional_options', String(length=255)),
        Column('status', String(length=255), default='ready', nullable=False),
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
    )

    try:
        benchmark_cases.create()
    except Exception:
        meta.drop_all(tables=[benchmark_cases])
        raise

def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    benchmark_cases = Table('benchmark_cases',
                    meta,
                    autoload=True)
    benchmark_cases.drop()

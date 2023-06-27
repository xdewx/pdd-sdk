#!/usr/bin/env python3
# coding:utf-8

#
# Author: leoking
# Date: 2023-04-18 23:44:16
# LastEditTime: 2023-04-18 23:50:49
# LastEditors: leoking
# Description:
#

from sqlalchemy.orm import declarative_base
from sqlalchemy import JSON, Column, Integer, SmallInteger, String

DataSet = declarative_base(name="dataset")


class RegionTable(DataSet):
    __tablename__ = 'region'
    region_id = Column(Integer, primary_key=True)
    region_name = Column(String, nullable=False)
    region_type = Column(SmallInteger)
    parent_id = Column(Integer, nullable=True)
    region_tag = Column(SmallInteger)
    location = Column(JSON, nullable=True)

"use client"

import React, { useRef, useState } from 'react';
import { SearchOutlined } from '@ant-design/icons';
import type { InputRef, TableColumnsType, TableColumnType } from 'antd';
import { Button, Input, Space, Table } from 'antd';
import type { FilterDropdownProps } from 'antd/es/table/interface';
import Highlighter from 'react-highlight-words';




export default function DataList<Type, Data>({ columns, data }
    : { columns: TableColumnsType<Type>, data: Data[] }) {


    return <Table columns={columns} dataSource={data} />
}
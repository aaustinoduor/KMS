"use server"

import DataList from "@/components/DataList";
import NavBar from "@/components/NavBar";
import SideBar from "@/components/SideBar";
import StatusBar from "@/components/StatusBar";
import { TableColumnsType } from "antd";

export default function Home() {

  interface DataType {
    key: string;
    name: string;
    age: number;
    address: string;
  }

  const columns: TableColumnsType<DataType> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      width: '30%'
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
      width: '20%',
    },
    {
      title: 'Address',
      dataIndex: 'address',
      key: 'address',
      sorter: (a, b) => a.address.length - b.address.length,
      sortDirections: ['descend', 'ascend'],
    },
  ];


  const data: DataType[] = [
    {
      key: '1',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
    },
    {
      key: '2',
      name: 'Joe Black',
      age: 42,
      address: 'London No. 1 Lake Park',
    },
  ]

  return (
    <div id="Home" className="h-dvh">
      <SideBar />
      <NavBar />
      <div id="Main" style={{ gridArea: "main" }}>
        Hello from App Content

        <DataList columns={columns} data={data} />
      </div>
      <StatusBar />
    </div>
  );
}

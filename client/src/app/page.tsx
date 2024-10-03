"use client"

import DataList from "@/components/DataList";
import NavBar from "@/components/NavBar";
import SideBar from "@/components/SideBar";
import StatusBar from "@/components/StatusBar";

export default function Home() {

 
  return (
    <div id="Home" className="h-dvh">
      <SideBar />
      <NavBar />
      <div id="Main" style={{ gridArea: "main" }}>
        Hello from App Content

        <DataList />

      </div>
      <StatusBar />
    </div>
  );
}

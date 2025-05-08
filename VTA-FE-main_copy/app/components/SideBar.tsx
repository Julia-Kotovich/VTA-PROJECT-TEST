import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useChatContext } from "../Context/ChatContext";
import { useRouter } from "next/router";
import { CiCircleQuestion, CiChat1, CiClock2, CiStar, CiSettings, CiEdit } from "react-icons/ci";

export default function SideBar() {
  const [isOpenModal, setIsOpenModal] = useState(false)
  const useChat = useChatContext();
  
  return (
    <>
      <div
        className="h-[100vh] sm:ml-[0] ml-[-8rem] shadow-md "
        id="sidebar-wrapper"
      >
        <div className="w-[8rem] flex flex-col gap-5 justify-around">
          <div className="w-[4.2rem] flex justify-center items-center m-auto h-[60px] mt-[1rem]">
          </div>
          <div className="w-[4.2rem] m-auto h-[300px] rounded-full py-2">
            <ul className="p-2 space-y-8">
              <li className="hover:bg-[#E8E8E8] hover:scale-110 flex justify-center items-center hover:rounded-full h-[3.3rem] w-[3.3rem] text-center flex-col">
                <Link href="/chat" className="flex items-center justify-center flex-col">
                  <CiChat1 size={35} className="text-[#1240AB] stroke-[0.75]" />
                  <span className="text-[#1240AB] text-xs mt-1">chat</span>
                </Link>
              </li>
              {/* History button temporarily hidden
              <li className="hover:bg-[#E8E8E8] hover:scale-110 flex justify-center items-center hover:rounded-full h-[3.3rem] w-[3.3rem] text-center flex-col">
                <Link href="#" className="flex items-center justify-center flex-col">
                  <CiClock2 size={35} className="text-[#1240AB] stroke-[0.75]" />
                  <span className="text-[#1240AB] text-xs mt-1">history</span>
                </Link>
              </li>
              */}
              <li className="hover:bg-[#E8E8E8] hover:scale-110 flex justify-center items-center hover:rounded-full h-[3.3rem] w-[3.3rem] text-center flex-col">
                <Link
                  href="#"
                  className="flex items-center justify-center flex-col"
                  onClick={() => useChat.handleModal()}
                >
                  <CiStar size={35} className="text-[#1240AB] stroke-[0.75]" />
                  <span className="text-[#1240AB] text-xs mt-1">feedback</span>
                </Link>
              </li>
              <li className="hover:bg-[#E8E8E8] hover:scale-110 flex justify-center items-center hover:rounded-full h-[3.3rem] w-[3.3rem] text-center flex-col">
                <Link href="#" className="flex items-center justify-center flex-col" onClick={() => useChat.handleSettingsModal()}>
                  <CiSettings size={35} className="text-[#1240AB] stroke-[0.75]" />
                  <span className="text-[#1240AB] text-xs mt-1">settings</span>
                </Link>
              </li>
              {/*
              <li className="hover:bg-[#E8E8E8] hover:scale-110 flex justify-center items-center hover:rounded-full h-[3.3rem] w-[3.3rem] text-center flex-col">
                <Link href="#" className="flex items-center justify-center flex-col" onClick={() => useChat.handleTrainingModal()}>
                  <CiEdit size={35} className="text-[#1240AB] stroke-[0.75]" />
                  <span className="text-[#1240AB] text-xs mt-1">train</span>
                </Link>
              </li>
              */}
              <li className="hover:bg-[#E8E8E8] hover:scale-110 flex justify-center items-center hover:rounded-full h-[3.3rem] w-[3.3rem] text-center flex-col">
                <Link
                  href="/"
                  className="flex items-center justify-center flex-col"
                  id="homeBtn"
                >
                  <CiCircleQuestion size={35} className="text-[#1240AB] stroke-[0.75]" />
                  <span className="text-[#1240AB] text-xs mt-1">about</span>
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}

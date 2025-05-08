"use client";
import React from "react";
import SideBar from "./SideBar";
import { MainContent } from "./MainContent";
import Image from "next/image";
import { ChatProvider, useChatContext,  } from "../Context/ChatContext";
import RatingModal from "./RatingModal";

interface DashboardContentProps {
  children: React.ReactNode;
  target: string;
}
export const Dashboard: React.FC<DashboardContentProps> = ({ children, target }) => {
  return (
    <div className="h-screenoverflow-y-hidden ">
      <div className="overflow-x-hidden flex relative" id="landing-page">
        <ChatProvider>
          <SideBar />
          <MainContent target={target}>
            {children}
          </MainContent>
        </ChatProvider>
      </div>
    </div>
  );
};

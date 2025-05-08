"use client";
import Image from "next/image";
import { useRouter } from "next/navigation";
import React, { useEffect, useRef, useState } from "react";
import HomeContent from "./HomeContent";
import UserChat from "./UserChat";
import BotChat from "./BotChat";
import { useChatContext } from "../Context/ChatContext";
import RatingModal from "./RatingModal";
import SettingsModal from "./SettingsModal";
import TrainingDataModal from "./TrainingDataModal";
import HeaderSection from "./Header";
import useCsrfToken from "../hooks/usecsrf";
import { CiPaperplane, CiImport } from "react-icons/ci";
import html2pdf from 'html2pdf.js';

interface ChatType {
  userPrompt: string;
  botResponse: string;
}

interface MainContentProps {
  children: React.ReactNode;
  target: string;
}

export const MainContent: React.FC<MainContentProps> = ({ children, target }) => {
  const router = useRouter();
  const useChat = useChatContext();
  const [content, setContent] = useState();
  const [userInput, setUserInput] = useState("");
  const { isOpenModal, isSettingsOpen, isTrainingOpen, chatHistory, addChatMessage, generateVTAResponse } = useChatContext();

  const chatContainerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  useEffect(() => {
    console.log("Current target:", target);
  }, [target]);

  async function handleChat(ev: any) {
    ev.preventDefault();
    if (userInput.trim()) {
      const VTAResponse = await generateVTAResponse(userInput);
      addChatMessage(userInput, VTAResponse);
      setUserInput(""); // clear user input
      router.push("/chat"); // Redirect to chat page after sending message
    }
  }

  // handle chat submission by pressing ENTER
  async function handleKeyDown(ev: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (ev.key === "Enter") {
      ev.preventDefault(); // Prevent form submission (if the input is inside a form)
      if (userInput.trim()) {
        const VTAResponse = await generateVTAResponse(userInput);
        addChatMessage(userInput, VTAResponse.trim());
        setUserInput(""); // clear user input
        router.push("/chat"); // Redirect to chat page after sending message
      }
    }
  }

  const exportToPDF = () => {
    const element = document.createElement('div');
    element.innerHTML = `
      <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h1 style="color: #1240AB; font-size: 20px; margin-bottom: 10px;">Chat History with Capstone VTA</h1>
        <p style="color: #666; font-size: 12px; margin-bottom: 20px;">Generated on: ${new Date().toLocaleString()}</p>
        ${chatHistory.map(chat => `
          <div style="margin-bottom: 20px; page-break-inside: avoid;">
            <p style="margin: 0 0 10px 0; padding: 5px 0;">You: ${chat.userText}</p>
            <p style="color: #1240AB; margin: 0; padding: 5px 0; display: flex; justify-content: space-between; align-items: center;">
              <span>VTA: ${chat.VTAText}</span>
              <span style="color: #FFD700; margin-left: 10px;">
                ${chat.like ? '👍' : ''}${chat.dislike ? '👎' : ''}
              </span>
            </p>
          </div>
        `).join('')}
      </div>
    `;

    const opt = {
      margin: [0.5, 1, 0.5, 1],
      filename: 'capstone-vta-chat.pdf',
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { 
        scale: 2,
        letterRendering: true,
        useCORS: true
      },
      jsPDF: { 
        unit: 'in', 
        format: 'a4', 
        orientation: 'portrait',
        putOnlyUsedFonts: true
      },
      pagebreak: { 
        mode: ['avoid-all', 'css', 'legacy'],
        before: '.page-break'
      }
    };

    html2pdf().set(opt).from(element).save();
  };

  return (
    <>
      <div
        className="min-w-full sm:min-w-[0] w-[100%] px-6 py-6"
        id="page-content-wrapper"
      >
        <HeaderSection />
        {typeof window !== 'undefined' && chatHistory.length !== 0 && target !== 'home' ? (
          <>
            <section
              className="flex flex-col gap-2 h-[65vh] border-2 rounded-md mb-2 py-3 px-2 overflow-y-auto overflow-x-hidden"
              ref={chatContainerRef}
            >
              {chatHistory.map((chat, index) => (
                <div className="mb-6 px-2 md:px-4" key={index}>
                  <UserChat message={chat.userText} key={index} />
                  <BotChat
                    message={chat.VTAText}
                    key={index + 1}
                    chatId={index}
                    like={chat.like}
                    dislike={chat.dislike}
                    currentUserId={useChat.currentUserId}
                  />
                </div>
              ))}
            </section>
            <div className="flex justify-end mb-2">
              <button
                onClick={exportToPDF}
                className="flex items-center gap-2 px-4 py-2 bg-[#1240AB] text-white rounded hover:bg-[#1240AB]/90 text-sm"
              >
                <CiImport size={20} />
                Download Chat History (PDF)
              </button>
            </div>
          </>
        ) : (
          <> {children}</>
        )}

        <section>
          <form onSubmit={handleChat} className="flex flex-nowrap gap-2">
            <div className="mt-2 w-[95%]">
              <textarea
                name="item_description"
                id="item_description"
                placeholder="Type your message to Capstone VTA here..."
                className="block w-full bg-[#F5F5F5] px-2 rounded-md border-0 py-1.5 text-[#1240AB] shadow-sm placeholder:text-[#1240AB]/60 placeholder:text-xs focus:ring-0 focus:ring-[#1240AB] sm:text-sm sm:leading-6 h-[2.5rem] resize-none"
                value={userInput}
                onChange={(ev) => setUserInput(ev.target.value)}
                onKeyDown={handleKeyDown}
              ></textarea>
            </div>
            <div className="bg-[#F5F5F5] flex justify-center items-center p-2 rounded mt-2 h-[2.5rem]">
              <button type="submit" disabled={userInput.length == 0}>
                <CiPaperplane size={20} className="text-[#1240AB]/60" />
              </button>
            </div>
          </form>
        </section>
      </div>

      <RatingModal isOpen={isOpenModal} />
      <SettingsModal isOpen={isSettingsOpen} />
      <TrainingDataModal isOpen={isTrainingOpen} />
    </>
  );
};

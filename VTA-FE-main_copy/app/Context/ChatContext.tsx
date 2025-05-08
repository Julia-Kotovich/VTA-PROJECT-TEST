"use client";
import { useContext, useState,useEffect } from "react";
import { createContext } from "react";
import { API_BASE_URL } from "@/constants";
import axios from "axios";
import { uuidv7 } from "uuidv7";



interface ChatMessage {
  userText: string;
  VTAText: string;
  like: boolean,
  dislike:boolean
}

interface VTAContextType {
  isOpenModal: boolean;
  handleModal: () => void;
  isSettingsOpen: boolean;
  handleSettingsModal: () => void;
  isTrainingOpen: boolean;
  handleTrainingModal: () => void;
  chatHistory: ChatMessage[];
  addChatMessage: (userQuery: string, VTAResponse: string) => void;
  generateVTAResponse: (query: string) => Promise<string>;
  currentUserId: string;
  updateLikeStatus: (like: boolean, dislike: boolean, id: number) =>void;
  customInstructions: string;
  updateCustomInstructions: (instructions: string) => void;
}
const ChatContext = createContext<VTAContextType | null>( null);
export const ChatProvider = ({children,}: Readonly<{children: React.ReactNode;}>) => {
  const [isOpenModal, setIsOpenModal] = useState<boolean>(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState<boolean>(false);
  const [isTrainingOpen, setIsTrainingOpen] = useState<boolean>(false);
  const [likeUpdated, setLikeUpdated] = useState(false);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [customInstructions, setCustomInstructions] = useState<string>("");
  const currentUserId = (uuidv7()).toString();

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const savedHistory = localStorage.getItem("VTAChatHistory");
      const savedInstructions = localStorage.getItem("VTACustomInstructions");
      if (savedHistory) {
        setChatHistory(JSON.parse(savedHistory));
      }
      if (savedInstructions) {
        setCustomInstructions(savedInstructions);
      }
    }
  }, []);

  useEffect(() => {
    if (typeof window !== 'undefined' && chatHistory.length > 0) {
      localStorage.setItem("VTAChatHistory", JSON.stringify(chatHistory));
    }
  }, [chatHistory, likeUpdated]);

  const handleModal = () => {
    return setIsOpenModal(!isOpenModal);
  };

  const handleSettingsModal = () => {
    return setIsSettingsOpen(!isSettingsOpen);
  };

  const handleTrainingModal = () => {
    return setIsTrainingOpen(!isTrainingOpen);
  };

  // Function to generate chatbot response
  const generateVTAResponse = async (query: string): Promise<string> => {
    try {
      const requestData = {
        query: query,
      };
      const response = await axios.post(
        `${API_BASE_URL}vta-answer/`,
        requestData
      );
      const VTAResponse = response.data.response;
      return VTAResponse;
    } catch (error) {
      console.log("Error requesting answer from VTA", error);
      return "Failed to retrieve answer from VTA";
    }
  };

  // Function to add a new chat message to the chat history
  const addChatMessage = (userQuery: string, VTAResponse: string) => {
    const newChatMessage: ChatMessage = {
      userText: userQuery,
      VTAText: VTAResponse,
      like: false,
      dislike: false
    };
    setChatHistory((prevHistory) => [...prevHistory, newChatMessage]);
  };

  const updateLikeStatus = (like: boolean, dislike: boolean, id: number) =>{
    
    if (typeof window !== "undefined" && typeof localStorage !== "undefined") {
      chatHistory[id].like = like;
      chatHistory[id].dislike = dislike;     
      localStorage.setItem("VTAChatHistory", JSON.stringify(chatHistory));
      setLikeUpdated(!likeUpdated);
    } else {
      return []; 
    } 
  }

  const updateCustomInstructions = (instructions: string) => {
    setCustomInstructions(instructions);
    if (typeof window !== "undefined") {
      localStorage.setItem("VTACustomInstructions", instructions);
    }
  };

  return (
    <ChatContext.Provider
      value={{
        isOpenModal,
        handleModal,
        isSettingsOpen,
        handleSettingsModal,
        isTrainingOpen,
        handleTrainingModal,
        chatHistory,
        addChatMessage,
        generateVTAResponse,
        currentUserId,
        updateLikeStatus,
        customInstructions,
        updateCustomInstructions
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChatContext = ():VTAContextType => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("setup chatContext");
    }
  return context;
}
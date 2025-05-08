import React, { useEffect, useState } from 'react'
import { AiFillDislike } from "react-icons/ai";
import { AiFillLike } from "react-icons/ai";
import { API_BASE_URL } from "@/constants";
import axios from "axios";
import { useChatContext } from '../Context/ChatContext';
import { ToastContainer, toast } from 'react-toastify';
import { CiDesktop } from "react-icons/ci";


interface BotChatProps {
  message: string;
  chatId: number;
  currentUserId: string;
  like: boolean;
  dislike: boolean;
}

export default function BotChat({ message, chatId,currentUserId,like,dislike }: BotChatProps): JSX.Element {
  const [isLiked,setIsLiked ]= useState(false)
  const [isDisLiked, setIsDisLiked] = useState(false)
  const useChat = useChatContext();
  
  
  async function handleLIke(ev:any) {
    const chatHistory = localStorage.getItem("VTAChatHistory")
    let data = null;
    let parsedChatHistory = null;
    if (chatHistory !== null) {
      try {
         parsedChatHistory = JSON.parse(chatHistory);
        if (Array.isArray(parsedChatHistory)) {
          data = parsedChatHistory[chatId]          
        }
      } catch (error) {
        console.log("Failed to parse chat history");
      }
    }
    Object.assign(data, { userId: currentUserId, likeStatus: !isLiked });  
    try {
      const response = await axios.post(`${API_BASE_URL}vta/like/`, data);
      const ratingResponse = response.data.response;
      useChat.updateLikeStatus(!isLiked,false,chatId)
      // console.log(ratingResponse);
      toast.success("Rating updated", {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "light",
      });
    } catch (error) {
      // console.log("Failed to rate chat", error);
         toast.error("Failed to rate chat", {
           position: "top-right",
           autoClose: 3000,
           hideProgressBar: false,
           closeOnClick: true,
           pauseOnHover: true,
           draggable: true,
           progress: undefined,
           theme: "light",
         });
      return "Failed to rate chat";
    }
       
    setIsLiked(!isLiked);  
    setIsDisLiked(false);
  }




  async function handleDisLIke(ev: any) {

    const chatHistory = localStorage.getItem("VTAChatHistory");
    let data = null;
    let parsedChatHistory = null;
       if (chatHistory !== null) {
         try {
            parsedChatHistory = JSON.parse(chatHistory);
           if (Array.isArray(parsedChatHistory)) {
             data = parsedChatHistory[chatId];
           }
         } catch (error) {
          //  console.log("failed to parse chat history");
         }
       }
       Object.assign(data, {
         userId: currentUserId,
         likeStatus: !isDisLiked,
       });
       try {
         const response = await axios.post(`${API_BASE_URL}vta/dislike/`, data);
         const ratingResponse = response.data.response;
         useChat.updateLikeStatus(false, !isDisLiked, chatId);
         console.log(ratingResponse);
                 toast.success("Rating updated", {
                   position: "top-right",
                   autoClose: 3000,
                   hideProgressBar: false,
                   closeOnClick: true,
                   pauseOnHover: true,
                   draggable: true,
                   progress: undefined,
                   theme: "light",
                 });
                 
       } catch (error) {
               toast.error("Failed to rate chat", {
                 position: "top-right",
                 autoClose: 3000,
                 hideProgressBar: false,
                 closeOnClick: true,
                 pauseOnHover: true,
                 draggable: true,
                 progress: undefined,
                 theme: "light",
               });
     
         return "Failed to rate chat";
       }
  

      setIsDisLiked(!isDisLiked);
      setIsLiked(false);
  }

  
  return (
    <>
      <div className="ms-3 md:ms-8 mt-2">
        <div className="bg-[#F5F5F5] p-1 rounded-full h-[1.5rem] w-[1.5rem] flex justify-center items-center">
          <CiDesktop size={14} className="text-[#1240AB] stroke-[1]" />
        </div>
        <div className="ms-6 -mt-1">
          <p className="w-[95%] text-[#1240AB] text-xs sm:text-[0.85rem] leading-snug">
            {message}
            <span className="float-right text-[#1240AB] flex gap-1">
              <AiFillLike
                className={`${like ? "text-yellow-400" : ""} cursor-pointer`}
                onClick={handleLIke}
              />
              <AiFillDislike
                className={`${dislike ? "text-yellow-400" : ""} cursor-pointer`}
                onClick={handleDisLIke}
              />
            </span>
          </p>
        </div>
      </div>
      <ToastContainer containerId="31" />
    </>
  );
}

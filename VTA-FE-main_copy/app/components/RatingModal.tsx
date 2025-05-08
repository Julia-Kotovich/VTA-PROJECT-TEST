import Image from 'next/image';
import React, { useState } from 'react'
import { useChatContext } from '../Context/ChatContext';
import { IoStarSharp } from "react-icons/io5";
import { API_BASE_URL } from "@/constants";
import axios from "axios";
import { toast, ToastContainer } from 'react-toastify';
import { errorMonitor } from 'events';
import { CiCircleRemove } from "react-icons/ci";

export default function RatingModal({ isOpen }: { isOpen: boolean }) {
  const useChat = useChatContext();
  const stars = [1,2,3,4,5]
  const [rating, setRating] = useState(0);
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);


  const handleRating = async (ev: any): Promise<void> => {
    setSending(true)
    ev.preventDefault();
      try {
        const requestData = {
          userFeedback: message,
          userId: useChat.currentUserId
        };
        const response = await axios.post(`${API_BASE_URL}vta/feedback/`,requestData);
        const successMessage = response.data.response;
        toast.success(successMessage, {
         position: "top-right",
         autoClose: 5000,
         hideProgressBar: false,
         closeOnClick: true,
         pauseOnHover: true,
         draggable: true,
         progress: undefined,
         theme: "light",
        });
      
        setMessage('');
        setSending(false)
      useChat.handleModal() // close modal
      } catch (error) {
        console.log("Error rating VTA", error);
        const errorMessage = "Failed to send feedback. Please try again later";
        toast.error(errorMessage, {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "light",
        });
        setMessage("");
        setSending(false);
        useChat.handleModal(); // close modal
      }
  };
  


  const handleStars = (ev: any) => {
    console.log(ev.target.index)
  }





  return (
    <>
      <div
        className={`sm:w-full md:w-2/3 h-[75vh] main-sec-v2-bg-color absolute top-6 bottom-4 left-[15%] mx-4 m-auto rounded z-10 ${
          !isOpen && "hidden"
        }`}
      >
        <form onSubmit={handleRating}>
          <div className="flex justify-between px-4 py-3 flex-nowrap items-center border-b border-[#1240AB]/20">
            <h5 className="bot-font tracking-widest text-base font-bold">
              Your feedback
            </h5>
            <div 
              className="p-2 hover:bg-[#1240AB]/10 hover:scale-110 hover:cursor-pointer rounded-full"
              onClick={() => useChat.handleModal()}
            >
              <CiCircleRemove size={30} className="text-[#1240AB]" />
            </div>
          </div>
          <div className="p-6 text-[#1240AB]">
            <textarea
              name="review"
              id="item_description"
              placeholder="Write your feedback about VTA here..."
              className="w-full h-52 p-4 rounded bg-white/90 text-sm"
              onChange={(ev) => setMessage(ev.target.value)}
            ></textarea>
          </div>
          <div className="px-6">
            <input
              type="submit"
              value="Send"
              className={`bot-font-2 main-prm-bg-color p-3 pl-6 font-bold w-1/2 rounded text-left ${
                sending
                  ? "cursor-not-allowed"
                  : "hover:bg-yellow-500 cursor-pointer"
              } `}
              disabled={sending}
            />
          </div>
        </form>
      </div>
      <ToastContainer />
    </>
  );
}

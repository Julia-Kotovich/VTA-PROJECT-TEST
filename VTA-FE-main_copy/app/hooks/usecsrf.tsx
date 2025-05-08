import axios from "axios";
import { useEffect, useState } from "react";

const useCsrfToken = () => {
  const [csrfToken, setCsrfToken] = useState("");

   useEffect(() => {
     const fetchCsrfToken = async () => {
       try {
         const response = await axios.get("/csrf-token", {
           withCredentials: true,
         });
         setCsrfToken(response.data.csrfToken);
       } catch (error) {
         console.error("Failed to fetch CSRF token:", error);
       }
     };

     fetchCsrfToken();
   }, []);

  return csrfToken;
};

export default useCsrfToken;

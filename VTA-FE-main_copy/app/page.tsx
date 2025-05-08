import { ToastContainer } from "react-toastify";
import { Dashboard } from "./components/Dashboard";
import HomeContent from "./components/HomeContent";


export default function Home() {
  return (
    <main>
      <Dashboard target="home">
        <>
          <HomeContent/>
        </>
      </Dashboard>
      <ToastContainer/>
    </main>
  );
}

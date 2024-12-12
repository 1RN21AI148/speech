
import SongsPage from "./SongsPage";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';



function App() {
  return (
    <div className="App" >
        <SongsPage/>
        <ToastContainer position="top-right" autoClose={5000} />
    </div>
  );
}

export default App;

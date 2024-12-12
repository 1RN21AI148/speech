import { useState } from "react";
import { GENRES_ARRAY } from "../utils/constants";
import apiJson from "../services/apiJson";
import axios from "../services/axiosInstance"
import { toast } from 'react-toastify';

const Popup = ({isOpen,setIsOpen,setSongsData}) => {

    const [songName, setSongName] = useState('');
    const [songGenre, setSongGenre] = useState('');
    const [songPath, setSongPath] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Handle form submission logic here
        console.log({ songName, songGenre, songPath });
        sendDataToServer(songName, songGenre, songPath)
        setIsOpen(false); // Close the popup after submission
    };

    const sendDataToServer = async (songName, songGenre, songPath) => {
        const requestObject = {...apiJson['addSong']};
        requestObject.data = {
            song_name: songName,
            genre: songGenre,
            path: songPath.replace(/\\/g, '/')
        }
        try {
            const response = await axios(requestObject)
            console.log('response',response.data)
            setSongsData((prev)=>{
                return [...prev,requestObject.data]
            })
            toast.success('API call successful!', {
                position: toast.POSITION.TOP_RIGHT,
                autoClose: 5000,
              });
              
        } catch (error) {
            console.log(error)
        }
    }
    

    return (
        <>
        {isOpen && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
                <div className="bg-white rounded-lg p-6 w-1/3">
                    <h2 className="text-xl font-bold mb-4">Add New Song</h2>
                
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {/* Song Name */}
                        <div>
                            <label htmlFor="songName" className="block text-sm font-medium text-gray-700">
                            Song Name
                            </label>
                            <input
                                type="text"
                                id="songName"
                                className="mt-1 p-2 w-full border border-gray-300 rounded"
                                value={songName}
                                onChange={(e) => setSongName(e.target.value)}
                                required
                            />
                        </div>

                        {/* Song Genre */}
                        <div>
                            <label htmlFor="songGenre" className="block text-sm font-medium text-gray-700">
                            Song Genre
                            </label>
                            <select
                                id="songGenre"
                                className="mt-1 p-2 w-full border border-gray-300 rounded"
                                value={songGenre}
                                onChange={(e) => setSongGenre(e.target.value)}
                                required
                                >
                                <option value="">Select Genre</option>
                                {GENRES_ARRAY.map((genre, index) => (
                                    <option key={index} value={genre.toLowerCase()}>
                                    {genre}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Song Path */}
                        <div>
                            <label htmlFor="songPath" className="block text-sm font-medium text-gray-700">
                            Song Path
                            </label>
                            <input
                                type="text"
                                id="songPath"
                                className="mt-1 p-2 w-full border border-gray-300 rounded"
                                value={songPath}
                                onChange={(e) => setSongPath(e.target.value)}
                                required
                            />
                        </div>

                        {/* Buttons */}
                        <div className="flex justify-between mt-4">
                            <button
                                type="submit"
                                className="bg-blue-500 text-white px-4 py-2 rounded"
                            >
                                Submit
                            </button>
                            <button
                                type="button"
                                className="bg-red-500 text-white px-4 py-2 rounded"
                                onClick={() => setIsOpen(false)}
                            >
                                Close
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        )}
        </>
    )   
}

export default Popup
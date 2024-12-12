import React, { useEffect, useState } from 'react'
import TableHeader from './tableHeader'
import TableData from './tableData'
import { MOKE_SONGS_DATA } from '../utils/constants'
import Popup from './popup'
import apiJson from '../services/apiJson'
import axios from "../services/axiosInstance"
import { toast } from 'react-toastify';

const Table = () => {

  const [isOpen,setIsOpen] = useState(false)
  const [songsData, setSongsData] = useState([])

  useEffect(() => {
    fetchData();
  },[])

  const fetchData = async () => {
    const requestObject = {...apiJson['getSongs']};
    try {
        const response = await axios(requestObject)
        console.log('response songssss',response.data)
        setSongsData(response.data)
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
    <div>
        <TableHeader/>
        <TableData data={songsData}/>
    </div>
    <button 
      className='text-centerborder-2 border-black mt-10 w-full p-2 text-white'
      style={{ backgroundColor: '#282c34' }}
      onClick={()=>{setIsOpen(true)}}
      >
        Add new songs
    </button>
    <Popup isOpen={isOpen} setIsOpen={setIsOpen} setSongsData={setSongsData}/>
    </>
    
  )
}

export default Table
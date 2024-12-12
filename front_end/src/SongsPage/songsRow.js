import React from 'react'
import { HEADER_DATA } from '../utils/constants'

const SongsRow = ({index,songName,genre,path}) => {



  return (
    <div className='flex'>
        <h1 className='text-center  border-black  border-2' style={{ flex: HEADER_DATA[0].flex }}>{index}</h1>
        <h1 className='text-center  border-black  border-2' style={{ flex: HEADER_DATA[1].flex }}>{songName}</h1>
        <h1 className='text-center  border-black  border-2' style={{ flex: HEADER_DATA[2].flex }}>{genre}</h1>
        <h1 className='text-center  border-black  border-2' style={{ flex: HEADER_DATA[3].flex }}>{path}</h1>
    </div>
  )
}

export default SongsRow
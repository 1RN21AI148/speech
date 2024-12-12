import React from 'react'
import SongsRow from './songsRow'

const TableData = ({data}) => {


  if(!data.length){
    return (
      <div className='border-2 border-black flex flex-col justify-center items-center'>
          <img 
            className='h-[40vh]'
            src={require("../assets/nosong.png")}  
            alt='logo'
          />
          <h1>No Songs added yet!!  </h1>
      </div>
    ) 
  }

  return (
    <div className='max-h-[60vh] overflow-x-auto'>
      {data.map((e,i) => (
        <SongsRow 
          index={i+1}
          songName={e.song_name}
          genre={e.genre}
          path={e.path} 
        />
      ))}
    </div>
  )
  
}

export default TableData
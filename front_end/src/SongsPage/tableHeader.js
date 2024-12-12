import React from 'react'
import { HEADER_DATA } from '../utils/constants'





const TableHeader = () => {
  return (
    <>
        <h1 className='text-center border-2 p-2 border-black text-xl font-bold text-white' style={{ backgroundColor: '#282c34' }}>Songs</h1>
        <div className='flex mt-10 border-black  border-2'>
            {HEADER_DATA.map((data) => (
                <h1 className='text-center border-black border-t-2 border-r-2 font-bold' style={{ flex: data.flex }}>{data.lable}</h1>
            ))}
        </div>
    </>
  )
}

export default TableHeader
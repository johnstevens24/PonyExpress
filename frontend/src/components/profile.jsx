import { Link, useParams, useNavigate} from 'react-router-dom';
import { useQuery } from "react-query";
import React, { useState, useEffect } from 'react';
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";




function Profile() {
    const { logout } = useAuth();
    const user = useUser();
    const [username, setUsername] = useState("loading...")
    const [email, setEmail] = useState("loading...")
    const [memberSince, setMemberSince] = useState("loading...")

    const navigate = useNavigate();

    useEffect(() => {
      setUsername(user.username)
      setEmail(user.email)
      
    
      let joinDate = new Date(user.created_at)
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      const formattedDate = joinDate.toLocaleDateString('en-US', options);
      setMemberSince(formattedDate)
    }, [])
  
    const logoutUser = () => {
      logout()
    }

    return <div className="grid place-items-center mx-2 h-full w-full">
      <div className="flex flex-col py-10 h-full">
        <div className="flex flex-col border-2 rounded min-w-96 max-w-lg">
          <h2 className='p-2 text-2xl font-semibold'>details</h2>
          <div className="flex flex-row border-t-2 border-neutral-800">
            <h2 className="px-2 text-lg text-neutral-800">username</h2>
            <div className="flex-1"></div>
            <h2 className="px-2 text-lg">{username}</h2>  
          </div>
          <div className="flex flex-row border-t-2 border-neutral-800">
            <h2 className="px-2 text-lg text-neutral-800">email</h2>
            <div className="flex-1"></div>
            <h2 className="px-2 text-lg">{email}</h2>  
          </div>
          <div className="flex flex-row border-t-2 border-neutral-800">
            <h2 className="px-2 text-lg text-neutral-800">member since</h2>
            <div className="flex-1"></div>
            <h2 className="px-2 text-lg">{memberSince}</h2>  
          </div>
        </div>
        
        <div className='flex justify-center flex-row border-2 rounded mt-7 max-w-20'>
            <button onClick={() => logoutUser()} className='my-2'>logout</button>
        </div>
      </div>
    </div>
}

export default Profile;
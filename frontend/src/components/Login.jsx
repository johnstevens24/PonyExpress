import { Link, useParams, useNavigate} from 'react-router-dom';
import { useQuery } from "react-query";
import { useAuth } from "../context/auth";
import React, { useState, useEffect } from 'react';

function Error({ message }) {
  if (message === "") {
    return <></>;
  }
  return (
    <div className="text-red-300 text-xs">
      {message}
    </div>
  );
}

function Login() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("");

    const navigate = useNavigate();
    const { login } = useAuth();
    const disabled = username === "" || password === "";

    const onSubmit = (e) => {
      e.preventDefault();
  
      fetch(
        "http://127.0.0.1:8000/auth/token",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({ username, password }),
        },
      ).then((response) => {
        if (response.ok) {
          response.json().then(login);
          //wihtout this timeout statement, it doesn't work. Its like it needs a second to process the login.
          setTimeout(() => {
            navigate("/chats");
          }, 500);
        } else if (response.status === 401) {
          response.json().then((data) => {
            setError(data.detail.error_description);
          });
        } else {
          setError("error logging in");
        }
      });
    }
  
    
    return <div className="grid place-items-center mx-2 h-full w-full">
      <div className="flex flex-col py-10 h-full w-96">
        <form onSubmit={onSubmit}>
          <label className="text-lg">username * 
            <br/> 
            <input className="bg-neutral-500 border border-neutral-100 rounded w-full" type="text" value={username} onChange={() => setUsername(event.target.value)}/>
          </label>
          <label className='text-lg'>password * 
            <br/>  
            <input className="bg-neutral-500 border border-neutral-100 rounded  w-full" type="password" value={password} onChange={() => setPassword(event.target.value)}/>
          </label>
          <div type="submit" disabled={disabled} className='bg-neutral-100 flex justify-center flex-row border-2 border-neutral-100 rounded mt-7 max-w-20'>
            <button className='my-2 text-neutral-500 italic'>login</button>
          </div>
          <Error message={error} />
        </form>
        
       

        <div className='flex flex-row max-w-96 my-4'>
          <h2 className="">don't have an account?</h2>
          <Link to="/registration">
            <button className='mx-4 text-yellow-400'>create an account</button>
          </Link>
        </div>
      </div>
    </div>
}

export default Login;
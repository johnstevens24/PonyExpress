import { Link, useParams, useNavigate} from 'react-router-dom';
import { useQuery } from "react-query";
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

function Registration() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [email, setEmail] = useState("")
  const [error, setError] = useState("");

  const navigate = useNavigate();


  const submit = (e) => {
    e.preventDefault();
    fetch(
      "http://127.0.0.1:8000/auth/registration",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      },
    ).then((response) => {
      if (response.ok) {
        navigate("/login");
      } else if (response.status === 422) {
        response.json().then((data) => {
          setError(data.detail.entity_field + " already taken");
        });
      } else {
        setError("error logging in");
      }
    });
  }

  
  return <div className="grid place-items-center mx-2 h-full width-full">
    <div className="flex flex-col py-10 h-full w-96">

      <form onSubmit={submit}>
        <label className="text-lg">username * 
          <br/> 
          <input className="bg-neutral-500 border border-neutral-100 rounded w-full" type="text" value={username} onChange={() => setUsername(event.target.value)}/>
        </label>
        <label className='text-lg'>email * 
          <br/>  
          <input className="bg-neutral-500 border border-neutral-100 rounded  w-full" type="text" value={email} onChange={() => setEmail(event.target.value)}/>
        </label>
        <label className='text-lg'>password * 
          <br/>  
          <input className="bg-neutral-500 border border-neutral-100 rounded  w-full" type="password" value={password} onChange={() => setPassword(event.target.value)}/>
        </label>
        <div type='submit' className='bg-neutral-100 flex justify-center flex-row border-2 border-neutral-100 rounded mt-7 max-w-36'>
          <button className='my-2 text-neutral-500 italic'>create account</button>
        </div>
        <Error message={error} />
      </form>

      <div className='flex flex-row max-w-96 my-4'>
        <h2 className="">already have an account?</h2>
        <Link to="/login">
          <button className='mx-4 text-yellow-400'>login</button>
        </Link>
      </div>
    </div>
  </div>
}

export default Registration;
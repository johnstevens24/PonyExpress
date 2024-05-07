import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route, NavLink, Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import ChatID from './components/chatId'
import Chats from './components/chats'
import Profile from './components/Profile'
import Login from './components/Login'
import Registration from './components/Registration'



import { AuthProvider, useAuth } from "./context/auth";
import { UserProvider, useUser } from "./context/user";
// import './App.css'

const queryClient = new QueryClient();
// const [text, setText] = useState("login") 

function NotFound()
{
  return <h1>404: Not Found</h1>
}

function Home() {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div className="max-w-4/5 mx-auto text-center px-4 py-8">
      <div className="py-2">
        <p className="pb-5">The Pony Express application is a messenger app.</p>
        <Link className="border rounded px-3 py-2" to="/login">get started</Link>
      </div>
    </div>
  );
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Chats/>} />
      <Route path="/chats" element={<Chats/>} />
      <Route path="/chats/:chatId" element={<ChatID/>} />
      <Route path="/profile" element={<Profile/>} />
      <Route path="/error/404" element={<NotFound/>} />
      <Route path="*" element={<Navigate to="/chats" />} />
    </Routes>
  );
}

function UnauthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();
  const [username, setUsername] = useState("loading...")
  const user = useUser()

  useEffect(() => {
    if(user)
      setUsername(user.username)
  }, [user])

  return (
    <div className='bg-neutral-400 w-screen h-screen flex flex-col items-center'>
      <header className='w-2/3 bg-neutral-500'>
        <nav className='flex flex-row'>
          <NavLink to="/" className='px-10 py-2 hover:bg-slate-500'>pony express</NavLink>
          <div className='flex-1'></div>
          {isLoggedIn? 
            <NavLink to="/profile" className='px-10 py-2 hover:bg-slate-500'>{username}</NavLink> :
            <NavLink to="/login" className='px-10 py-2 hover:bg-slate-500'>login</NavLink>
          }
        </nav>
      </header>
      <main className="bg-neutral-400 h-5/6 w-2/3">
        {isLoggedIn ?
          <AuthenticatedRoutes /> :
          <UnauthenticatedRoutes />
        }
      </main>
    </div>
  );
}


function App() {

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <UserProvider>
              <Main />
          </UserProvider>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App

import { Link, useParams} from 'react-router-dom';
import { useQuery } from "react-query";
import React, { useState, useRef, useEffect } from 'react';
import { useUser } from "../context/user";

// LEFT COLUMN STUFF
function ChatList() {
    const authToken = sessionStorage.getItem("__pony_express_token__");
    const { data, isLoading, error } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
            fetch("http://127.0.0.1:8000/chats", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${authToken}`
                }
            }).then((response)=>response.json())
        ),
    });
    if(error) {
        return <div>Error: {error.message}</div>;
    }
    if (data && data.chats) {
        return (
           <div style={{display:'flex', flex:1, flexDirection:'column'}}>
            <h1>Chats</h1>
                <div style={{display:'flex', flexDirection:'column', overflowY:'scroll'}}>
                    {data.chats.map((chat)=> (<ChatBox chat={chat}/>))}
                </div>
           </div> 
        )

    }

}


function ChatBox({ chat }) {

    const [boxStyle, setBoxStyle] = useState({
        display: 'flex',
        flexDirection: 'column',
        padding: 5,
        margin: 3,
        border: '2px solid #D3D3D3',
        width:'80%'
      });


    const date = new Date(chat.created_at) 
    const chatId = chat.id
    return (
      <Link
        key={chat.id}
        to={`/chats/${chatId}`}
        onMouseEnter={() => setBoxStyle({display: 'flex',
          padding: 5,
          margin: 3,
          border: '2px solid black',
          width:'80%'})}
        onMouseLeave={() => setBoxStyle({display: 'flex',
        flexDirection: 'column',
        padding: 5,
        margin: 3,
        border: '2px solid #D3D3D3',
        width:'80%'})}
        style={boxStyle}
      >
        <p style={{color:"white"}}>
            <strong>{chat.name}</strong><br></br>
        </p>
      </Link>
    );
  }

// RIGHT COLUMN STUFF
function MessageList({ chatId, setRefresh }) {
    const authToken = sessionStorage.getItem("__pony_express_token__");
    const [data, setData] = useState(<h2>loading...</h2>)
    const lastMessageRef = useRef(null);
    const scrollToBottom = () => {
        if (lastMessageRef.current) {
            lastMessageRef.current.scrollIntoView({ behavior: "smooth" });
        }
    };

    useEffect(() => {
        scrollToBottom();
    }, [data]);
    
    useEffect(() => {
        getMessages()
    }, [chatId])

    const getMessages = () => {
        try{
            fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`,
            {
                method: "GET",
                headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${authToken}`
                },
                // body: JSON.stringify({ text })
            },
            ).then((response) => {
                if (response.ok) {
                    return response.json()
                } else {
                    setData(<p>Something unexpected happend</p>)
                }
            }).then((json) => {
                setData(<div style={{display:'flex', flexDirection:'column', height:"100%", overflowY:'scroll'}}>
                            {json.messages.map((message)=> (<MessageBox message={message} chatId={chatId} setRefresh={setRefresh}/>))} 
                            <div ref={lastMessageRef}></div>
                        </div>)
            })
        }
        catch(error)
        {
            setData(error.message);
        }
        
    }

    return data

}


function MessageBox({ message, chatId, setRefresh }) {
    const authToken = sessionStorage.getItem("__pony_express_token__");
    const currentUsername = useUser().username;
    const [openEdit, setOpenEdit] = useState(false)
    const [inputMessage, setInputMessage] = useState(message.text)

    function formatDate(){
        let joinDate = new Date(message.created_at)
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
            hour12: true // to display in 12-hour format with AM/PM
        };
        const formattedDate = joinDate.toLocaleDateString('en-US', options);
        return formattedDate;
    }

    const deleteChat = async () => {
        fetch(`http://127.0.0.1:8000/chats/${chatId}/messages/${message.id}`,
        {
            method: "DELETE",
            headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
            }
        },
        ).then((response) => {
            if (response.ok) {
                //this timeout is necessary otherwise it won't work
                setTimeout(setRefresh(true), 500)
            } else {
                setError("error deleting chat message");
            }
        });
    }
    
    const editChat = (e) => {
        e.preventDefault()
        
        if(inputMessage == "")
        {
            return;
        }

        //needs to be called "text" because thats what the api is expecting it to be called
        let text = inputMessage
        
        fetch(`http://127.0.0.1:8000/chats/${chatId}/messages/${message.id}`,
        {
            method: "PUT",
            headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
            },
            body: JSON.stringify({ text })
        },
        ).then((response) => {
            if (response.ok) {
                //reload messages
                setTimeout(setRefresh(true), 500)
            } else {
                setError("error posting chat message");
            }
        });

        //set inpt message to blank
        setInputMessage("")
    }

    
    

    //this just resets the message every time you open or close the edit box
    useEffect(() => {
            setInputMessage(message.text)
    }, [openEdit])

    return (
      <div style={{display: 'flex',
      flex:1,
      flexDirection: 'column',
      maxWidth:"98%",
      padding: 7,
      margin: 3,
      border: '1px solid #D3D3D3',
      borderRadius:"5px"}}>
            <div style={{display:'flex', flexDirection:'row', justifyContent:"space-between"}}>
                {message.user.username == currentUsername ? 
                    <p style={{color:"#6885B0", fontWeight:"bold", fontSize:20}}>{message.user.username}</p>
                    :
                    <p style={{color:"#647286", fontWeight:"bold", fontSize:20}}>{message.user.username}</p>
                }
                {message.user.username == currentUsername ? 
                    <div style={{width:"50%", display:'flex', flexDirection:"row", justifyContent:"flex-end", alignItems:"center"}}>
                        <p style={{fontSize:12, paddingRight:5}}>{formatDate()}</p>
                        <button style={{fontSize:12, paddingRight:5}} onClick={() => openEdit == true ? setOpenEdit(false) : setOpenEdit(true)}>edit</button>
                        <button style={{fontSize:12, paddingRight:5}} onClick={deleteChat}>delete</button>
                        {openEdit == true ? 
                            <div style={{backgroundColor:"#bfbfbf", 
                                        borderRadius:10, 
                                        border: '2px solid #D3D3D3', 
                                        position:'fixed', 
                                        width:"50%", 
                                        height:"30%", 
                                        top:"15%", 
                                        left:"25%", 
                                        zIndex:1}}>
                                <div style={{display:"flex", flexDirection:"row", justifyContent:"space-between", alignItems:"center", height:"25%", width:"100%", borderBottom:'2px solid #D3D3D3', backgroundColor:"#8d8d8d"}}>
                                    <p style={{fontSize:30, paddingLeft:"5%"}}>{message.user.username}</p>
                                    <p style={{fontSize:15, paddingRight:"5%"}}>{formatDate()}</p>
                                </div>
                                <form onSubmit={editChat} style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", height:"75%", width:"100%", padding:"10%"}}>
                                        <input style={{width:"100%", backgroundColor:"#8d8d8d", border: '1px solid #D3D3D3', borderRadius:5, padding:1, marginBottom:10}} type="text" value={inputMessage} onChange={() => setInputMessage(event.target.value)}></input>
                                        <div style={{display:"flex", flexDirection:"row", justifyContent:"flex-end", width:"100%", paddingTop:"5"}}>
                                            <button style={{border: '1px solid #D3D3D3', borderRadius:5, backgroundColor:"#8d8d8d", padding:3, marginRight:10}}>submit</button>
                                            <button style={{border: '1px solid #D3D3D3', borderRadius:5, backgroundColor:"#8d8d8d", padding:3}} onClick={() => {setOpenEdit(false)}}>cancel</button>
                                        </div>
                                        
                                </form>
                            </div> 
                            : 
                            <div></div>
                        }
                    </div> : 
                    <p style={{fontSize:12}}>{formatDate()}</p>
                }
            </div>
            <div>
                <p>{message.text}</p>
            </div>
      </div>
    );
  }

function Chats() {
    const authToken = sessionStorage.getItem("__pony_express_token__");
    const user = useUser();
    const { chatId } = useParams();
    const [body, setBody] = useState(null);
    const [inputMessage, setInputMessage] = useState("");
    const [refresh, setRefresh] = useState(false)
    const [check, setCheck] = useState(false)
    
    const refreshBody = async () => {
        //something about assignment 5 has broken my refresh code. I know this isn't an elegant or great solution but it works
        setBody(<p></p>)
        setTimeout(() => {
            setBody(<MessageList chatId={chatId} setRefresh={setRefresh}/>);
        }, 1);
    };

    useEffect(() => {
        if(refresh == true)
        {
            setRefresh(false)
            refreshBody()
        }
            
    }, [refresh])
    
    useEffect(() => {
        setBody(<MessageList chatId={chatId} setRefresh={setRefresh}/>);
    }, [chatId])

    const onSubmitChat = (e) => {
        e.preventDefault()
        
        if(inputMessage == "")
        {
            return;
        }

        //needs to be called "text" because thats what the api is expecting it to be called
        const text = inputMessage
        
        fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`,
        {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
            },
            body: JSON.stringify({ text })
        }).then((response) => {
            if (response.ok) {
                setInputMessage("")
                refreshBody()
            } else {
                setError("error posting chat message");
            }
        });
    }

    return <div style={{display:'flex', flex: 1, padding:10, flexDirection:'row', justifyContent:'space-between', width:'100%', height:"75%"}}> 
            <div id="column1" style={{display:'flex', width:'50%', height:"80%"}}>
                <ChatList/>
            </div>
            <div id="column2" style={{display:'flex', flexDirection:'column', width:'50%'}}>
                {body}
                <form onSubmit={onSubmitChat} style={{display:"flex", flexDirection:"row", height:"2rem", borderWidth:"1px", borderColor:"black", borderRadius:"5px", width:"100%", marginTop:"10px"}}>
                    <input type="text" value={inputMessage} className="bg-neutral-400 border border-neutral-100 rounded  w-full" onChange={() => setInputMessage(event.target.value)}></input>
                    <button className="bg-neutral-500 px-3 italic">send</button>
                </form>
            </div>
           </div>;
    
}

export default Chats;
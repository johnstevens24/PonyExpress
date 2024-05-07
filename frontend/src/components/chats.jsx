import { Link, useParams} from 'react-router-dom';
import { useQuery } from "react-query";
import React, { useState } from 'react';


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

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
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

// function makeUserList(chat){
//     let list = ""
//     let length = Object.keys(chat.user_ids).length
//     for(let i = 0; i < length; i++)
//     {
//         list += chat.user_ids[i]
//         if(i != (length - 1))
//             list += ", "
//     }
//     return list;
// }

function ChatBox({ chat }) {
    const [boxStyle, setBoxStyle] = useState({
        display: 'flex',
        flexDirection: 'column',
        padding: 5,
        margin: 3,
        border: '1px solid #D3D3D3',
        width:'80%'
      });


    const date = new Date(chat.created_at) 
    return (
      <Link
        key={chat.id}
        to={`/chats/${chat.id}`}
        onMouseEnter={() => setBoxStyle({display: 'flex',
          padding: 5,
          margin: 3,
          border: '2px solid black',
          width:'80%'})}
        onMouseLeave={() => setBoxStyle({display: 'flex',
        flexDirection: 'column',
        padding: 5,
        margin: 3,
        border: '1px solid #D3D3D3',
        width:'80%'})}
        style={boxStyle}
      >
        <p style={{color:"white"}}>
            <strong>{chat.name}</strong><br></br>
        </p>
      </Link>
    );
  }

  
function Chats() {
    
    return <div style={{display:'flex', flex: 1, padding:10, flexDirection:'row', justifyContent:'space-between', width:'100%', height:"75%"}}> 
            <div id="column1" style={{display:'flex', width:'50%', height:"80%"}}>
                <ChatList/>
            </div>
            <div id="column2" style={{display:'flex', width:'50%', padding: 5, justifyContent:'space-evenly'}}>
                <h1>Select a Chat</h1>
            </div>
           </div>;
}

export default Chats;
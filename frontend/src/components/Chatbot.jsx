import React, { useState } from 'react'
import { chat } from '../services/api'

export default function Chatbot(){
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(null)

  const send = async () => {
    if(!input) return
    const userMsg = { from: 'user', text: input }
    setMessages(prev=>[...prev, userMsg])
    const res = await chat(input, sessionId)
    setSessionId(res.session_id)
    setMessages(prev=>[...prev, { from: 'bot', text: res.response }])
    setInput('')
  }

  return (
    <div className="p-4 border rounded-md">
      <div style={{height: '300px', overflow:'auto', background:'#f7f7f7'}}>
        {messages.map((m,i)=>(
          <div key={i} style={{padding:8, textAlign: m.from==='user'? 'right':'left'}}>
            <b>{m.from}</b>: {m.text}
          </div>
        ))}
      </div>
      <div className="flex gap-2 mt-2">
        <input value={input} onChange={e=>setInput(e.target.value)} className="flex-1 p-2 border"/>
        <button onClick={send} className="p-2 bg-blue-600 text-white">Enviar</button>
      </div>
    </div>
  )
}

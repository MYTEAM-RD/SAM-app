import ReactInputVerificationCode from 'react-input-verification-code';
import Footer from "../../components/Footer/Footer";
import useCookie from 'react-use-cookie';
import "./Confirm.scss"

import { backendUrl } from '../../utils/var';

import { useEffect, useState } from 'react';

export default function Confirm() {

    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "")
    const [code, setCode] = useState("")
    const [email, setEmail] = useState("")

    function handleSubmit() {
          fetch(`${backendUrl}/api/v1/verify/email?code=${code}`, {
            method: 'GET',
            headers: {
              'accept': 'text/plain',
              'Content-Type': 'application/json'
            },
          })
            .then(response => {
              if (response.ok) {
                response.json().then(json => {
                    setToken(json.token, {days: 12})
                    window.location = "/dashboard";
                })
              } else {
                throw new Error('Request failed.'); // Throw an error if the response is not successful
              }
            })
            .catch(error => {
              // Handle any errors that occurred during the fetch request
              console.error(error);
            });
    }

    function newCode(){
      fetch(`${backendUrl}/api/v1/verify/new/email?email=${email}`, {
        method: 'GET',
        headers: {
          'accept': 'text/plain',
          'Content-Type': 'application/json'
        },
      })
        .then(response => {
          if (response.ok) {
              alert("Un nouveau code vous a été envoyé par email")
          }
        })
        .catch(error => {
          // Handle any errors that occurred during the fetch request
          console.error(error);
        });
    }

    useEffect(() => {
        console.log(code)
        console.log(code.length)
        if(code.length === 5 && code.includes("_") === false){
            handleSubmit()
        }
        // eslint-disable-next-line
    }, [code])

    return(
      <>
        <section className='verification'>
            <h1>Confirmer votre email</h1>
            <p>Un code de confirmation vous a été envoyé par email</p>
            <ReactInputVerificationCode length={5} autoFocus={true} placeholder='_' onChange={setCode}/>
            <div className='new'>
              <input type="text" placeholder="Email" onChange={(e)=>{setEmail(e.target.value)}}/>
              <button className='bigButton' onClick={newCode}>Envoyer un nouveau code</button>
            </div>
        </section>
        <Footer />
      </>
    )
}
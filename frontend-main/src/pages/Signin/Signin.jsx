import { useEffect, useState } from "react"

import signup from "../../assets/images/robot.jpg"
import useCookie from 'react-use-cookie';
import useLocalStorage from 'react-use-localstorage';

import { backendUrl } from "../../utils/var"
import ModalError from "../../components/ModalError/ModalError";

export default function Signin() {

    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "");
    const [credit, setCredit] = useLocalStorage('credit', 0);

    const [errorPopup, setErrorPopup] = useState(false);
    const [errorText, setErrorText] = useState("Une erreur est survenue");

    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");

    function handleSubmit(e){
        e.preventDefault()
        fetch(`${backendUrl}/api/v1/login`, {
            method: 'POST',
            headers: {
                'accept': 'text/plain',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password,
            })
        })
        .then(response => {
            if (response.ok) {
              response.json().then(json => {
                  fetch(`${backendUrl}/api/v1/user/me`, {
                    method: 'GET',
                    headers: {
                      "Authorization": "Bearer " + json.token
                    }
                    }).then(response => {
                        if (response.ok) {
                            response.json().then(json => {
                                setCredit(Number(json.credit));
                            })
                        } else {
                            response.text().then(text => {
                                setErrorText(text);
                                setErrorPopup(false);
                            })
                        }
                    }
                )
                setToken(json.token);
              })
            } else {
              response.text().then(text => {
                setErrorText(text);
                setErrorPopup(false);
              })
            }
          })
          .catch(error => {
            // Handle any errors that occurred during the fetch request
            console.error(error);
          });
    }

    useEffect(() => {
        if(token !== "" && token !== undefined){
            window.location = "/dashboard?reload=true";
        }
    }, [token])


    return (
        <div className="signup">
            <img src={signup} alt="happy peoples" />
            <form onSubmit={handleSubmit}>
                <h1 className="littleTitle">Se connecter</h1>
                <input type="email" placeholder="Email" onChange={(e) =>{setEmail(e.target.value)}}/>
                <input type="password" placeholder="Mot de passe" onChange={(e)=>(setPassword(e.target.value))} />
                <button className="bigButton connect" type="submit" >Se connecter</button>
                <a href="/signup">Pas encore de compte ?</a>
                <a href="/ask/reset">Mot de passe oublié ?</a>
                <ModalError open={errorPopup} setOpen={setErrorPopup} text={errorText} />
            </form>
        </div>
    )
}

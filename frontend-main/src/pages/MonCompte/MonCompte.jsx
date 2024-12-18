import Menu from "../../components/Menu/Menu";
import TokenRequied from "../../utils/TokenRequired";
import { backendUrl } from "../../utils/var";
import useCookie from 'react-use-cookie';
import useLocalStorage from 'react-use-localstorage';

import "./MonCompte.scss";
import { useEffect, useRef, useState } from "react";
import ModalError from "../../components/ModalError/ModalError";
import Footer from "../../components/Footer/Footer";

export default function MonCompte(){

    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "")
    const [credit, setCredit] = useLocalStorage('credit', 0);
    const [user, setUser] = useCookie('user', "")
    const [popup, setPopup] = useState(false);
    const [message, setMessage] = useState("Une erreur est survenue");
    const [severity, setSeverity] = useState("success");

    const nameInput = useRef(null);
    const phoneInput = useRef(null);
    const companyInput = useRef(null);

    useEffect(() => {
        fetch(`${backendUrl}/api/v1/user/me`, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'Authorization': 'Bearer '+ token,
            },
        })
        .then(response => response.json())
        .then(data => {
            setUser(data);
            nameInput.current.value = data.name;
            phoneInput.current.value = data.phone;
            companyInput.current.value = data.company;
        })
        .catch(error => {
            
        });
        // eslint-disable-next-line
    }, [])

    function customerPortal(){
        fetch(`${backendUrl}/api/v1/customer_portal`, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'Authorization': 'Bearer '+ token,
            },
        })
        .then(response => response.json())
        .then(data => {
            const a = document.createElement('a');
            a.href = data.url;
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => {
            
        });
    }

    function newPassword(){
        fetch(`${backendUrl}/api/v1/trouble/forgot_email?email=${user.email}`, {
            method: 'GET',
            headers: {
                'accept': 'application/json'
            },
        })
        .then(response => response.text())
        .then(data => {
            setSeverity("success");
            setPopup(true);
            setMessage("Email envoyé à votre adresse email");
        })
        .catch(error => {
            setSeverity("error");
            setPopup(true);
            setMessage(error.message);
        });
    }

    function saveUser(){
        fetch(`${backendUrl}/api/v1/user`, {
            method: 'PATCH',
            headers: {
                'accept': 'text/plain',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+ token,
            },
            body: JSON.stringify({
                name: nameInput.current.value,
                phone: phoneInput.current.value,
                company: companyInput.current.value
              })
            })
        .then(response => {
            if (response.status === 200) {
                setSeverity("success");
                setPopup(true);
                setMessage("Profil mis à jour");
            } else {
                response.text().then(text => {
                    setSeverity("error");
                    setPopup(true);
                    setMessage(text);
                })
            }
        })
    }

    function logout(){
        setToken("");
        setCredit("");
        window.location = "/signin";
    }

    return(
        <>
            <TokenRequied />
            <Menu />
            <div className="moncompte">
                <h1 className="littleTitle">Mon compte</h1>
                <div className="form">
                        <label>Nom, prénom</label>
                        <input ref={nameInput} type="text" placeholder={user.name} />
                        <label>Numéro de téléphone</label>
                        <input ref={phoneInput} type="tel" placeholder={user.phone} />
                        <label>Entreprise</label>
                        <input ref={companyInput} type="text" placeholder={user.company} />
                </div>
                <div className="save">
                    <button onClick={()=>{saveUser()}} className="bigButton">Enregistrer</button>
                    <button onClick={()=>{newPassword()}} className="bigButton empty">Mot de passe oublié</button>
                    <button onClick={customerPortal} className="bigButton empty">Méthode de paiement et abonements</button>
                    <button onClick={logout} className="bigButton empty">Se déconnecter</button>
                </div>
                <ModalError open={popup} setOpen={setPopup} text={message} severity={severity} />
            </div>
            <Footer />
        </>
    )
}
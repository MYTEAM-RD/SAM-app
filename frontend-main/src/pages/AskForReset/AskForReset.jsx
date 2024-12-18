import { useState } from "react"

import signup from "../../assets/images/password_img.jpg"

import { backendUrl } from "../../utils/var"
import ModalError from "../../components/ModalError/ModalError";

export default function AskForReset() {

    const [errorPopup, setErrorPopup] = useState(false);
    const [errorText, setErrorText] = useState("Une erreur est survenue");
    const [severity, setSeverity] = useState("error");

    const [email, setEmail] = useState("");

    function newPassword(e){
        e.preventDefault();
        fetch(`${backendUrl}/api/v1/trouble/forgot_email?email=${email}`, {
            method: 'GET',
            headers: {
                'accept': 'application/json'
            },
        })
        .then(response => response.text())
        .then(data => {
            setSeverity("success");
            setErrorPopup(true);
            setErrorText("Email envoyé à votre adresse email");
        })
        .catch(error => {
            setSeverity("error");
            setErrorPopup(true);
            setErrorText(error.message);
        });
    }


    return (
        <div className="signup">
            <img src={signup} alt="happy peoples" />
            <form onSubmit={newPassword}>
                <h1 className="littleTitle">Mot de passe oublié</h1>
                <input type="email" placeholder="Email" onChange={(e) =>{setEmail(e.target.value)}}/>
                <button className="bigButton connect" type="submit" >Envoyer</button>
                <ModalError open={errorPopup} setOpen={setErrorPopup} text={errorText} severity={severity} />
            </form>
        </div>
    )
}

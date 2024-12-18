import { useState } from "react"

import signup from "../../assets/images/password_img.jpg"

import { backendUrl } from "../../utils/var"
import ModalError from "../../components/ModalError/ModalError";
import ReactPasswordChecklist from "react-password-checklist";
import { useLocation } from "react-router-dom";

export default function ResetPassword() {

    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const code = searchParams.get('code');

    const [errorPopup, setErrorPopup] = useState(false);
    const [errorText, setErrorText] = useState("Une erreur est survenue");
    const [severity, setSeverity] = useState("error");
    // eslint-disable-next-line
    const [isValid, setIsValid] = useState(false);

    const [password, setPassword] = useState("");
    const [passwordAgain, setPasswordAgain] = useState("");

    function newPassword(e){
        e.preventDefault();
        fetch(`${backendUrl}/api/v1/trouble/forgot_email`, {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                password: password,
            })
        })
        .then(response => response.text())
        .then(data => {
            setSeverity("success");
            setErrorPopup(true);
            setErrorText("Mot de passe modifié");
            setTimeout(() => {
                window.location = "/signin";
            }, 2000);
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
            <form className="password" onSubmit={newPassword}>
                <h1 className="littleTitle">Modifier le mot de passe</h1>
                <label>New Password</label>
                <input type="password" placeholder="new password" onChange={(e) =>{setPassword(e.target.value)}}/>
                <label>New Password again</label>
                <input type="password" placeholder="new password" onChange={(e) =>{setPasswordAgain(e.target.value)}}/>
                {password && <ReactPasswordChecklist
                    rules={["minLength","number","capital","match"]}
                    minLength={6}
                    value={password}
                    valueAgain={passwordAgain}
                    onChange={(isValid) => {setIsValid(isValid)}}
			    />}
                <button className="bigButton connect" type="submit" >Change password</button>
                <ModalError open={errorPopup} setOpen={setErrorPopup} text={errorText} severity={severity} />
            </form>
        </div>
    )
}

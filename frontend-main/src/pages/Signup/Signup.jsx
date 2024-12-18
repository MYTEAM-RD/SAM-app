import { useEffect, useState } from "react"

import signup from "../../assets/images/signup.jpg"
import PasswordChecklist from "react-password-checklist"
import useCookie from 'react-use-cookie';
import useLocalStorage from 'react-use-localstorage';
import "./Signup.scss"

import { backendUrl } from "../../utils/var"
import ModalError from "../../components/ModalError/ModalError";

export default function Signup() {

    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "");
    const [credit, setCredit] = useLocalStorage('credit', 0);
    const [errorPopup, setErrorPopup] = useState(false);
    const [errorText, setErrorText] = useState("Une erreur est survenue");

    const [password, setPassword] = useState("");
    const [valid, setIsValid] = useState(false);
    const [name, setName] = useState("");
    const [phone, setPhone] = useState("");
    const [email, setEmail] = useState("");
    const [company, setCompany] = useState("");
    const [type, setType] = useState("");

    function handleSubmit(e){
        e.preventDefault()
        if(valid){
            fetch(`${backendUrl}/api/v1/user`, {
                method: 'POST',
                headers: {
                    'accept': 'text/plain',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                    name: name,
                    company: company,
                    phone: phone,
                    company_type: type
                })
                })
                .then(response => {
                    if (response.status === 200) {
                        setCredit(1);
                        window.location = "/confirm";
                    } else {
                        response.text().then(text => {
                            setErrorText(text);
                            setErrorPopup(true);
                        })
                    }
                })
            }
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
                <h1 className="littleTitle">Créer un compte</h1>
                <input type="text" placeholder="Nom Prénom" onChange={(e) =>{setName(e.target.value)}}/>
                <input type="email" placeholder="Email" onChange={(e) =>{setEmail(e.target.value)}}/>
                <input type="tel" placeholder="phone" onChange={(e) =>{setPhone(e.target.value)}}/>
                <input type="text" placeholder="Company" onChange={(e) =>{setCompany(e.target.value)}}/>
                <select onChange={(e) =>{setType(e.target.value)}}>
                    <option value="startup">Startup</option>
                    <option value="TPE">TPE</option>
                    <option value="PME">PME</option>
                    <option value="ETI">ETI</option>
                    <option value="GE">GE</option>
                </select>
                <input type="password" placeholder="Mot de passe" onChange={(e)=>(setPassword(e.target.value))} />
                {password && <PasswordChecklist
                    rules={["minLength","number","capital"]}
                    minLength={6}
                    value={password}
                    onChange={(isValid) => {setIsValid(isValid)}}
			    />}
                <button className="bigButton connect" type="submit" >Créer mon compte</button>
                <a href="/signin">Vous avez déja un compte ? Se connecter</a>
            </form>
            <ModalError open={errorPopup} setOpen={setErrorPopup} text={errorText} />
        </div>
    )
}

import { useState } from "react"

import { ReactComponent as Mail } from "../../assets/images/envelope.svg"
import { ReactComponent as Phone } from "../../assets/images/telephone.svg"
import { ReactComponent as Location } from "../../assets/images/geo.svg"
import "./Contact.scss"

import { backendUrl } from "../../utils/var"

import Menu from "../../components/Menu/Menu"
import Footer from "../../components/Footer/Footer"

export default function Contact(){

    const [name, setName] = useState("")
    const [phone, setPhone] = useState("")
    const [email, setEmail] = useState("")
    const [message, setMessage] = useState("")

    function handleSubmit(e){
        e.preventDefault()
        if(name === "" || phone === "" || email === "" || message === ""){
            alert("Veuillez remplir tous les champs")
            return
        }
        fetch(`${backendUrl}/api/v1/contact`, {
            method: 'POST',
            headers: {
                'accept': 'text/plain',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                from: email,
                subject: `contact de ${name}`,
                phone: phone,
                content: message
              })
            })
            .then(response => {
                if (response.status === 200) {
                // eslint-disable-next-line no-restricted-globals
                  if (confirm("Message envoyé")) {
                    setName("");
                    setPhone("");
                    setEmail("");
                    setMessage("");
                    window.location = "/";
                  }
                } else {
                  alert("Une erreur est survenue");
                }
              })
    }

    return(
        <>
        <Menu />
        <section className="contact">
            <h1 className="littleTitle">Contact</h1>
            <div>
                <div className="info">
                    <h3>Nous contacter</h3>
                    <p>Et avancer vers la réussite de vos projets</p>
                    <span>
                        <Location />
                        <p>179 Rue de la Pompe, 75116, Paris</p>
                    </span>
                    <span>
                        <Phone />
                        <p>+33 (0)1 70 23 08 20</p>
                    </span>
                    <span>
                        <Mail />
                        <p>contact@elyas-conseil.fr</p>
                    </span>
                </div>
                <div className="form">
                    <input type="text" placeholder="Nom Prénom" onChange={(e)=>{setName(e.target.value)}}/>
                    <input type="tel" placeholder="Teléphone" onChange={(e)=>{setPhone(e.target.value)}}/>
                    <input type="email" placeholder="Email" onChange={(e)=>{setEmail(e.target.value)}}/>
                    <textarea placeholder="Message" onChange={(e)=>{setMessage(e.target.value)}}></textarea>
                    <button className="bigButton" onClick={handleSubmit}>Envoyer</button>
                </div>
            </div>
        </section>
        <Footer />
        </>
    )
}
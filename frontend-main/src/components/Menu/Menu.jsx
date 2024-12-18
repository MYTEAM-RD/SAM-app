import myteam_logo from "../../assets/images/myteam_logo.png";
import useCookie from 'react-use-cookie';
import { HashLink as Link } from 'react-router-hash-link';

//css
import "./Menu.scss";
import useLocalStorage from 'react-use-localstorage';
import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { backendUrl } from "../../utils/var";

export default function Menu() {
    
    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "");
    const [credit, setCredit] = useLocalStorage('credit', 0);

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const reload = queryParams.get('reload');

    function connected(){
        if(token === "" || token === undefined){
            return false;
        }else{
            return true;
        }
    }

    useEffect(() => {
        console.log(reload);
        if(reload === "true"){
            if(connected()){
                fetch(`${backendUrl}/api/v1/user/me`, {
                    method: 'GET',
                    headers: {
                      "Authorization": "Bearer " + token
                    }
                    }).then(response => {
                        if (response.ok) {
                            response.json().then(json => {
                                setCredit(Number(json.credit));
                            })
                        }
                    }
                )
            }
        }
    }, [])

    function getTitle(){
        const search = window.location.pathname.split('/').pop();     
        return search;
    }


    return (
        <nav>
            <img src={myteam_logo} alt="MyTeam Logo" />
            <div>
                <a href="/" className={getTitle() === "" ? "active" :""}>Home</a>
                <Link to="/#howitwork">Comment ça marche</Link>
                <Link to="/#tarif">Tarification</Link>
                <a href="/team" className={getTitle() === "team" ? "active" :""}>Team</a>
                <a href="/contact" className={getTitle() === "contact" ? "active" :""}>Contact</a>
                <a href={connected() ? "/account" : "/signin"} className={getTitle() === "account" ? "active" :""}>Mon compte</a>
                <Link href={connected() ? "/dashboard" : "/signin"} className={getTitle() === "dashboard" ? "active" :""}>Mes analyses</Link>
            </div>
            {connected() && <Link className="credit" to="/#tarif" >{credit} credit</Link>}
            <a href={connected() ? "/dashboard" : "/signin"} className="bigButton">Lancer une analyse</a>
        </nav>
    )
}
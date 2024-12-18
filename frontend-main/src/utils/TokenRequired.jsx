import useCookie from 'react-use-cookie';
import { useEffect } from 'react';

export default function TokenRequied() {

    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "")

    useEffect(() => {
        if(token === "" || token === undefined){
            window.location = "/signin";
        }
    }, [token])

    return(
        <>
        </>
    )
}
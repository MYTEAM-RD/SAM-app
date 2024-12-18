import { useEffect, useState } from "react"
import { backendUrl } from "../../utils/var"
import useCookie from 'react-use-cookie';

import "./Prices.scss"

export default function Prices(){

    const [product, setProduct] = useState([])
    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "");

    function add(index){
        let newProduct = [...product];
        newProduct[index].quantity = newProduct[index].quantity + 1;
        setProduct(newProduct)
    }

    function remove(index){
        let newProduct = [...product];
        if(newProduct[index].quantity > 1){
          newProduct[index].quantity = newProduct[index].quantity - 1;  
        }
        setProduct(newProduct)
    }

    useEffect(() => {
        fetch(`${backendUrl}/api/v1/products`, {
            method: 'GET',
            headers: {
                'accept': 'application/json'
            }
            })
            .then(response => response.json())
                .then(data => {
                    data.data.forEach(element => {
                        element.quantity = 1;
                    });
                    setProduct(data.data)
                })
            .catch(error => {
            // Handle any errors that occurred during the fetch request
        });
    }, [])

    function buyProduct(id, quantity){
        if(token === "" || token === undefined){
            window.location = "/signin";
        }else{
            fetch(`${backendUrl}/api/v1/create_payment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": "Bearer "+ token,
            },
            body: JSON.stringify({
                items: [
                {
                    id: id,
                    quantity: quantity
                }
                ]
            })
            })
            .then(response => response.text())
            .then(data => {
                window.location = data;
            })
            .catch(error => {
                console.error(error);
            });
        }
    }

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

    return(
        <>
        <span id="tarif"></span>
        <section className="prices">
            <h1 className="littleTitle">Tarification</h1>
            <p>SAM est un outil d’analyse de la nature d’un projet par la description des travaux réalisés. Il estime le niveau de difficulté technologique dans sa réalisation (Innovation vs R&D). SAM permet aussi de valider la cohérence des budgets déclarés.</p>
            {token !== "" && token !== undefined && <button className="account-btn" onClick={customerPortal}>Mes achats et abonements.</button>}
            <div className="itemList">
                {product.map((item, index) => {
                    return(
                        <div className="item" key={item.id}>
                            <h4>{item.name}</h4>
                            <div>
                                <h4>{item.price.unit_amount_decimal /100}</h4>
                                <h5>{item.price.type === "recurring" ? "EUR / MOIS" : "EUR"}</h5>
                            </div>
                            <p>
                                {item.description}
                            </p>
                            <span className="buy">
                                <button className={ item.price.type !== "recurring" ? "main-btn multiples" : "main-btn"}  onClick={()=>{buyProduct(item.id,item.quantity)}}>
                                    Acheter {item.quantity > 1 ? item.quantity : ""}
                                </button>
                                {
                                    item.price.type !== "recurring" && 
                                    <div className="selector">
                                        <button onClick={()=>{add(index)}}>+</button>
                                        <button onClick={()=>{remove(index)}}>-</button>
                                    </div>
                                }
                            </span>
                        </div>
                    )
                })}
            </div>
        </section>
    </>
    )
}
import Menu from "../../components/Menu/Menu";
import Footer from "../../components/Footer/Footer";
import TokenRequied from "../../utils/TokenRequired";
import { backendUrl } from '../../utils/var';
import useCookie from 'react-use-cookie';
import {useParams } from 'react-router-dom';
import { useCallback, useState, useEffect, useRef } from "react";
import { ReactComponent as File } from "../../assets/images/file.svg";
import { ReactComponent as Arrow } from "../../assets/images/arrow.svg";
import { ReactComponent as Labore } from "../../assets/images/labore.svg";

import "./Analysis.scss";
import { wait } from "@testing-library/user-event/dist/utils";

export default function Analysis(){

    let { id } = useParams();
    // eslint-disable-next-line
    const [analysis, setAnalysis] = useState({});
    const [budget, setBudget] = useState({});
    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "")
    let budgetRef = useRef([]);
    let budgetInput = useRef([]);

    const getAnalysis = useCallback(() => {
        fetch(`${backendUrl}/api/v1/analyse/${id}/info`, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'Authorization': 'Bearer '+ token,
            },
        })
        .then(response => response.json())
        .then(data => {
            setAnalysis(data);
        })
        .catch(error => {
            
        });
    }, [id, token]);

    useEffect(() => {
        getAnalysis();
    }, [getAnalysis]);

    useEffect(() => {
        budgetInput.current.forEach((element,i) => {
            element.value = analysis.analyse_data.project_list[i].budget;
            budget[i] = analysis.analyse_data.project_list[i].budget;
            if(budget[i] !== undefined && budget[i] !== "" && budget[i] !== null){
                handleEstimate(i);
            }
        });
    }, [analysis]);

    function handleEstimate(index) {
        fetch(`${backendUrl}/api/v1/analyse/${id}/estimate`, {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer '+ token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                budget : budget[index],
                index : index
            })
        })
        .then(response => {
            if (!response.ok) {
              //raise error
              throw new Error('Network response was not ok');
            }
            return response.text();
          })
          .then(data => {
            console.log(data, "response");
            console.log(budgetRef);
            if(data === "True"){
                budgetRef.current[index].classList.remove("false");
                budgetRef.current[index].classList.add("true");
                budgetRef.current[index].classList.add("shake");
                budgetRef.current[index].textContent = "Budget cohérent";
                wait(400).then(()=>{
                    budgetRef.current[index].classList.remove("shake");
                })
            }else{
                budgetRef.current[index].classList.remove("true");
                budgetRef.current[index].classList.add("false");
                budgetRef.current[index].textContent = "Budget incohérent";
                budgetRef.current[index].classList.add("shake");
                wait(400).then(()=>{
                    budgetRef.current[index].classList.remove("shake");
                })
            }
          })
          .catch(error => {
            
          });
    }

    function assignBudget(index, value) {
        let tmp = budget;
        tmp[index] = value;
        setBudget(tmp);
    }

    return(
        <>
            <TokenRequied />
            <Menu />
            <div className="main-analysis">
                <h1>Analyse</h1>
                {analysis.analyse_data !== undefined && analysis.analyse_data.project_list.map((item, index) => {
                    return(
                        <div className="analysis" key={index}>
                            <div className="file">
                                <div>
                                    <File />
                                    <Arrow />
                                </div>
                                <div>
                                    <h3>{item.project_name}</h3>
                                    <h4>{analysis.filename}</h4>
                                </div>
                            </div>
                            <div className="content">
                                <span>
                                    <Labore />
                                    <h2>{item.result}</h2>
                                </span>
                                <h3>{new Date(analysis.created_at*1000).toLocaleString('fr-FR',{ day: '2-digit', month: '2-digit', year: 'numeric' })}</h3>
                            </div>
                            <div className="estimate">
                                <h3>Évaluer la cohérence du montant</h3>
                                <div>
                                    <input ref={el => budgetInput.current[index] = el} type="text" placeholder={item.budget ? item.budget : "Montant à éstimer"} onChange={(e)=>{assignBudget(index,e.target.value)}}/>
                                    <button ref={el => budgetRef.current[index] = el} onClick={()=>handleEstimate(index)}>Evaluer</button>
                                </div>
                            </div>
                        </div>
                    )
                })}
                <a href="/dashboard" className="bigButton">Retour a vos analyses</a>
            </div>
            <Footer />
        </>
    )
}
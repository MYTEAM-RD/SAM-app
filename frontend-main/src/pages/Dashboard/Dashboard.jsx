import Menu from "../../components/Menu/Menu";
import TokenRequired from "../../utils/TokenRequired";
import { useEffect, useState } from "react";
import useCookie from 'react-use-cookie';

import { ReactComponent as Dots } from "../../assets/images/dots.svg";
import { ReactComponent as Loading } from "../../assets/images/loading.svg";

import "./Dashboard.scss"
import { backendUrl } from "../../utils/var";
import ModalMenu from "../../components/ModalMenu/ModalMenu";
import Footer from "../../components/Footer/Footer";

export default function Dashboard() {

    const [analysis , setAnalysis] = useState([]);
    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "")
    const [loading, setLoading] = useState(true);

    function status(budget, estimate){
        const result = estimate/3 < Math.abs(budget) && Math.abs(budget) < estimate*3
        if(estimate === null){
            return "_"
        }
        if(result){
            return "Montant cohérent"
        }else{
            return "Montant incohérent"
        }
    }

    useEffect(() => {
        fetch(`${backendUrl}/api/v1/analyse`, {
          method: 'GET',
          headers: {
            "Authorization": "Bearer " + token
          }
        })
          .then(response => {
            setLoading(false);
            if (!response.ok) {
                //raise error
                throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            var tmp = [];
            data.forEach(project => {
                project.analyse_data.project_list.forEach(file => {
                    tmp.push({
                        name : file.project_name,
                        createdAt: new Date(project.updated_at * 1000),
                        filename: project.filename,
                        type: file.result,
                        budget: file.budget,
                        status: status(file.montant_pred_, file.budget),
                        menu : false,
                        id: project.id
                    });
                })
            });
            tmp.sort((a, b) => b.createdAt - a.createdAt);
            console.log(tmp);
            setAnalysis(tmp)
          })
          .catch(error => {
            
          });
    }, [token])

    function ShowMenu(event, index){
        event.stopPropagation();
        let tmp = [...analysis];
        tmp[index].menu = !tmp[index].menu;
        setAnalysis(tmp);
    }

    function closeMenu(index){
        let tmp = [...analysis];
        tmp[index].menu = false;
        setAnalysis(tmp);
    }

    return(
        <>
            <TokenRequired />
            <Menu />
            <section className='dashboard'>
                <div className="header">
                    <h1>Vos analyses</h1>
                    <a href="/new-project" className="bigButton">Nouvelle analyse</a>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Project name</th>
                            <th>File name</th>
                            <th>Analyze date</th>
                            <th>Type</th>
                            <th>Budget</th>
                            <th>Status</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            analysis.map((item, index) => {
                                return(
                                    <tr key={index} onClick={()=>{window.location.href = `/analysis/${item.id}`}}>
                                        <td>{item.name}</td>
                                        <td>{item.filename}</td>
                                        <td>{item.createdAt.toLocaleString('fr-FR',{ day: '2-digit', month: '2-digit', year: 'numeric' })}</td>
                                        <td>{item.type}</td>
                                        <td>{item.budget} {item.budget ? "€" : "_"}</td>
                                        <td>{item.status}</td>
                                        <td><button className="dot" onClick={(e)=>ShowMenu(e,index)}><Dots /></button><ModalMenu show={item.menu} index={index} close={closeMenu} item={item}/></td>
                                    </tr>
                                )
                            })
                        }
                    </tbody>
                </table>
                {loading ? <div style={{display : "flex", width : "100%", justifyContent : "center"}}>
                        <Loading />
                </div> : analysis.length < 1 && 
                <div className="none">
                    <h3>Vous n'avez pas encore d'analyse</h3>
                    <a href="/new-project" className="bigButton">Nouvelle analyse</a>
                </div>}
            </section>
            <Footer />
        </>
    )
}
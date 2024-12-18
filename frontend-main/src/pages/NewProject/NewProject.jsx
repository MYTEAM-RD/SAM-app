import Menu from "../../components/Menu/Menu";
import TokenRequied from "../../utils/TokenRequired";

import { ReactComponent as Upload } from "../../assets/images/upload.svg";
import { ReactComponent as Loading } from "../../assets/images/loading.svg";
import useCookie from 'react-use-cookie';
import useLocalStorage from 'react-use-localstorage';

import "./NewProject.scss"
import { useRef } from "react";
import { useState } from "react";
import { backendUrl } from "../../utils/var";
import ModalError from "../../components/ModalError/ModalError";


export default function NewProject() {
    // eslint-disable-next-line
    const [token, setToken] = useCookie('token', "")
    const [credit, setCredit] = useLocalStorage('credit', 0);
    const dropZone = useRef(null);
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(0);
    const [errorPopup, setErrorPopup] = useState(false);
    const [errorText, setErrorText] = useState("Une erreur est survenue");

    function drop(e) {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        setFile(file);
        dropZone.current.classList.remove("entered");
    }

    const handleDragOver = (e) => {
        e.preventDefault();
      };
    
    const handleDragEnter = (e) => {
        e.preventDefault();
        dropZone.current.classList.add("entered");
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        dropZone.current.classList.remove("entered");
    };

    function handleSubmit() {
        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        fetch(`${backendUrl}/api/v1/analyse`, {
          method: 'POST',
          body: formData,
          headers: {
            "Authorization": "Bearer " + token
          }
        })
          .then(response => {
            if (!response.ok) {
              response.text().then(text => {
                throw Error(text);
              }).catch(error => {
                setErrorPopup(true);
                setErrorText(error.message);
                setLoading(0);
                setFile(null);
              });
            }
            return response.json();
          })
          .then(data => {
            setCredit(Number(credit) - 1);
            window.location = "/analysis/" + data.id;
            setLoading(false);
          })
          .catch(error => {
            setErrorPopup(true);
            setErrorText(error.message);
          });
      }
    function newAnalysis(){
        return(
        <section className='newProject'>
                <h1 className="littleTitle">Nouvelle analyse</h1>
                <div className="step">
                    <h5>1</h5>
                    <p>Upload</p>
                    <h5>2</h5>
                    <p>Analyse</p>
                    <span></span>
                </div>
                <h2>Uploadez vos synthèses ici :</h2>
                <ol>
                    <li>Vous pouvez uploader un fichier selon les formats .txt, .docx ou .pdf</li>
                    <li>L’outil fonctionne pour une taille de description supérieure à 3 pages et les temps de calcul peuvent être importants pour une taille de description supérieure à 15 pages</li>
                </ol>
                <div ref={dropZone} className="upload" onDrop={drop} onDragOver={handleDragOver} onDragEnter={handleDragEnter} onDragLeave={handleDragLeave}>
                    <Upload />
                    <span>
                        <p>Glissez-déposez vos fichiers ici</p>
                        <p>Limit 200MB , .txt, .docx, .pdf</p>
                    </span>
                    <input type="file" accept=".txt,.docx,.pdf" className="inputfile" onChange={(e)=>{setFile(e.target.files[0])}}/>
                    <button disabled={file === null} className={file !== null ? "bigButton active" : "bigButton"} onClick={handleSubmit}>Lancer l'analyse</button>
                </div>
                <ModalError open={errorPopup} setOpen={setErrorPopup} text={errorText} />
            </section>
        )
    }

    return(
        <>
            <TokenRequied />
            <Menu />
            {
                loading === 0 ? newAnalysis() : <div className="loading">
                <h3>Analyse en cours ...</h3>
                <Loading />
              </div>
            }            
        </>
    )
}
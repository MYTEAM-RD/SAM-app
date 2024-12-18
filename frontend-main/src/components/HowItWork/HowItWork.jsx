import "./HowItWork.scss"

export default function HowItWork() {

    return( 
    <>
    <span id="howitwork"></span>
    <div className="howItWork">
        <h1 className="littleTitle">Comment ça marche ?</h1>
        <section>
            <div className="text">
                <h4>Categorisation de votre projet</h4>
                <p>SAM permet de caractériser un projet en 4 catégories :</p>
                <ol>
                    <li>Très probablement R&D</li>
                    <li>Probablement R&D</li>
                    <li>Innovation mais pourrait passer en R&D</li>
                    <li>Très probablement innovation</li>
                </ol>
                <h4>Confidentialité des données</h4>
                <p>Les synthèses ainsi que l'ensemble des données personnelles entrées dans la plateforme sont employées dans le strict cadre du fonctionnement de l'application. Les données sont encryptés selon les recomandations des autorités (ANSI). Elles ne sont aucunement utilisées à d'autres fins par MYTEAM, cédées ou vendues à des tiers.</p>
                <a href="/signin" className="bigButton">Commencez votre analyse</a>
            </div>
            <div className="step">
                <span>1</span>
                <div>
                    <h4>Upload de votre projet</h4>
                    <p>Vous pouvez uploader un fichier selon les formes .txt, .docx ou .pdf, comprenant plusieurs synthèses techniques mais aussi charger plusieurs fichiers à traiter à la fois.</p>
                </div>
                <span>2</span>
                <div>
                    <h4>Analyse</h4>
                    <p>SAM ira chercher la section correspondante à la description des travaux.</p>
                </div>
                <span>3</span>
                <div>
                    <h4>Resultats</h4>
                    <p>SAM permet de categoriser votre project pour mieux cibler la demande de financement. En plus, SAM permet aujourd’hui de valider l’ordre de grandeur du budget déclaré : cohérent ou incohérent.</p>
                </div>
                <span>4</span>
                <div>
                    <h4>Rapport</h4>
                    <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>
                </div>
                <div className="line"></div>
            </div>
        </section>
    </div>
    </>)
}

import placeholder from "../../assets/images/avatar/placeholder.png"
import { ReactComponent as Linkedin } from "../../assets/images/linkedin.svg"
import { ReactComponent as Facebook } from "../../assets/images/facebook.svg"
import { ReactComponent as Twitter } from "../../assets/images/twitter.svg"

//css
import "./Team.scss"
import Menu from "../../components/Menu/Menu"
import Footer from "../../components/Footer/Footer"

export default function Team(){

    return(
        <>
            <Menu />
            <section className="team">
                <div className="title">
                    <h1 className="littleTitle">Team</h1>
                    <p>Donner de l'énergie à vos données Les visages derrière votre succès</p>
                    <a href="/contact" className="bigButton">Contacter l’equipe</a>
                </div>
                <div className="teamList">
                    <div className="member">
                        <img src={placeholder} alt="placeholder" />
                        <div>
                            <h5>Joachim Carvallo</h5>
                            <h6>Ingénieur Intelligence Artificielle</h6>
                            <span>
                                <a href="/" target="blank">
                                    <Linkedin />
                                </a>
                                <a href="/" target="blank">
                                    <Facebook />
                                </a>
                                <a href="/" target="blank">
                                    <Twitter />
                                </a>
                            </span>
                        </div>
                    </div>
                    <div className="member">
                        <img src={placeholder} alt="placeholder" />
                        <div>
                            <h5>Joachim Carvallo</h5>
                            <h6>Ingénieur Intelligence Artificielle</h6>
                            <span>
                                <a href="/" target="blank">
                                    <Linkedin />
                                </a>
                                <a href="/" target="blank">
                                    <Facebook />
                                </a>
                                <a href="/" target="blank">
                                    <Twitter />
                                </a>
                            </span>
                        </div>
                    </div>
                    <div className="member">
                        <img src={placeholder} alt="placeholder" />
                        <div>
                            <h5>Joachim Carvallo</h5>
                            <h6>Ingénieur Intelligence Artificielle</h6>
                            <span>
                                <a href="/" target="blank">
                                    <Linkedin />
                                </a>
                                <a href="/" target="blank">
                                    <Facebook />
                                </a>
                                <a href="/" target="blank">
                                    <Twitter />
                                </a>
                            </span>
                        </div>
                    </div>
                    <div className="member">
                        <img src={placeholder} alt="placeholder" />
                        <div>
                            <h5>Joachim Carvallo</h5>
                            <h6>Ingénieur Intelligence Artificielle</h6>
                            <span>
                                <a href="/" target="blank">
                                    <Linkedin />
                                </a>
                                <a href="/" target="blank">
                                    <Facebook />
                                </a>
                                <a href="/" target="blank">
                                    <Twitter />
                                </a>
                            </span>
                        </div>
                    </div>
                </div>
            </section>
            <Footer />
        </>
    )
}
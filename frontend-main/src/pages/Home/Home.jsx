import "./Home.scss"

import { ReactComponent as Arrow } from "../../assets/images/arrow.svg"
import { ReactComponent as PlaceHolder } from "../../assets/images/placeholder.svg"
import { ReactComponent as Upload } from "../../assets/images/upload.svg"
import { ReactComponent as Analyze } from "../../assets/images/analyze.svg"
import { ReactComponent as Chart } from "../../assets/images/chart.svg"
import { ReactComponent as FileChart } from "../../assets/images/fileChart.svg"
import HowItWork from "../../components/HowItWork/HowItWork"
import Prices from "../../components/prices/Prices"

import Menu from "../../components/Menu/Menu"
import Footer from "../../components/Footer/Footer"

export default function Home() {
    return (
        <>
            <Menu />
            <section className="firstSection">
                <div className="firstLine">
                    <h1>Get your project analysed in few clicks</h1>
                    <h3>SAM est un outil d’analyse de la nature d’un projet par la description des travaux réalisés. Il estime le niveau de difficulté technologique dans sa réalisation (Innovation vs R&D).</h3>
                    <a href="/signin" className="bigButton">Lancer une analyse</a>
                </div>
                <div className="steps">
                    <div className="item">
                        <Upload />
                        <h3>Upload your file</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur</p>
                    </div>
                    <Arrow />
                    <div className="item">
                        <Analyze />
                        <h3>SAM will analyse it</h3>
                        <p>SAM ira chercher la section correspondante à la description des travaux.</p>
                    </div>
                    <Arrow />
                    <div className="item">
                        <Chart />
                        <h3>Check the result</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur</p>
                    </div>
                    <Arrow />
                    <div className="item">
                        <FileChart />
                        <h3>Download your report</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur</p>
                    </div>
                </div>
            </section>
            <HowItWork />
            <Prices />
            <Footer />
        </>
    )
}
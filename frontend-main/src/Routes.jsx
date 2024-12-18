import React from "react";
import { Route as Page, Routes as Pages} from "react-router-dom";
import Home from "./pages/Home/Home";
import Team from "./pages/Team/Team";
import Contact from "./pages/Contact/Contact";
import Signup from "./pages/Signup/Signup";
import Confirm from "./pages/Confirm/Confirm";
import Dashboard from "./pages/Dashboard/Dashboard";
import Signin from "./pages/Signin/Signin";
import NewProject from "./pages/NewProject/NewProject";
import Analysis from "./pages/Analysis/Analysis";
import MonCompte from "./pages/MonCompte/MonCompte";
import AskForReset from "./pages/AskForReset/AskForReset";
import ResetPassword from "./pages/ResetPassword/ResetPassword";

export default function App() {

  return (
    <>
        <Pages >
            <Page path="/" element={<Home />} />
            <Page path="/team" element={<Team />} />
            <Page path="/contact" element={<Contact />} />
            <Page path="/signup" element={<Signup />} />
            <Page path="/signin" element={<Signin />} />
            <Page path="/confirm" element={<Confirm />} />
            <Page path="/dashboard" element={<Dashboard />} />
            <Page path="/new-project" element={<NewProject />} />
            <Page path="/analysis/:id" element={<Analysis />} />
            <Page path="/account" element={<MonCompte />} />
            <Page path="/ask/reset" element={<AskForReset />} />
            <Page path="/reset/password" element={<ResetPassword />} />
        </Pages>
    </>
  );
}
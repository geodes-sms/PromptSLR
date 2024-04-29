import React from "react";
import "./styles.scss";
import Navbar from "../../components/Navbar/Navbar";
import LLMConfiguration from "../../components/LLMConfiguration/LLMConfiguration";
// import ConfigurationWindow from "../../components/ConfigurationWindow/ConfigurationWindow";

function Main() {
  return (
    <>
      <section className="section__config" id="configuration">
        {/* <ConfigurationWindow /> */}
        <LLMConfiguration />
      </section>
    </>
  );
}

export default Main;

import React from "react";
import "./styles.scss";
import Navbar from "../../components/Navbar/Navbar";
import LLMConfiguration from "../../components/LLMConfiguration/LLMConfiguration";
// import ConfigurationWindow from "../../components/ConfigurationWindow/ConfigurationWindow";

function Main(props: { setProjectId: (val: string) => void }) {
  return (
    <>
      <section className="section__config" id="configuration">
        {/* <ConfigurationWindow /> */}
        <LLMConfiguration setProjectId={props.setProjectId} />
      </section>
    </>
  );
}

export default Main;

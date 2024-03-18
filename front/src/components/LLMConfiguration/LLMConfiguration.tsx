import React from "react";
import "./styles.scss";
import Button from "../Button/Button";

const LLMConfiguration = () => {
  return (
    <div className="llm-configuration">
      <div className="llm-configuration__header">
        <div className="configuration-breadcrumb">LLM</div>
        <Button label="next" onClick={() => {}} disabled={false} />
      </div>
    </div>
  );
};

export default LLMConfiguration;

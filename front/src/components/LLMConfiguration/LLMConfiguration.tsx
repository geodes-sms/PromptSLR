import React, { useState } from "react";
import "./styles.scss";
import Button from "../Button/Button";

const LLMConfiguration = () => {
  const [step, setStep] = useState(1);

  const [llmName, setLlmName] = useState("");

  const [APIKey, setAPIKey] = useState("");
  const [temperature, setTemperature] = useState("0.2");
  const [maxToken, setMaxTokens] = useState("512");

  const [foldCount, setFoldCount] = useState("150");
  const [epochs, setEpochs] = useState("12");
  const [seed, setSeed] = useState("12");

  const [classifierAlgorithm, setClassifierAlgorithm] = useState("");

  const [additionalHyperParams, setadditionalHyperParams] = useState({});

  const LLMForm = [
    {
      label: "LLM Name",
      value: llmName,
      setValue: (value: string) => setLlmName(value),
      type: "dropdown",
      options: ["ChatGPT", "Trainable", "Custom URL"],
    },
  ];

  // Here you should define the form values (using states) and for info for each page
  // pass everything to child components
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

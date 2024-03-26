import React, { useState } from "react";
import "./styles.scss";
import Button from "../Button/Button";
import DropdownSelector from "../DropdownSelector/DropdownSelector";
import TextInput from "../TextInput/TextInput";
import LLMForm from "../LLMForm/LLMForm";

const LLMConfiguration = () => {
  const [step, setStep] = useState(1);

  const [llmName, setLlmName] = useState("");

  const [APIKey, setAPIKey] = useState("");
  const [temperature, setTemperature] = useState("0.2");
  const [maxTokens, setMaxTokens] = useState("512");

  const [foldCount, setFoldCount] = useState("150");
  const [epochs, setEpochs] = useState("12");
  const [seed, setSeed] = useState("12");
  const [classifierAlgorithm, setClassifierAlgorithm] = useState("");

  const [customUrl, setCustomUrl] = useState("");

  const [additionalHyperParams, setadditionalHyperParams] = useState({});

  const renderInput = (formInput: any) => {
    switch (formInput.type) {
      case "dropdown":
        return (
          <DropdownSelector
            label={formInput.label}
            dropdownItems={formInput.options}
            selectedItem={formInput.value}
            setSelectedItem={formInput.setValue}
          />
        );

      case "textInput":
        return (
          <TextInput
            label={formInput.label}
            value={formInput.value}
            setValue={formInput.setValue}
            {...formInput.props}
          />
        );

      default:
        return <></>;
    }
  };
  const renderForm = (formFields: Array<any>) => {
    return (
      <div className="form-flex">
        {formFields.map((item, i) => {
          return <div key={i}>{renderInput(item)}</div>;
        })}
      </div>
    );
  };

  return (
    <div className="llm-configuration">
      <div className="llm-configuration__header">
        <div className="configuration-breadcrumb" style={{ fontSize: "36px" }}>
          LLM
        </div>
        <Button label="next" onClick={() => {}} disabled={false} />
      </div>
      <LLMForm
        llmName={llmName}
        setLlmName={setLlmName}
        APIKey={APIKey}
        setAPIKey={setAPIKey}
        temperature={temperature}
        setTemperature={setTemperature}
        maxTokens={maxTokens}
        setMaxTokens={setMaxTokens}
        renderInput={renderInput}
        renderForm={renderForm}
        classifierAlgorithm={classifierAlgorithm}
        setClassifierAlgorithm={setClassifierAlgorithm}
        foldCount={foldCount}
        setFoldCount={setFoldCount}
        epochs={epochs}
        setEpochs={setEpochs}
        seed={seed}
        setSeed={setSeed}
        customUrl={customUrl}
        setCustomUrl={setCustomUrl}
      />
    </div>
  );
};

export default LLMConfiguration;

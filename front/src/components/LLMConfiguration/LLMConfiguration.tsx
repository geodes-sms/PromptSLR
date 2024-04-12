import React, { useEffect, useState } from "react";
import "./styles.scss";
import Button from "../Button/Button";
import DropdownSelector from "../DropdownSelector/DropdownSelector";
import TextInput from "../TextInput/TextInput";
import LLMForm from "../LLMForm/LLMForm";
import AddableKeyValueInput from "../AddableKeyValueInput/AddableKeyValueInput";
import DatasetForm from "../DatasetForm/DatasetForm";

const LLMConfiguration = () => {
  const [step, setStep] = useState(1);

  // step 1 (llm) fields
  const [llmName, setLlmName] = useState("");

  const [APIKey, setAPIKey] = useState("");
  const [temperature, setTemperature] = useState("0.2");
  const [maxTokens, setMaxTokens] = useState("512");

  const [foldCount, setFoldCount] = useState("0.2");
  const [epochs, setEpochs] = useState("12");
  const [seed, setSeed] = useState("12");
  const [classifierAlgorithm, setClassifierAlgorithm] = useState("");

  const [customUrl, setCustomUrl] = useState("");

  const [additionalHyperParams, setAdditionalHyperParams] = useState([]);

  // step2 (dataset)
  const [selectedDataset, setSelectedDataset] = useState("");

  useEffect(() => {
    console.log("---- Additional params:", additionalHyperParams);
  }, [additionalHyperParams]);

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

      case "addableInputs":
        return (
          <AddableKeyValueInput
            title={formInput.title}
            values={formInput.value}
            setValues={formInput.setValue}
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

  const isRequiredFieldsSatisfied = () => {
    console.log(llmName);
    switch (step) {
      case 1:
        console.log("Stuff:", llmName, APIKey, temperature, maxTokens);
        switch (llmName) {
          case "":
            return false;
          case "ChatGPT":
            return Boolean(APIKey && temperature && maxTokens);
          case "Trainable":
            return Boolean(classifierAlgorithm && foldCount && epochs && seed);
          case "Custom URL":
            return Boolean(customUrl && temperature && maxTokens);

          default:
            return false;
        }

      case 2:
        return Boolean(selectedDataset);

      default:
        return false;
    }
  };

  const renderPaginatedForm = () => {
    switch (step) {
      case 1:
        return (
          <LLMForm
            llmName={llmName}
            setLlmName={setLlmName}
            APIKey={APIKey}
            setAPIKey={setAPIKey}
            temperature={temperature}
            setTemperature={setTemperature}
            maxTokens={maxTokens}
            setMaxTokens={setMaxTokens}
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
            additionalHyperParams={additionalHyperParams}
            setAdditionalHyperParams={setAdditionalHyperParams}
          />
        );

      case 2:
        return (
          <DatasetForm
            selectedDataset={selectedDataset}
            setSelectedDataset={setSelectedDataset}
            renderForm={renderForm}
          />
        );
      default:
        return <div>No form available</div>;
    }
  };

  const gotoNextStep = () => {
    setStep(step + 1);
  };

  return (
    <div className="llm-configuration">
      <div className="llm-configuration__header">
        <div className="configuration-breadcrumb" style={{ fontSize: "36px" }}>
          LLM
        </div>
        <Button
          label="next"
          onClick={() => gotoNextStep()}
          disabled={!isRequiredFieldsSatisfied()}
        />
      </div>
      {renderPaginatedForm()}
    </div>
  );
};

export default LLMConfiguration;

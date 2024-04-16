import React, { useEffect, useState } from "react";
import "./styles.scss";
import Button from "../Button/Button";
import DropdownSelector from "../DropdownSelector/DropdownSelector";
import TextInput from "../TextInput/TextInput";
import LLMForm from "../LLMForm/LLMForm";
import AddableKeyValueInput from "../AddableKeyValueInput/AddableKeyValueInput";
import DatasetForm from "../DatasetForm/DatasetForm";
import MultiSelector from "../MultiSelector/MultiSelector";
import Checkbox from "../Checkbox/Checkbox";
import ConfigurationForm from "../ConfigurationForm/ConfigurationForm";

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

  // step3 (configuration)
  const [features, setFeatures] = useState<string[]>([]);
  const [linient, setLinient] = useState(true);
  const [positiveShots, setPositiveShots] = useState(2);
  const [negativeShots, setNegativeShots] = useState(1);
  const [outputClasses, setOutputClasses] = useState(3);
  const [showReasons, setShowReasons] = useState(true);
  const [confidence, setConfidence] = useState(false);
  const [inclusion, setInclusion] = useState(false);
  const [exclusion, setExclusion] = useState(false);
  const [inclusionCondition, setInclusionCondition] = useState("");
  const [exclusionCondition, setExclusionCondition] = useState("");
  const [inclusionCriteria, setInclusionCriteria] = useState([]);
  const [exclusionCriteria, setExclusionCriteria] = useState([]);

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
            {...formInput.props}
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
            {...formInput.props}
          />
        );

      case "multi-select":
        return (
          <MultiSelector
            label={formInput.label}
            dropdownItems={formInput.items}
            selectedItems={formInput.value}
            setSelectedItems={formInput.setValue}
          />
        );

      case "checkbox":
        return (
          <Checkbox
            label={formInput.label}
            isActive={formInput.value}
            setIsActive={formInput.setValue}
          />
        );

      default:
        return <></>;
    }
  };
  const renderForm = (formFields: Array<any>, className = "") => {
    return (
      <div className={`form-flex ${className}`}>
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

      case 3:
        return (
          <ConfigurationForm
            renderForm={renderForm}
            features={features}
            setFeatures={setFeatures}
            linient={linient}
            setLinient={setLinient}
            positiveShots={positiveShots}
            setPositiveShots={setPositiveShots}
            negativeShots={negativeShots}
            setNegativeShots={setNegativeShots}
            confidence={confidence}
            setConfidence={setConfidence}
            showReasons={showReasons}
            setShowReasons={setShowReasons}
            outputClasses={outputClasses}
            setOutputClasses={setOutputClasses}
            inclusion={inclusion}
            setInclusion={setInclusion}
            exclusion={exclusion}
            setExclusion={setExclusion}
            inclusionCondition={inclusionCondition}
            setInclusionCondition={setInclusionCondition}
            exclusionCondition={exclusionCondition}
            setExclusionCondition={setExclusionCondition}
            inclusionCriteria={inclusionCriteria}
            setInclusionCriteria={setInclusionCriteria}
            exclusionCriteria={exclusionCriteria}
            setExclusionCriteria={setExclusionCriteria}
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

import React, { Dispatch, SetStateAction } from "react";
import "./styles.scss";

const LLMForm = (props: {
  llmName: string;
  setLlmName: (value: string) => void;
  APIKey: string;
  setAPIKey: (value: string) => void;
  temperature: string;
  setTemperature: (value: string) => void;
  maxTokens: string;
  setMaxTokens: (value: string) => void;
  classifierAlgorithm: string;
  setClassifierAlgorithm: (value: string) => void;
  foldCount: string;
  setFoldCount: (value: string) => void;
  epochs: string;
  setEpochs: (value: string) => void;
  seed: string;
  setSeed: (value: string) => void;
  customUrl: string;
  setCustomUrl: (value: string) => void;
  additionalHyperParams: Array<any>;
  setAdditionalHyperParams: Dispatch<SetStateAction<never[]>>;

  renderForm: (formFields: Array<any>) => JSX.Element;
}) => {
  const {
    llmName,
    setLlmName,
    APIKey,
    setAPIKey,
    temperature,
    setTemperature,
    maxTokens,
    setMaxTokens,
    classifierAlgorithm,
    setClassifierAlgorithm,
    foldCount,
    setFoldCount,
    epochs,
    setEpochs,
    seed,
    setSeed,
    customUrl,
    setCustomUrl,
    additionalHyperParams,
    setAdditionalHyperParams,

    renderForm,
  } = props;

  const staticForm = [
    {
      label: "LLM Name",
      value: llmName,
      setValue: (value: string) => setLlmName(value),
      type: "dropdown",
      options: ["ChatGPT", "Trainable", "Custom URL"],
    },
  ];

  const GPTForm = [
    {
      label: "API Key",
      value: APIKey,
      setValue: (value: string) => setAPIKey(value),
      type: "textInput",
    },
    {
      label: "Temperature",
      value: temperature,
      setValue: setTemperature,
      type: "textInput",
      props: {
        type: "number",
        min: 0,
        max: 1,
        step: 0.1,
      },
    },
    {
      label: "Max Tokens",
      value: maxTokens,
      setValue: setMaxTokens,
      type: "textInput",
      props: {
        type: "number",
      },
    },
    {
      title: "Additional Hyperparameters",
      value: additionalHyperParams,
      setValue: (value: never[]) => setAdditionalHyperParams(value),
      type: "addableInputs",
    },
  ];

  const trainableForm = [
    {
      label: "Classifier Algorithm",
      value: classifierAlgorithm,
      setValue: setClassifierAlgorithm,
      type: "dropdown",
      options: [
        "Random",
        "Linear Regression",
        "SVM",
        "Naive Bayes",
        "Random Forest",
      ],
    },
    {
      label: "Fold Count (Train - Test)",
      value: foldCount,
      setValue: setFoldCount,
      type: "textInput",
      props: {
        type: "number",
        min: 0,
        max: 1,
        step: 0.1,
      },
    },
    {
      label: "Epochs",
      value: epochs,
      setValue: setEpochs,
      type: "textInput",
      props: {
        type: "number",
      },
    },
    {
      label: "Seed",
      value: seed,
      setValue: setSeed,
      type: "textInput",
      props: {
        type: "number",
      },
    },
  ];

  const customURLForm = [
    {
      label: "URL",
      value: customUrl,
      setValue: setCustomUrl,
      type: "textInput",
      props: {
        placeholder: "api.url.com",
      },
    },

    {
      label: "Temperature",
      value: temperature,
      setValue: setTemperature,
      type: "textInput",
      props: {
        type: "number",
        min: 0,
        max: 1,
        step: 0.1,
      },
    },
    {
      label: "Max Tokens",
      value: maxTokens,
      setValue: setMaxTokens,
      type: "textInput",
      props: {
        type: "number",
      },
    },
    {
      title: "Additional Hyperparameters",
      value: additionalHyperParams,
      setValue: (value: never[]) => setAdditionalHyperParams(value),
      type: "addableInputs",
    },
  ];

  const renderDynamicForm = () => {
    switch (llmName) {
      case "ChatGPT":
        return <div>{renderForm(GPTForm)}</div>;

      case "Trainable":
        return <div>{renderForm(trainableForm)}</div>;

      case "Custom URL":
        return <div>{renderForm(customURLForm)}</div>;

      default:
        return <></>;
    }
  };

  return (
    <>
      {renderForm(staticForm)}
      {renderDynamicForm()}
    </>
  );
};

export default LLMForm;

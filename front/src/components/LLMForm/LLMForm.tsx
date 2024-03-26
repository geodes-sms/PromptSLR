import React from "react";
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

  renderInput: (formInput: any) => JSX.Element;
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

    renderInput,
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
  ];

  const renderDynamicForm = () => {
    switch (llmName) {
      case "ChatGPT":
        return <div>{renderForm(GPTForm)}</div>;

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
